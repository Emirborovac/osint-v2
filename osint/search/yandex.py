"""yandex search-engine scraper (discovery layer). Tier: free. TODO."""

from .base import SearchEngine


class YandexEngine(SearchEngine):
    name = "yandex"
    tier = "free"

    def search(self, query, pages=1):
        raise NotImplementedError  # TODO
