"""startpage search-engine scraper (discovery layer). Tier: free. TODO."""

from .base import SearchEngine


class StartpageEngine(SearchEngine):
    name = "startpage"
    tier = "free"

    def search(self, query, pages=1):
        raise NotImplementedError  # TODO
