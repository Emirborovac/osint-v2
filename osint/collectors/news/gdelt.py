"""gdelt collector. Category: news | Tier: free.

See FREE-SOURCES.md / PAID-SOURCES.md for what this source yields.
"""

from ..base import Collector


class GdeltCollector(Collector):
    name = "gdelt"
    category = "news"
    tier = "free"
    watched = []   # TODO: entity types consumed
    produces = []  # TODO: entity types produced
    enabled = True

    def collect(self, entity):
        raise NotImplementedError  # TODO
