# OSINT V2 — Paid Source Catalog

Sources that **require payment to use at all** (even if cheap). We do **not** build
these first — the free catalog ([FREE-SOURCES.md](FREE-SOURCES.md)) covers the same
intelligence types. Each paid source below lists the **free alternative** already in
scope, so nothing is blocked by skipping it.

Add a paid source only when its free alternative proves insufficient for a real case.

**Cost tiers:** `$` cheap (<$10/mo) · `$$` moderate · `$$$` expensive / enterprise

---

## Breach / leak data

| Source | Yields | Cost | Free alternative (already in scope) |
|---|---|---|---|
| Have I Been Pwned (API) | breaches per email | `$` (~$4/mo) | IntelX free tier + paste sites |
| DeHashed | breach records incl. plaintext creds, PII | `$$` | IntelX free tier; HIBP if added |
| LeakCheck | breach records | `$$` | IntelX free tier |
| Snusbase | breach records | `$$` | IntelX free tier |

## Corporate / business

| Source | Yields | Cost | Free alternative (already in scope) |
|---|---|---|---|
| Crunchbase | startups, funding rounds, people | `$$$` | OpenCorporates, SEC EDGAR, LittleSis |

## Images / faces

| Source | Yields | Cost | Free alternative (already in scope) |
|---|---|---|---|
| FaceCheck.id | face search across the web | `$$` | Yandex / Google reverse image |
| PimEyes | face search across the web | `$$$` | Yandex / Google reverse image |

> Face-search engines also carry legal/ethics constraints — gate behind explicit authorization regardless of cost.

## People-search aggregators (paywalled)

| Source | Yields | Cost | Free alternative (already in scope) |
|---|---|---|---|
| Spokeo | aggregated person profiles | `$$` | TruePeopleSearch, FastPeopleSearch |
| BeenVerified | aggregated person profiles, records | `$$` | TruePeopleSearch, ThatsThem |
| Whitepages Premium | reverse lookups, background | `$$` | TruePeopleSearch, ThatsThem |

## Court / legal

| Source | Yields | Cost | Free alternative (already in scope) |
|---|---|---|---|
| PACER | US federal court records | `$` (per-page) | CourtListener / RECAP (free mirror of PACER) |

## Due-diligence / sanctions (enterprise)

| Source | Yields | Cost | Free alternative (already in scope) |
|---|---|---|---|
| World-Check (Refinitiv) | PEP / sanctions / risk profiles | `$$$` | OpenSanctions (free, aggregates OFAC/UN/EU/Interpol) |
| Dow Jones Risk & Compliance | PEP / sanctions / adverse media | `$$$` | OpenSanctions + scraped adverse-media news |

---

## Note on "freemium" sources

Sources like Shodan, Censys, SecurityTrails, Hunter, IntelX, OpenCorporates and the
host-intel engines have **usable free tiers** — they live in
[FREE-SOURCES.md](FREE-SOURCES.md) and we start with those tiers. They only become a
paid line item if/when query volume exceeds the free quota. Revisit them here only
when we actually hit those limits.
