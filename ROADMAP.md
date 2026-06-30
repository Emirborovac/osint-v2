# OSINT V2 — Build Roadmap

A scraper-first OSINT engine that **expands like a web**: from a single seed it
scrapes search engines, harvests result links, deep-crawls every page, enriches
with public sources, then hands the whole corpus to the AI to synthesize a full
report.

> **Core principle: NO paid search / SERP APIs.**
> Discovery is done by **scraping search engines ourselves** (crawl4ai).
> The build is **free-first**: Stage 1 ships the engine + every free source.
> Paid sources are **Stage 2** — enabled only after Stage 1 is complete.

**Two stages**
- **Stage 1 — Free build:** engine framework + all free / freemium sources (~75). This is the whole product on a $0 source budget (only the LLM synthesis step costs money).
- **Stage 2 — Paid sources:** payment-required sources, added later. Each has a free alternative already shipped in Stage 1, so nothing is blocked.

See [FREE-SOURCES.md](FREE-SOURCES.md) and [PAID-SOURCES.md](PAID-SOURCES.md) for what each source yields.

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
        │ 3. SOURCE ENRICHMENT          │   │  (entities discovered during   │
        │    free collectors by category│◀──│   crawl feed back as new seeds │
        │    (infra, corporate, social…)│   │   → recursive expansion)       │
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
| **Type** | `scrape` (HTML) · `crawl` (browser/crawl4ai) · `api` (JSON) · `cli` (local tool) · `core` (engine) |
| **Tier** | `free` · `freemium` (free tier now, pay only to scale) |
| **Status** | ☐ todo · ◐ in progress · ☑ done |

---

# STAGE 1 — FREE BUILD

## Part A — Engine & framework

### Phase 0 — Foundation & scaffold

| # | Component | What it does | Type | Status |
|---|---|---|---|---|
| 0.1 | Repo scaffold & config | Package layout, `.env`, settings, tier toggles | core | ☑ |
| 0.2 | Dependency setup | crawl4ai + Playwright, requests, fastapi, networkx, pydantic | core | ◐ |
| 0.3 | Entity model | Typed entities (PERSON, EMAIL, USERNAME, PHONE, DOMAIN, ORG, URL, DOCUMENT…) | core | ☐ |
| 0.4 | Graph store | Nodes + relationships + confidence | core | ☐ |
| 0.5 | Content/result store | Cache + dedupe of scraped pages | core | ☐ |
| 0.6 | Collector registry | Auto-discover collectors, filter by tier (free-first) | core | ☐ |
| 0.7 | Run orchestrator | One investigation = one run; progress events (SSE) | core | ☐ |

### Phase 1 — Search discovery (scraped engines — no SERP APIs)

| # | Source | What it does | Type | Status |
|---|---|---|---|---|
| 1.1 | DuckDuckGo (HTML) | **primary**, no key, clean, low anti-bot | scrape | ☐ |
| 1.2 | Bing | second free engine for coverage | scrape | ☐ |
| 1.3 | Google | crawl4ai + stealth + proxy, pages 1–5 (anti-bot heavy) | crawl | ☐ |
| 1.4 | Yandex | different index + image discovery | crawl | ☐ |
| 1.5 | Startpage · Brave · Mojeek · SearXNG | fallback engines for resilience | scrape | ☐ |
| 1.6 | Query builder / dorking | name variants + `site:` dorks | core | ☐ |
| 1.7 | Result normalizer | extract {url,title,snippet}; dedupe across engines/pages; rank | core | ☐ |

### Phase 2 — Deep crawl / web expansion (the core)

| # | Component | What it does | Type | Status |
|---|---|---|---|---|
| 2.1 | crawl4ai page reader | navigate into each URL → `fit_markdown` content | crawl | ☐ |
| 2.2 | Recursive link follower | BFS / best-first; depth + breadth + per-domain caps | crawl | ☐ |
| 2.3 | Entity extractor | regex: emails, phones, usernames, handles | core | ☐ |
| 2.4 | Feedback loop | discovered entities re-enter pipeline as new seeds | core | ☐ |
| 2.5 | Blocked-site guard | skip LinkedIn / IG / FB / TikTok | core | ☐ |
| 2.6 | Anti-bot layer | rate limiting, proxy rotation, stealth, retries/backoff | core | ☐ |
| 2.7 | Crawl scope controls | max pages / depth / per-domain budget / timeout | core | ☐ |

### Phase 4 — Aggregation & entity resolution

| # | Component | What it does | Type | Status |
|---|---|---|---|---|
| 4.1 | Findings aggregator | merge crawl output + all collectors into one corpus | core | ☐ |
| 4.2 | Entity resolution | dedupe, merge aliases, link across sources | core | ☐ |
| 4.3 | Confidence scoring | per-claim confidence from evidence | core | ☐ |
| 4.4 | Graph builder | relationships + pivots for report/UI | core | ☐ |

### Phase 5 — AI synthesis & report

| # | Component | What it does | Type | Status |
|---|---|---|---|---|
| 5.1 | Map-reduce summarizer | per-page summary → cluster → final (handles large crawls) | core | ☐ |
| 5.2 | One-shot mode | single-call synthesis for small crawls (configurable) | core | ☐ |
| 5.3 | Report generator | PDF/HTML, sectioned, **inline citations + source URLs** | core | ☐ |
| 5.4 | Media collection | og:image + scraped images into the report | core | ☐ |

### Phase 6 — Orchestration, API & UI

| # | Component | What it does | Type | Status |
|---|---|---|---|---|
| 6.1 | Pipeline runner | search → crawl → enrich → aggregate → report | core | ☐ |
| 6.2 | FastAPI + streaming | start run, stream progress (SSE), fetch report | core | ◐ |
| 6.3 | Async job queue | background runs, concurrency control | core | ☐ |
| 6.4 | Frontend | investigation UI + graph view | core | ☐ |

---

## Part B — Free collectors (every free source)

Grouped by build wave. One row per source = one file under `osint/collectors/<category>/`.

### Wave 1 — Archives (`collectors/archives/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| wayback | historical snapshots, deleted pages | api+scrape | free | ☐ |
| archive_today | snapshots | scrape | free | ☐ |
| common_crawl | bulk historical web index | api | free | ☐ |

### Wave 2 — Identity

**Username** (`collectors/username/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| sherlock | accounts across ~400 sites | cli | free | ☐ |
| maigret | accounts across ~3000 sites | cli | free | ☐ |
| whatsmyname | curated account check | api | free | ☐ |
| blackbird | account check | cli | free | ☐ |
| socialscan | username availability | cli | free | ☐ |

**Email** (`collectors/email/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| holehe | account existence ~120 sites | cli | free | ☐ |
| emailrep | reputation, linked profiles | api | free | ☐ |
| epieos | Google account, linked services | scrape/api | freemium | ☐ |
| hunter | verification, domain pattern | api | freemium | ☐ |
| gravatar | profile, avatar, linked accounts | api | free | ☐ |

**Phone** (`collectors/phone/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| ignorant | account existence (IG/Amazon/Snapchat) | cli | free | ☐ |
| phoneinfoga | footprint, carrier, reputation | cli | free | ☐ |
| numverify | carrier, line type, country | api | freemium | ☐ |
| truecaller | name lookup (login-gated) | scrape | free | ☐ |

**Identity linking** (`collectors/identity/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| keybase | cryptographically linked accounts | api | free | ☐ |
| linktree | bio link hubs → all profiles | scrape | free | ☐ |

### Wave 3 — Infrastructure

**Network / DNS** (`collectors/infra/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| shodan | exposed hosts, services, banners | api | freemium | ☐ |
| censys | hosts, certs, services | api | freemium | ☐ |
| urlscan | URL scans, screenshots, related domains | api | free | ☐ |
| securitytrails | passive DNS, subdomain history | api | freemium | ☐ |
| otx | passive DNS, threat indicators | api | free | ☐ |
| dnsdumpster | subdomains, DNS records | scrape/api | free | ☐ |
| bgp_he | ASN, BGP, IP ranges | scrape | free | ☐ |
| viewdns | DNS/IP lookups | scrape/api | freemium | ☐ |
| ipinfo | geo-IP, ASN, hosting | api | freemium | ☐ |
| abuseipdb | IP reputation | api | free | ☐ |
| builtwith | tech stack | scrape/api | freemium | ☐ |
| publicwww | source-code / tracker-ID search | scrape/api | freemium | ☐ |
| greynoise | host & exposure intel | api | freemium | ☐ |

**Certificates** (`collectors/certs/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| crtsh | CT logs → subdomains, related domains | api | free | ☐ |
| certspotter | CT log monitoring | api | free | ☐ |
| censys_certs | certificate search | api | freemium | ☐ |

**Breach / leak (free)** (`collectors/breach/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| intelx | leaks, pastes, dark-web index | api | freemium | ☐ |

**Paste sites** (`collectors/paste/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| pastebin | leaked data, dumps | scrape | free | ☐ |
| github_gists | code, secrets, emails | api | free | ☐ |
| ghostbin | pasted content | scrape | free | ☐ |

### Wave 4 — Records

**Sanctions / PEP** (`collectors/sanctions/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| opensanctions | OFAC/UN/EU/Interpol + PEP, aggregated | api | free | ☐ |
| ofac_sdn | US sanctions list | api | free | ☐ |
| un_eu_lists | UN / EU consolidated lists | dataset | free | ☐ |
| interpol | Red Notices | api/scrape | free | ☐ |
| aleph | OCCRP investigative docs, leaks | api | free | ☐ |
| offshoreleaks | ICIJ offshore entities & officers | scrape | free | ☐ |
| littlesis | power/relationship networks | api | free | ☐ |

**Corporate** (`collectors/corporate/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| opencorporates | global companies, officers, jurisdictions | api | freemium | ☐ |
| companies_house | UK officers, filings, addresses | api | free | ☐ |
| sec_edgar | US filings, execs, insiders (full-text) | api | free | ☐ |
| gleif | legal entity identifiers (LEI) | api | free | ☐ |
| eu_bris | EU company data | scrape | free | ☐ |

**Court / legal** (`collectors/legal/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| courtlistener | US dockets, opinions, parties (RECAP) | api | free | ☐ |
| state_courts | US state case records | scrape | free | ☐ |
| property_records | ownership, addresses | scrape | free | ☐ |
| voter_records | name, address, party (select US states) | scrape | free | ☐ |
| gazettes | gov notices, registrations | scrape | free | ☐ |

### Wave 5 — Footprint

**Social** (`collectors/social/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| reddit | user post/comment history, subs | api/scrape | free | ☐ |
| telegram | public channels, groups, members | api | free | ☐ |
| bluesky | public posts, profiles, follows | api | free | ☐ |
| mastodon | public posts, profiles | api | free | ☐ |
| youtube | channels, videos, comments | api | free | ☐ |
| vk | profiles, posts, connections | api/scrape | free | ☐ |
| flickr | photos + geotags, profiles | api | free | ☐ |
| pinterest | boards, pins | scrape | free | ☐ |
| tumblr | blogs, posts | api | free | ☐ |
| twitch | profiles, clips | api | free | ☐ |
| soundcloud | profiles, tracks | scrape/api | free | ☐ |
| strava | activity, segments, geolocation | scrape | free | ☐ |
| goodreads | reading / film history | scrape | free | ☐ |

**Code / developer** (`collectors/code/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| github | users, code, commits, leaked emails | api | free | ☐ |
| gitlab | users, repos, commits | api | free | ☐ |
| bitbucket | users, repos | api | free | ☐ |
| stackexchange | profiles, activity | api | free | ☐ |
| pypi_npm | package maintainer emails | api/scrape | free | ☐ |
| dockerhub | images, users | api | free | ☐ |
| grepapp | cross-repo code search | scrape/api | free | ☐ |

**News** (`collectors/news/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| gdelt | global news mentions | api | free | ☐ |
| google_news | news articles | scrape | free | ☐ |
| mediacloud | media coverage analysis | api | free | ☐ |
| rss | publisher feeds | fetch | free | ☐ |

**Academic / patents** (`collectors/academic/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| orcid | researcher IDs, affiliations | api | free | ☐ |
| semantic_scholar | papers, authors, citations | api | free | ☐ |
| arxiv | preprints | api | free | ☐ |
| pubmed | biomedical papers | api | free | ☐ |
| google_scholar | papers, citations, profiles | scrape | free | ☐ |
| patents | Google Patents / USPTO / Espacenet | scrape/api | free | ☐ |

### Wave 6 — Specialized

**Images / reverse image** (`collectors/images/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| yandex_images | reverse image match (best) | crawl | free | ☐ |
| google_lens | reverse image match | crawl | free | ☐ |
| bing_visual | reverse image match | api/scrape | freemium | ☐ |
| tineye | reverse image match | api/scrape | freemium | ☐ |
| exif | camera, GPS, timestamps from images | local lib | free | ☐ |

**Geolocation / maps** (`collectors/geo/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| google_maps | places, reviewer identities | scrape/api | freemium | ☐ |
| osm_nominatim | geocoding, place data | api | free | ☐ |
| wikimapia | annotated places | scrape | free | ☐ |
| foursquare | places, check-ins | api | freemium | ☐ |

**Crypto / blockchain** (`collectors/crypto/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| etherscan | ETH addresses, transactions | api | free | ☐ |
| blockchain_com | BTC explorer | api | free | ☐ |
| blockchair | multi-chain explorer | api | freemium | ☐ |
| arkham | wallet → entity tagging | scrape/api | freemium | ☐ |
| wallet_explorer | wallet clustering | scrape | free | ☐ |
| opensea | NFT holdings → wallets | api | free | ☐ |

**People-search (free tier)** (`collectors/people/`)

| Source | Yields | Type | Tier | Status |
|---|---|---|---|---|
| truepeoplesearch | name, address, phone, relatives | scrape | free | ☐ |
| fastpeoplesearch | name, address, phone, relatives | scrape | free | ☐ |
| thatsthem | reverse phone/email/address | scrape/api | freemium | ☐ |
| radaris_peekyou | aggregated profiles | scrape | freemium | ☐ |

### Frameworks to integrate (`collectors/frameworks/`)

| Source | Role | Type | Tier | Status |
|---|---|---|---|---|
| theharvester | emails, subdomains, names from many sources | cli | free | ☐ |
| spiderfoot | 200+ modules; mine module list as superset | cli/api | free | ☐ |
| reconng | modular recon framework | cli | free | ☐ |

---

# STAGE 2 — PAID SOURCES (enable after Stage 1)

Built/enabled only once Stage 1 is complete. Each lives in its category folder with
`tier = "paid"`, disabled by default. The **free alternative** (already shipped in
Stage 1) is noted so skipping any paid source blocks nothing.

**Breach / leak** (`collectors/breach/`)

| Source | Yields | Cost | Free alternative | Status |
|---|---|---|---|---|
| hibp | breaches per email | $ (~$4/mo) | intelx + paste sites | ☐ |
| dehashed | breach records incl. plaintext creds | $$ | intelx | ☐ |
| leakcheck | breach records | $$ | intelx | ☐ |
| snusbase | breach records | $$ | intelx | ☐ |

**Corporate** (`collectors/corporate/`)

| Source | Yields | Cost | Free alternative | Status |
|---|---|---|---|---|
| crunchbase | startups, funding, people | $$$ | opencorporates, sec_edgar, littlesis | ☐ |

**Court / legal** (`collectors/legal/`)

| Source | Yields | Cost | Free alternative | Status |
|---|---|---|---|---|
| pacer | US federal court records | $ (per-page) | courtlistener (RECAP) | ☐ |

**Images / faces** (`collectors/images/`)

| Source | Yields | Cost | Free alternative | Status |
|---|---|---|---|---|
| facecheck | face search across web | $$ | yandex_images / google_lens | ☐ |
| pimeyes | face search across web | $$$ | yandex_images / google_lens | ☐ |

**People-search (paywalled)** (`collectors/people/`)

| Source | Yields | Cost | Free alternative | Status |
|---|---|---|---|---|
| spokeo | aggregated person profiles | $$ | truepeoplesearch, fastpeoplesearch | ☐ |
| beenverified | aggregated profiles, records | $$ | truepeoplesearch, thatsthem | ☐ |
| whitepages | reverse lookups, background | $$ | truepeoplesearch, thatsthem | ☐ |

**Due-diligence (enterprise)** (`collectors/sanctions/`)

| Source | Yields | Cost | Free alternative | Status |
|---|---|---|---|---|
| world_check | PEP / sanctions / risk profiles | $$$ | opensanctions | ☐ |
| dowjones | PEP / sanctions / adverse media | $$$ | opensanctions + scraped news | ☐ |

---

## Excluded — never crawled directly

| Site | Reason |
|---|---|
| LinkedIn | Login wall + aggressive anti-bot + legal exposure |
| Instagram / Facebook | Login wall + account bans + legal restrictions |
| TikTok | Signed-request anti-bot; brittle |
| X / Twitter | Login required to view; viable access is paid-only |

> Picked up only as **mentions in scraped search snippets / third-party pages**, never crawled directly.

---

## First runnable slice (product spine)

Build this end-to-end first, then layer sources on:
Phase 0 + Phase 1 **DuckDuckGo** + Phase 2 **page reader & extractor** +
Phase 4 **aggregator** + Phase 5 **map-reduce report** + Phase 6 **pipeline & API**.
Once search → crawl → report runs clean, add free collectors wave by wave (W1→W6),
then unlock Stage 2 paid sources as needed.
