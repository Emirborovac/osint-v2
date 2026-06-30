"""FastAPI app — OSINT V2 web entry point.

Serves the app shell and the search API. More run/report endpoints
(progress streaming, full report) get layered on later.

Run from the project root:
    python app.py
"""

import logging
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ..search.google import GoogleEngine

log = logging.getLogger("osint.api")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

GOOGLE_PAGES = int(os.environ.get("GOOGLE_PAGES", "5"))

app = FastAPI(title="OSINT V2")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


class SearchRequest(BaseModel):
    query: str


@app.post("/api/search")
async def api_search(req: SearchRequest):
    """Harvest result links from Google for a query (no content fetch yet)."""
    query = (req.query or "").strip()
    if not query:
        return {"query": "", "count": 0, "links": [], "note": "Empty query."}

    log.info("SEARCH request: query=%r (pages=%d)", query, GOOGLE_PAGES)
    engine = GoogleEngine()
    try:
        links = await engine.search(query, pages=GOOGLE_PAGES)
    except Exception:
        log.exception("SEARCH failed: query=%r", query)
        return {"query": query, "count": 0, "links": [],
                "note": "Search error — check the server terminal for the traceback."}

    note = None
    if not links:
        blocked = getattr(engine, "last_blocked", 0)
        note = ("Google returned a consent/CAPTCHA page on every fetch — no links harvested. "
                "This is the no-proxy limitation; check the server logs."
                if blocked else
                "No links harvested — check the server logs for why.")
    log.info("SEARCH response: query=%r -> %d links%s", query, len(links),
             " (note: " + note + ")" if note else "")
    return {"query": query, "count": len(links), "links": links, "note": note}
