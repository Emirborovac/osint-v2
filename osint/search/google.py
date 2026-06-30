"""Google search-engine scraper (discovery layer). Tier: free.

Scrapes the first N pages of Google results with crawl4ai (headless
Chromium) and extracts organic result links. No SERP API. CAPTCHA
handling and proxy rotation are intentionally not implemented yet.

Every page fetch is logged. Failures are logged, never swallowed silently.
"""

import logging
import urllib.parse

from bs4 import BeautifulSoup

from .base import SearchEngine

try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
except ImportError:  # crawl4ai is optional until installed
    AsyncWebCrawler = None

log = logging.getLogger("osint.search.google")

RESULTS_PER_PAGE = 10
_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
# Skips the EU consent interstitial that would otherwise hide all results.
_CONSENT_COOKIE = {"name": "CONSENT", "value": "YES+1", "domain": ".google.com", "path": "/"}
# Markers of a genuine block / CAPTCHA page. Only consulted when 0 links were
# parsed — these phrases must be specific enough not to appear on real results
# pages (e.g. "/sorry/" and "consent.google.com" do appear on normal pages).
_BLOCK_MARKERS = (
    "our systems have detected unusual traffic",
    "g-recaptcha",
    'id="captcha"',
    "captcha-form",
    "/sorry/index",
)


class GoogleEngine(SearchEngine):
    name = "google"
    tier = "free"

    def _page_url(self, query, start):
        params = {"q": query, "start": start, "hl": "en", "gl": "us"}
        return "https://www.google.com/search?" + urllib.parse.urlencode(params)

    async def search(self, query, pages=5):
        if AsyncWebCrawler is None:
            raise RuntimeError("crawl4ai is not installed")

        browser = BrowserConfig(headless=True, user_agent=_UA, cookies=[_CONSENT_COOKIE])
        run = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, page_timeout=25000)

        seen, out, blocked = set(), [], 0
        log.info("Google harvest START: query=%r pages=%d", query, pages)
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

                # Parse first. Only treat 0-result pages as "blocked" if a genuine
                # CAPTCHA marker is present — avoids discarding real result pages.
                page_links = self._parse(html)
                if not page_links:
                    if self._looks_blocked(html):
                        blocked += 1
                        log.warning(
                            "page %d: 0 results + CAPTCHA markers (status=%s, html=%d bytes) — likely blocked",
                            p + 1, status, len(html),
                        )
                    else:
                        log.info(
                            "page %d: 0 results parsed (status=%s, html=%d bytes) — no more results",
                            p + 1, status, len(html),
                        )
                    continue

                new = 0
                for link in page_links:
                    if link["url"] not in seen:
                        seen.add(link["url"])
                        out.append(link)
                        new += 1
                log.info(
                    "page %d OK: status=%s html=%d bytes, parsed=%d, +%d new (total %d)",
                    p + 1, status, len(html), len(page_links), new, len(out),
                )

        log.info("Google harvest DONE: query=%r total=%d (blocked pages=%d)", query, len(out), blocked)
        self.last_blocked = blocked
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
