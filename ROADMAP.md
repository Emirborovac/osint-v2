# OSINT V2 — Build Roadmap

A scraper-first OSINT engine that **expands like a web**: from a single seed it
scrapes search engines, harvests result links, deep-crawls every page, enriches
with free public sources, then hands the whole corpus to the AI to synthesize a
full report.

> **Core principle: NO paid search / SERP APIs.**
> Discovery is done by **scraping search engines ourselves** (crawl4ai).
> Enrichment uses **free public APIs only**. The only money spent is the LLM
> synthesis step.

---

## Engine flow

```
                       ┌────────────────────────────────────────────┐
   seed (name,         │  1. SEARCH (scraped, multi-page 1–5)        │
   email, username, ──▶│     DuckDuckGo · Google · Bing  (no SERP API)│
   phone, domain)      └───────────────────┬────────────────────────┘
                                           │ harvested result URLs
                                           ▼
                       ┌────────────────────────────────────────────┐
                       │  2. DEEP CRAWL (the web expansion)          │
                       │     navigate INTO each URL, scrape content, │
                       │     optionally follow links N levels deep   │
                       └───────────────────┬────────────────────────┘
                                           │ page content + extracted entities
                          ┌────────────────┴───────────────┐
                          ▼                                 ▼
        ┌──────────────────────────────┐   ┌──────────────────────────────┐
        │ 3. STRUCTURED ENRICHMENT      │   │  (entities discovered during   │
        │    free APIs: RDAP, crt.sh,   │◀──│   crawl feed back as new seeds │
        │    OpenCorporates, GitHub …   │   │   → recursive expansion)       │
        └───────────────┬──────────────┘   └────────────────────────────────┘
                        ▼
        ┌──────────────────────────────┐
        │ 4. AGGREGATE + RESOLVE        │  dedupe, entity resolution,
        │    build the graph            │  confidence scoring
        └───────────────┬──────────────┘
                        ▼
        ┌──────────────────────────────┐
        │ 5. AI SYNTHESIS (map-reduce)  │  per-page summaries → cluster →
        │    → full report (PDF/HTML)   │  final report with citations
        └──────────────────────────────┘
```

---

## Legend

| Field | Meaning |
|---|---|
| **Priority** | P0 = required for MVP pipeline · P1 = high · P2 = nice-to-have |
| **Status** | ☐ todo · ◐ in progress · ☑ done |
| **Type** | `scrape` (HTML), `crawl` (browser/crawl4ai), `api` (free JSON), `cli` (local tool), `core` (engine) |

---

## Phase 0 — Foundation & scaffold

| # | Component | What it does | Type | Priority | Status |
|---|---|---|---|---|---|
| 0.1 | Repo scaffold & config | Package layout, `.env`, settings, logging | core | P0 | ☐ |
| 0.2 | Dependency setup | crawl4ai + Playwright, requests, flask, networkx, pydantic | core | P0 | ☐ |
| 0.3 | Entity model | Typed entities (PERSON, EMAIL, USERNAME, PHONE, DOMAIN, ORG, URL, DOCUMENT…) | core | P0 | ☐ |
| 0.4 | Graph store | Nodes + relationships + confidence (carry from V1) | core | P0 | ☐ |
| 0.5 | Content/result store | Cache + dedupe of scraped pages (avoid re-fetch, cut cost) | core | P0 | ☐ |
| 0.6 | Run orchestrator | One investigation = one run; progress events (SSE) | core | P0 | ☐ |

## Phase 1 — Search discovery (SCRAPED — no SERP APIs)

| # | Component | What it does | Type | Priority | Status |
|---|---|---|---|---|---|
| 1.1 | DuckDuckGo HTML scraper | `html.duckduckgo.com/html` — **primary**, no key, clean, low anti-bot | scrape | P0 | ☐ |
| 1.2 | Google results scraper | crawl4ai + **stealth + proxy rotation**, pages 1–5 (anti-bot heavy) | crawl | P1 | ☐ |
| 1.3 | Bing results scraper | HTML scrape, second free engine for coverage | scrape | P1 | ☐ |
| 1.4 | Fallback engines | Startpage / Mojeek / Brave frontend (resilience if one blocks) | scrape | P2 | ☐ |
| 1.5 | Query builder / dorking | Name variants + `site:` dorks (linkedin, github, x, etc.) | core | P0 | ☐ |
| 1.6 | Result normalizer | Extract {url, title, snippet}; dedupe across engines & pages; rank | core | P0 | ☐ |

## Phase 2 — Deep crawl / web expansion (the core)

| # | Component | What it does | Type | Priority | Status |
|---|---|---|---|---|---|
| 2.1 | crawl4ai page reader | Navigate into each harvested URL → `fit_markdown` content | crawl | P0 | ☐ |
| 2.2 | Recursive link follower | BFS / best-first; depth + breadth + per-domain caps | crawl | P1 | ☐ |
| 2.3 | Entity extractor | RegexExtractionStrategy: emails, phones, usernames, handles | core | P0 | ☐ |
| 2.4 | Feedback loop | Discovered entities re-enter the pipeline as new seeds | core | P1 | ☐ |
| 2.5 | Blocked-site guard | Skip LinkedIn / IG / FB / TikTok (login walls, legal) | core | P0 | ☐ |
| 2.6 | Anti-bot layer | Rate limiting, proxy rotation, stealth, retries/backoff | core | P1 | ☐ |
| 2.7 | Crawl scope controls | max pages / depth / per-domain budget / timeout (cost guardrails) | core | P0 | ☐ |

## Phase 3 — Structured enrichment (free public APIs — stay)

| # | Component | What it does | Type | Priority | Status |
|---|---|---|---|---|---|
| 3.1 | RDAP / WHOIS | Domain → registrant, org, email | api | P1 | ☐ |
| 3.2 | crt.sh | Certificate transparency → subdomains / related domains | api | P2 | ☐ |
| 3.3 | OpenCorporates | Company → officers, directors, jurisdictions | api | P1 | ☐ |
| 3.4 | Companies House (UK) | Authoritative UK officers + filings | api | P2 | ☐ |
| 3.5 | SEC EDGAR | US filings full-text (execs, insiders) | api | P2 | ☐ |
| 3.6 | GitHub | User / code / commit search → usernames, leaked emails | api | P1 | ☐ |
| 3.7 | Gravatar | Email → profile / avatar / linked accounts | api | P2 | ☐ |
| 3.8 | Keybase | Username → cryptographically linked accounts | api | P2 | ☐ |
| 3.9 | GDELT + Wikipedia/Wikidata | News mentions + biography (free) | api | P2 | ☐ |
| 3.10 | Sherlock / Holehe / Ignorant | Username/email/phone → account existence (CLIs) | cli | P2 | ☐ |

## Phase 4 — Aggregation & entity resolution

| # | Component | What it does | Type | Priority | Status |
|---|---|---|---|---|---|
| 4.1 | Findings aggregator | Merge crawl output + all collectors into one corpus | core | P0 | ☐ |
| 4.2 | Entity resolution | Dedupe, merge aliases, link across sources | core | P1 | ☐ |
| 4.3 | Confidence scoring | Per-claim confidence from evidence (carry/upgrade V1) | core | P1 | ☐ |
| 4.4 | Graph builder | Relationships + pivots for the report/UI | core | P1 | ☐ |

## Phase 5 — AI synthesis & report

| # | Component | What it does | Type | Priority | Status |
|---|---|---|---|---|---|
| 5.1 | Map-reduce summarizer | Per-page summary → cluster → final (handles large crawls) | core | P0 | ☐ |
| 5.2 | One-shot mode | Single-call synthesis for small crawls (configurable) | core | P2 | ☐ |
| 5.3 | Report generator | PDF/HTML, sectioned, **inline citations + source URLs** | core | P0 | ☐ |
| 5.4 | Media collection | og:image + scraped images into the report | core | P2 | ☐ |

## Phase 6 — Orchestration, API & UI

| # | Component | What it does | Type | Priority | Status |
|---|---|---|---|---|---|
| 6.1 | Pipeline runner | search → crawl → enrich → aggregate → report | core | P0 | ☐ |
| 6.2 | Flask API + streaming | Start run, stream progress (SSE), fetch report | core | P0 | ☐ |
| 6.3 | Async job queue | Background runs, concurrency control | core | P1 | ☐ |
| 6.4 | Frontend | Investigation UI + graph view (carry/upgrade V1) | core | P1 | ☐ |

---

## Excluded — do NOT scrape

| Site | Reason |
|---|---|
| LinkedIn | Hard login wall + aggressive anti-bot + legal exposure |
| Instagram / Facebook | Login wall + account bans + legal restrictions |
| TikTok | Signed-request anti-bot; brittle, high-maintenance |
| X / Twitter | Login required to view; viable access is paid-only |

> These are only ever picked up as **mentions in scraped search snippets / third-party pages**, never crawled directly.

---

## MVP definition (first runnable slice)

Phase 0 + **1.1 DuckDuckGo scraper** + **2.1 page reader** + **2.3 entity extractor**
+ **4.1 aggregator** + **5.1 map-reduce report** + **6.1/6.2 pipeline & API**.
Everything else layers on top once the search → crawl → report spine works end to end.
