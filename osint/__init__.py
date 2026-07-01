"""OSINT V2 — scraper-first intelligence engine."""

import logging

__version__ = "0.1.0"

# Load .env (API keys, config) if python-dotenv is available. Optional — env
# vars set in the shell work regardless.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Central logging: every osint.* module logs to the terminal. No silent failures.
_logger = logging.getLogger("osint")
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%H:%M:%S")
    )
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False
