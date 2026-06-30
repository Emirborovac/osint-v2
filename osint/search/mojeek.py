"""mojeek search-engine scraper (discovery layer). Tier: free. TODO."""

from .base import SearchEngine


class MojeekEngine(SearchEngine):
    name = "mojeek"
    tier = "free"

    def search(self, query, pages=1):
        raise NotImplementedError  # TODO
