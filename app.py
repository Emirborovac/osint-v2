"""OSINT V2 — entry point.

Quick start:
    pip install -r requirements.txt
    python app.py

Then open http://localhost:8000

Config via env (optional): HOST, PORT, RELOAD (1/0).
"""

import os

import uvicorn

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "9000"))
    reload = os.environ.get("RELOAD", "1") == "1"
    uvicorn.run("osint.api.app:app", host=host, port=port, reload=reload)
