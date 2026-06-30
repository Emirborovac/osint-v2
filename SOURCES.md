# OSINT V2 — Source Catalog

The complete list of sources the engine collects from. This is the product scope,
not an MVP subset.

**Two collection modes:**
- **Discovery + deep crawl** (source-agnostic) — scrapes search engines, then crawls
  *any* page they surface. Covers all general/unstructured web content with no
  per-site code.
- **Targeted collectors** (below) — reach structured data and deep-web sources that
  general search can't: registries, DNS, breach DBs, archives, specialized indexes.

**Legend**
- **Method:** `scrape` (HTML) · `crawl` (browser/crawl4ai) · `api` (JSON) · `cli` (local tool) · `socket` · `dataset` (bulk)
- **Auth:** none · free key · paid key · token · login · phone
- **Cost:** free · freemium · paid
- **Anti-bot:** low / med / high / — (n/a for APIs)

---

## 1. Search engines — discovery layer (scraped, pages 1–5)

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| DuckDuckGo (HTML) | result links, titles, snippets | scrape | none | free | low |
| Bing | result links, snippets | scrape | none | free | med |
| Google | result links, snippets | crawl (stealth+proxy) | none | free | high |
| Yandex | result links + image index | crawl (stealth+proxy) | none | free | high |
| Startpage | result links | scrape | none | free | med |
| Brave Search (frontend) | result links | scrape | none | free | med |
| Mojeek | result links | scrape | none | free | low |
| SearXNG (self-hosted) | aggregated links | api/scrape | none | free | low |

## 2. Web archives — historical & deleted content

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Wayback Machine (archive.org) | historical snapshots, deleted pages | api (CDX) + scrape | none | free | low |
| archive.today | snapshots | scrape | none | free | med |
| Common Crawl | bulk historical web index | api/dataset | none | free | — |

## 3. Username enumeration

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Sherlock | accounts across ~400 sites | cli | none | free | — |
| Maigret | accounts across ~3000 sites (richer) | cli | none | free | — |
| WhatsMyName | curated account check | api/dataset | none | free | — |
| Blackbird | account check | cli | none | free | — |
| Socialscan / Namechk | username availability | scrape/cli | none | free | med |

## 4. Email intelligence

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Holehe | account existence ~120 sites | cli | none | free | — |
| EmailRep.io | reputation, linked profiles | api | free key | free | — |
| Epieos | Google account, linked services | scrape/api | none | freemium | med |
| Hunter.io | verification, domain pattern | api | paid key | freemium | — |
| Gravatar | profile, avatar, linked accounts | api | none | free | — |
| Have I Been Pwned | breaches for email | api | paid key | paid (cheap) | — |

## 5. Phone intelligence

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Ignorant | account existence (IG/Amazon/Snapchat) | cli | none | free | — |
| PhoneInfoga | footprint, carrier, reputation | cli/scrape | none | free | — |
| NumVerify | carrier, line type, country | api | free key | freemium | — |
| Truecaller | name lookup | scrape | login | free | high |

## 6. Breach / leak data

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Have I Been Pwned | breach list | api | paid key | paid (cheap) | — |
| Intelligence X (IntelX) | leaks, pastes, dark-web index | api | free/paid key | freemium | — |
| DeHashed | breach records (creds, PII) | api | paid key | paid | — |
| LeakCheck | breach records | api | paid key | paid | — |
| Snusbase | breach records | api | paid key | paid | — |

## 7. Paste sites

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Pastebin | leaked data, dumps | scrape | none | free | med |
| GitHub Gists | code, secrets, emails | api | token | free | — |
| Ghostbin / Rentry / Throwbin | pasted content | scrape | none | free | low |

## 8. Infrastructure / DNS / network

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Shodan | exposed hosts, services, banners | api | paid key | freemium | — |
| Censys | hosts, certs, services | api | free key | freemium | — |
| urlscan.io | URL scans, screenshots, related domains | api | free key | free | — |
| SecurityTrails | passive DNS, subdomain history | api | free key | freemium | — |
| AlienVault OTX | passive DNS, threat indicators | api | free key | free | — |
| DNSdumpster / RapidDNS | subdomains, DNS records | scrape/api | none | free | low |
| bgp.he.net (Hurricane Electric) | ASN, BGP, IP ranges | scrape | none | free | low |
| ViewDNS.info | DNS/IP lookups | scrape/api | optional | freemium | low |
| IPinfo / ipdata | geo-IP, ASN, hosting | api | free key | freemium | — |
| AbuseIPDB | IP reputation | api | free key | free | — |
| BuiltWith / Wappalyzer | tech stack | scrape/api | optional | freemium | low |
| PublicWWW | source-code / tracker-ID search | scrape/api | optional | freemium | med |
| GreyNoise / Onyphe / BinaryEdge / FOFA / ZoomEye | host & exposure intel | api | key | freemium | — |

## 9. Certificates

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| crt.sh | CT logs → subdomains, related domains | api (JSON) | none | free | — |
| CertSpotter | CT log monitoring | api | free key | free | — |
| Censys certs | certificate search | api | free key | freemium | — |

## 10. Sanctions / PEP / due-diligence

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| OpenSanctions | OFAC/UN/EU/Interpol + PEP, aggregated | api/dataset | none | free | — |
| OFAC SDN | US sanctions list | dataset/api | none | free | — |
| UN / EU consolidated lists | sanctions | dataset | none | free | — |
| Interpol Red Notices | wanted persons | api/scrape | none | free | low |
| OCCRP Aleph | investigative docs, leaks, entities | api | free key | free | — |
| ICIJ OffshoreLeaks | offshore entities & officers | scrape/dataset | none | free | low |
| LittleSis | power/relationship networks | api | none | free | — |

## 11. Corporate / business registries

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| OpenCorporates | global companies, officers, jurisdictions | api | free key | freemium | — |
| Companies House (UK) | officers, filings, addresses | api | free key | free | — |
| SEC EDGAR | US filings, execs, insiders (full-text) | api | none | free | — |
| GLEIF (LEI) | legal entity identifiers | api | none | free | — |
| EU Business Registers (BRIS) | EU company data | scrape | none | free | med |
| Crunchbase | startups, funding, people | api | paid key | paid | — |

## 12. Court / legal / public records

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| CourtListener / RECAP | US dockets, opinions, parties | api | free key | free | — |
| US state court portals | case records | scrape | varies | free | high |
| Property / land records | ownership, addresses | scrape | varies | free | high |
| Voter records (select US states) | name, address, party | scrape/dataset | varies | free | med |
| Government gazettes / official journals | notices, registrations | scrape | none | free | low |

## 13. Social media — non-walled / scrapeable

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Reddit | user post/comment history, subs | api/scrape | token | free | low |
| Telegram | public channels, groups, members | api (Telethon) | phone | free | med |
| Bluesky | public posts, profiles, follows | api (AT proto) | none | free | — |
| Mastodon / Fediverse | public posts, profiles | api | none | free | low |
| YouTube | channels, videos, comments | api | free key | free | — |
| VK | profiles, posts, connections | api/scrape | token | free | med |
| Flickr | photos + geotags, profiles | api | free key | free | — |
| Pinterest | boards, pins | scrape | none | free | med |
| Tumblr | blogs, posts | api | free key | free | — |
| Twitch | profiles, clips | api | free key | free | — |
| SoundCloud | profiles, tracks | scrape/api | optional | free | med |
| Strava | activity, segments, geolocation | scrape | login | free | high |
| Goodreads / Letterboxd | reading / film history | scrape | none | free | low |

## 14. Code / developer

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| GitHub | users, code, commits, leaked emails | api | token | free | — |
| GitLab | users, repos, commits | api | token | free | — |
| Bitbucket | users, repos | api | token | free | — |
| Stack Exchange / Stack Overflow | profiles, activity | api | free key | free | — |
| PyPI / npm | package maintainer emails | api/scrape | none | free | — |
| Docker Hub | images, users | api | none | free | — |
| grep.app / Sourcegraph | cross-repo code search | scrape/api | optional | free | low |

## 15. News / media

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| GDELT | global news mentions | api | none | free | — |
| Google News / Bing News | news articles | scrape | none | free | med |
| MediaCloud | media coverage analysis | api | free key | free | — |
| RSS / Atom feeds | publisher feeds | fetch | none | free | low |

## 16. Academic / patents

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| ORCID | researcher IDs, affiliations | api | none | free | — |
| Semantic Scholar | papers, authors, citations | api | free key | free | — |
| arXiv | preprints | api | none | free | — |
| PubMed | biomedical papers | api | none | free | — |
| Google Scholar | papers, citations, profiles | scrape | none | free | high |
| Google Patents / USPTO / Espacenet | patents, inventors, assignees | scrape/api | none | free | med |

## 17. Images / faces / reverse image

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Yandex Images | reverse image match (best) | crawl | none | free | high |
| Google Images / Lens | reverse image match | crawl | none | free | high |
| Bing Visual Search | reverse image match | api/scrape | key | freemium | — |
| TinEye | reverse image match | api/scrape | key | freemium | low |
| FaceCheck.id | face search across web | scrape/api | key | paid | med |
| EXIF extraction | camera, GPS, timestamps from images | local lib | none | free | — |

> Face-search tools (FaceCheck, PimEyes) carry legal/ethics constraints — gate behind explicit authorization.

## 18. Geolocation / maps

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Google Maps / reviews / Street View | places, reviewer identities | scrape/api | optional | freemium | high |
| OpenStreetMap / Nominatim | geocoding, place data | api | none | free | — |
| Wikimapia | annotated places | scrape | none | free | low |
| Foursquare / Swarm | places, check-ins | api | key | freemium | — |

## 19. Crypto / blockchain

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Etherscan | ETH addresses, transactions | api | free key | free | — |
| Blockchain.com | BTC explorer | api | none | free | — |
| Blockchair | multi-chain explorer | api | optional key | freemium | — |
| Arkham | wallet → entity tagging | scrape/api | optional | freemium | med |
| Wallet Explorer | wallet clustering | scrape | none | free | low |
| OpenSea | NFT holdings → wallets | api | key | free | — |

## 20. People-search aggregators (US-centric)

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| TruePeopleSearch | name, address, phone, relatives | scrape | none | free | high |
| FastPeopleSearch | name, address, phone, relatives | scrape | none | free | high |
| ThatsThem | reverse phone/email/address | scrape/api | optional | freemium | high |
| Radaris / PeekYou | aggregated profiles | scrape | none | freemium | high |
| Spokeo / BeenVerified / Whitepages | aggregated profiles (paywalled) | scrape | login | paid | high |

## 21. Identity linking / bio aggregators

| Source | Yields | Method | Auth | Cost | Anti-bot |
|---|---|---|---|---|---|
| Keybase | cryptographically linked accounts | api | none | free | — |
| Gravatar | email → profile, linked accounts | api | none | free | — |
| Linktree / About.me / Carrd | bio link hubs → all profiles | scrape | none | free | low |

## 22. Frameworks to integrate (don't rebuild)

| Tool | Role | Method |
|---|---|---|
| Sherlock / Holehe / Ignorant | username/email/phone account existence | cli (already used in V1) |
| Maigret | broad username enumeration | cli |
| theHarvester | emails, subdomains, names from many sources | cli |
| SpiderFoot | 200+ modules; mine its module list as the canonical superset | cli/api |
| recon-ng | modular recon framework | cli |
| PhoneInfoga | phone footprinting | cli |

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

## Build waves (suggested order)

| Wave | Categories |
|---|---|
| W1 — Spine | 1 Search · 2 Archives · deep-crawl core |
| W2 — Identity | 3 Username · 4 Email · 5 Phone · 21 Identity linking |
| W3 — Infra | 8 Network/DNS · 9 Certificates · 6 Breach · 7 Pastes |
| W4 — Records | 10 Sanctions · 11 Corporate · 12 Court/legal |
| W5 — Footprint | 13 Social · 14 Code · 15 News · 16 Academic |
| W6 — Specialized | 17 Images/face · 18 Geo · 19 Crypto · 20 People-search |
