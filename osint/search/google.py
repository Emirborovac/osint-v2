"""Google search-engine source (discovery layer).

Two paths, chosen automatically:

1. **Custom Search JSON API** (preferred) — used when GOOGLE_API_KEY and
   GOOGLE_CSE_ID are set. Official, reliable, structured, no CAPTCHA/proxy.
   Free 100 queries/day, then paid; max 10 results/page, 100 results/query.
2. **Scraper fallback** — headless Chromium via crawl4ai when no API creds are
   configured. Free, real google.com results, but fragile (CAPTCHA/rate limits).
   No CAPTCHA handling or proxies yet.

Every page/request is logged. Failures are logged, never swallowed silently.
"""

import logging
import os
import urllib.parse

import httpx
from bs4 import BeautifulSoup

from .base import SearchEngine

try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
except ImportError:  # crawl4ai is optional until installed
    AsyncWebCrawler = None

log = logging.getLogger("osint.search.google")

RESULTS_PER_PAGE = 10
_CSE_ENDPOINT = "https://www.googleapis.com/customsearch/v1"
_CSE_MAX_START = 91  # API allows start up to 91 (100 results max per query)

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_CONSENT_COOKIE = {"name": "CONSENT", "value": "YES+1", "domain": ".google.com", "path": "/"}
_BLOCK_MARKERS = (
    "our systems have detected unusual traffic",
    "g-recaptcha",
    'id="captcha"',
    "captcha-form",
    "/sorry/index",
)


class GoogleEngine(SearchEngine):
    name = "google"
    tier = "freemium"  # API tier is free up to 100/day; scraper path is free

    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY") or ""
        self.cse_id = os.environ.get("GOOGLE_CSE_ID") or ""
        self.last_blocked = 0

    async def search(self, query, pages=5):
        if self.api_key and self.cse_id:
            return await self._search_api(query, pages)
        log.info("No GOOGLE_API_KEY/GOOGLE_CSE_ID set — using scraper fallback")
        return await self._search_scrape(query, pages)

    # ---- Custom Search JSON API (preferred) --------------------------------
    async def _search_api(self, query, pages):
        out, seen = [], set()
        log.info("Google CSE API START: query=%r pages=%d", query, pages)
        async with httpx.AsyncClient(timeout=15) as client:
            for p in range(pages):
                start = p * RESULTS_PER_PAGE + 1
                if start > _CSE_MAX_START:
                    log.info("CSE reached 100-result cap; stopping")
                    break
                params = {"key": self.api_key, "cx": self.cse_id, "q": query,
                          "start": start, "num": RESULTS_PER_PAGE}
                try:
                    r = await client.get(_CSE_ENDPOINT, params=params)
                except Exception:
                    log.exception("CSE page %d request raised", p + 1)
                    continue
                if r.status_code != 200:
                    log.warning("CSE page %d HTTP %s: %s", p + 1, r.status_code, r.text[:180])
                    if r.status_code in (403, 429):  # quota / key problem — no point continuing
                        break
                    continue
                items = r.json().get("items") or []
                new = 0
                for it in items:
                    url = it.get("link")
                    if url and url not in seen:
                        seen.add(url)
                        out.append({"url": url, "title": it.get("title", ""),
                                    "snippet": it.get("snippet", "")})
                        new += 1
                log.info("CSE page %d OK: items=%d, +%d new (total %d)", p + 1, len(items), new, len(out))
                if len(items) < RESULTS_PER_PAGE:  # no more results
                    break
        log.info("Google CSE API DONE: query=%r total=%d", query, len(out))
        return out

    # ---- Scraper fallback --------------------------------------------------
    def _page_url(self, query, start):
        params = {"q": query, "start": start, "hl": "en", "gl": "us"}
        return "https://www.google.com/search?" + urllib.parse.urlencode(params)

    async def _search_scrape(self, query, pages):
        if AsyncWebCrawler is None:
            raise RuntimeError("crawl4ai is not installed")

        browser = BrowserConfig(headless=True, user_agent=_UA, cookies=[_CONSENT_COOKIE])
        run = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, page_timeout=25000)

        seen, out, blocked = set(), [], 0
        log.info("Google SCRAPE START: query=%r pages=%d", query, pages)
        async with AsyncWebCrawler(config=browser) as crawler:
            for p in range(pages):
                url = self._page_url(query, p * RESULTS_PER_PAGE)
                log.info("page %d/%d -> %s", p + 1, pages, url)
                try:
                    res = await crawler.arun(url, config=run)
                except Exception:
                    log.exception("page %d fetch raised an exception", p + 1)
                    continue

                html = getattr(res, "html", "") or ""
                ok = getattr(res, "success", False)
                status = getattr(res, "status_code", None)
                if not ok:
                    log.warning("page %d NOT ok (status=%s, html=%d bytes)", p + 1, status, len(html))
                    continue

                page_links = self._parse(html)
                if not page_links:
                    if self._looks_blocked(html):
                        blocked += 1
                        log.warning(
                            "page %d: 0 results + CAPTCHA markers (status=%s, html=%d bytes) — likely blocked",
                            p + 1, status, len(html),
                        )
                    else:
                        log.info("page %d: 0 results parsed (status=%s, html=%d bytes)", p + 1, status, len(html))
                    continue

                new = 0
                for link in page_links:
                    if link["url"] not in seen:
                        seen.add(link["url"])
                        out.append(link)
                        new += 1
                log.info("page %d OK: status=%s html=%d bytes, parsed=%d, +%d new (total %d)",
                         p + 1, status, len(html), len(page_links), new, len(out))

        self.last_blocked = blocked
        log.info("Google SCRAPE DONE: query=%r total=%d (blocked pages=%d)", query, len(out), blocked)
        return out

    def _parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        out = []
        for a in soup.select("a:has(h3)"):
            url = self._clean(a.get("href") or "")
            if not url:
                continue
            h3 = a.find("h3")
            out.append({"url": url, "title": h3.get_text(strip=True) if h3 else "", "snippet": ""})
        return out

    @staticmethod
    def _looks_blocked(html):
        low = html.lower()
        return any(m in low for m in _BLOCK_MARKERS)

    @staticmethod
    def _clean(href):
        if href.startswith("/url?"):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            href = (qs.get("q") or qs.get("url") or [""])[0]
        if not href.startswith("http"):
            return None
        host = urllib.parse.urlparse(href).netloc.lower()
        if "google." in host or "googleusercontent" in host or "webcache" in host:
            return None
        return href
