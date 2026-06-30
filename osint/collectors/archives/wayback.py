"""wayback collector. Category: archives | Tier: free.

See FREE-SOURCES.md / PAID-SOURCES.md for what this source yields.
"""

from ..base import Collector


class WaybackCollector(Collector):
    name = "wayback"
    category = "archives"
    tier = "free"
    watched = []   # TODO: entity types consumed
    produces = []  # TODO: entity types produced
    enabled = True

    def collect(self, entity):
        raise NotImplementedError  # TODO
