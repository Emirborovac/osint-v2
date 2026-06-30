"""google search-engine scraper (discovery layer). Tier: free. TODO."""

from .base import SearchEngine


class GoogleEngine(SearchEngine):
    name = "google"
    tier = "free"

    def search(self, query, pages=1):
        raise NotImplementedError  # TODO
