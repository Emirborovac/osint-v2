"""opencorporates collector. Category: corporate | Tier: freemium.

See FREE-SOURCES.md / PAID-SOURCES.md for what this source yields.
"""

from ..base import Collector


class OpencorporatesCollector(Collector):
    name = "opencorporates"
    category = "corporate"
    tier = "freemium"
    watched = []   # TODO: entity types consumed
    produces = []  # TODO: entity types produced
    enabled = True

    def collect(self, entity):
        raise NotImplementedError  # TODO
