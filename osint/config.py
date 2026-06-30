"""Central configuration: env loading, API keys, tier toggles.

Set ENABLED_TIERS to control which collectors run. Start free-only:
    ENABLED_TIERS = {"free", "freemium"}
"""

# TODO: load from environment / .env
ENABLED_TIERS = {"free", "freemium"}  # add "paid" to enable paid collectors

API_KEYS: dict = {}        # TODO: source_name -> key, loaded from env
PROXIES: list = []         # TODO: proxy pool for stealth crawling
