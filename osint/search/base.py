"""Base search-engine scraper interface."""

from abc import ABC, abstractmethod


class SearchEngine(ABC):
    name: str = "base"
    tier: str = "free"
    enabled: bool = True

    @abstractmethod
    def search(self, query: str, pages: int = 1):
        """Return a list of {"url", "title", "snippet"} result dicts."""
        raise NotImplementedError
