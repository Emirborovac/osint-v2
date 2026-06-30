"""crunchbase collector. Category: corporate | Tier: paid.

See FREE-SOURCES.md / PAID-SOURCES.md for what this source yields.
"""

from ..base import Collector


class CrunchbaseCollector(Collector):
    name = "crunchbase"
    category = "corporate"
    tier = "paid"
    watched = []   # TODO: entity types consumed
    produces = []  # TODO: entity types produced
    enabled = True

    def collect(self, entity):
        raise NotImplementedError  # TODO
