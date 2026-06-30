"""Collector registry: auto-discovery + tier filtering."""

from ..config import ENABLED_TIERS


class Registry:
    """Discovers Collector subclasses and filters them by enabled tier."""

    def __init__(self):
        self._collectors = []  # populated by discover()

    def discover(self):
        """TODO: import osint.collectors.* and register Collector subclasses."""
        raise NotImplementedError

    def active(self, tiers=ENABLED_TIERS):
        """Return enabled collectors whose tier is in `tiers` (free-first)."""
        return [c for c in self._collectors if c.enabled and c.tier in tiers]

    def for_entity(self, etype, tiers=ENABLED_TIERS):
        """Active collectors that consume the given entity type."""
        return [c for c in self.active(tiers) if etype in c.watched]
