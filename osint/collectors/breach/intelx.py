"""intelx collector. Category: breach | Tier: freemium.

See FREE-SOURCES.md / PAID-SOURCES.md for what this source yields.
"""

from ..base import Collector


class IntelxCollector(Collector):
    name = "intelx"
    category = "breach"
    tier = "freemium"
    watched = []   # TODO: entity types consumed
    produces = []  # TODO: entity types produced
    enabled = True

    def collect(self, entity):
        raise NotImplementedError  # TODO
