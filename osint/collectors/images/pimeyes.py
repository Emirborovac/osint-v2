"""pimeyes collector. Category: images | Tier: paid.

See FREE-SOURCES.md / PAID-SOURCES.md for what this source yields.
"""

from ..base import Collector


class PimeyesCollector(Collector):
    name = "pimeyes"
    category = "images"
    tier = "paid"
    watched = []   # TODO: entity types consumed
    produces = []  # TODO: entity types produced
    enabled = True

    def collect(self, entity):
        raise NotImplementedError  # TODO
