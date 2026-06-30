"""Google search-engine scraper (discovery layer). Tier: free.

Scrapes the first N pages of Google results with crawl4ai (headless
Chromium) and extracts organic result links. No SERP API. CAPTCHA
handling and proxy rotation are intentionally not implemented yet.
"""

import urllib.parse

from bs4 import BeautifulSoup

from .base import SearchEngine

try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
except ImportError:  # crawl4ai is optional until installed
    AsyncWebCrawler = None

RESULTS_PER_PAGE = 10
_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
# Skips the EU consent interstitial that would otherwise hide all results.
_CONSENT_COOKIE = {"name": "CONSENT", "value": "YES+1", "domain": ".google.com", "path": "/"}


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

        seen, out = set(), []
        async with AsyncWebCrawler(config=browser) as crawler:
            for p in range(pages):
                url = self._page_url(query, p * RESULTS_PER_PAGE)
                try:
                    res = await crawler.arun(url, config=run)
                except Exception:
                    continue
                if not getattr(res, "success", False):
                    continue
                for link in self._parse(getattr(res, "html", "") or ""):
                    if link["url"] not in seen:
                        seen.add(link["url"])
                        out.append(link)
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
