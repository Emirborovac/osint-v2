"""OSINT V2 — entry point.

Quick start:
    pip install -r requirements.txt
    python app.py

Then open http://localhost:9000

Config via env (optional): HOST, PORT, RELOAD (1/0).

RELOAD defaults to 0: just restart the process to load code changes. Auto-reload
(WatchFiles) is unreliable on some drives (e.g. mapped/network X:), which can
leave a stale worker serving old code. Set RELOAD=1 to opt in.
"""

import os

import uvicorn

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "9000"))
    reload = os.environ.get("RELOAD", "0") == "1"
    uvicorn.run("osint.api.app:app", host=host, port=port, reload=reload)
