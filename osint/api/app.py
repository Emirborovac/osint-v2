"""FastAPI app — OSINT V2 web entry point.

Serves the app shell and the search API. More run/report endpoints
(progress streaming, full report) get layered on later.

Run from the project root:
    python app.py
"""

import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ..search.google import GoogleEngine

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
        return {"query": "", "count": 0, "links": []}
    engine = GoogleEngine()
    links = await engine.search(query, pages=GOOGLE_PAGES)
    return {"query": query, "count": len(links), "links": links}
