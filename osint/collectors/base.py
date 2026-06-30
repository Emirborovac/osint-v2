"""Base collector interface. One file per source; grouped by category.

Each collector declares its `tier` (free | freemium | paid). The registry
filters by tier, so paid collectors can live here disabled until needed.
"""

from abc import ABC, abstractmethod


class Collector(ABC):
    name: str = "base"
    category: str = ""
    tier: str = "free"        # free | freemium | paid
    watched: list = []        # entity types this collector consumes
    produces: list = []       # entity types this collector can yield
    enabled: bool = True

    @abstractmethod
    def collect(self, entity):
        """Run against an entity; return a list of Finding objects."""
        raise NotImplementedError
