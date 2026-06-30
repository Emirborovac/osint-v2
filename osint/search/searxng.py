"""searxng search-engine scraper (discovery layer). Tier: free. TODO."""

from .base import SearchEngine


class SearxngEngine(SearchEngine):
    name = "searxng"
    tier = "free"

    def search(self, query, pages=1):
        raise NotImplementedError  # TODO
