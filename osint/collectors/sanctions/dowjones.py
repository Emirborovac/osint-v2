"""dowjones collector. Category: sanctions | Tier: paid.

See FREE-SOURCES.md / PAID-SOURCES.md for what this source yields.
"""

from ..base import Collector


class DowjonesCollector(Collector):
    name = "dowjones"
    category = "sanctions"
    tier = "paid"
    watched = []   # TODO: entity types consumed
    produces = []  # TODO: entity types produced
    enabled = True

    def collect(self, entity):
        raise NotImplementedError  # TODO
