# OSINT V2

Scraper-first OSINT engine. See [ROADMAP.md](ROADMAP.md) and
[FREE-SOURCES.md](FREE-SOURCES.md) / [PAID-SOURCES.md](PAID-SOURCES.md).

## Quick start

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:9000

## Config (optional, via env)

| Var | Default | Meaning |
|---|---|---|
| `HOST` | `0.0.0.0` | bind address |
| `PORT` | `9000` | port |
| `RELOAD` | `0` | auto-reload on code change (unreliable on mapped drives; restart manually) |
