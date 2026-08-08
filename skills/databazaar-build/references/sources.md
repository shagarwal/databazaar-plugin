# Source Adapters

Each adapter implements a single interface:

```python
class Adapter:
    name: str
    priority: int  # lower = earlier in fallback chain

    def can_handle(self, request: DataRequest) -> float:
        """Confidence 0-1 that this adapter can satisfy the request."""

    def fetch(self, request: DataRequest) -> AdapterResult:
        """Returns rows + per-row provenance metadata."""
```

## Adapters (priority order)

The **Status** column tracks operational reality — sources die, get retired,
or rate-limit hard. Always set `--allow-broken` to bypass the disabled-status
guard if you're testing a recovery; otherwise the build script skips disabled
adapters silently. Verified-on dates should be re-stamped after any
successful fetch in evals/CI.

| # | Name | Module | Auth | Status | Verified | Notes |
|---|---|---|---|---|---|---|
| 1 | databazaar | `adapters/databazaar.py` | optional API key | ✅ live | 2026-05-07 | Always tried first. Branches on mirrored vs federated — see `databazaar-api.md` for the manifest/passthrough flow added 2026-05-07. |
| 2 | huggingface | `adapters/huggingface.py` | optional HF token | ✅ live | 2026-05-07 | `datasets-server.huggingface.co/parquet` for direct parquet access; falls back to `datasets` lib for non-parquet. See `hf-picker.md` for shard / mirror-vs-federate decision logic borrowed from `databazaar-discovery`. |
| 3 | kaggle | `adapters/kaggle.py` | Kaggle API token | ✅ live | 2026-04-15 | Public datasets only. |
| 4 | world_bank | `adapters/world_bank.py` | none | ✅ live | 2026-04-30 | Indicators API; covers ~30% of databazaar's existing country-panel listings. |
| 5 | data_gov | `adapters/data_gov.py` | none | ⛔ **DISABLED** | 2026-04-30 | CKAN catalog API was retired in 2025. The discovery pipeline learned this and disabled its data.gov connector ([commit b822094](https://github.com/shagarwal/agentdatamarketplace/commit/b822094)). Use catalog.data.gov direct dataset URLs via `web_fetch` until a replacement lands. |
| 6 | wikidata | `adapters/wikidata.py` | none | ✅ live | 2026-04-15 | SPARQL. Best for entity lists with structured properties. |
| 7 | usgs | `adapters/usgs.py` | none | ✅ live | 2026-04-15 | Earthquakes, geo. |
| 8 | noaa | `adapters/noaa.py` | optional token | ✅ live | 2026-04-15 | Weather, climate. |
| 9 | nasa | `adapters/nasa.py` | optional API key | ✅ live | 2026-04-15 | Exoplanets, imagery metadata. |
| 10 | arxiv | `adapters/arxiv.py` | none | ✅ live | 2026-04-15 | Paper metadata. |
| 11 | github | `adapters/github.py` | optional token (rate limit) | ✅ live | 2026-04-15 | Repo lists, issues. |
| 12 | sec_edgar | `adapters/sec_edgar.py` | none | ✅ live | 2026-04-15 | Filings. Per the SEC's data ToS, set `User-Agent: <name> <email>` or you'll be 403'd. |
| 13 | web_fetch | `adapters/web_fetch.py` | none | ✅ live | 2026-04-15 | LAST RESORT. Robots.txt + rate-limit + ToS allowlist + reachability rule enforced (treat 429/503 as ambiguous — see `gotchas.md`). |
| — | common-crawl | (no adapter) | — | ⛔ never enabled | — | The discovery pipeline tried this; CDX API doesn't support path globs needed for targeted dataset lookups ([commit d41413b](https://github.com/shagarwal/agentdatamarketplace/commit/d41413b)). Don't reach for it. |

## Routing logic

1. Always run `databazaar.can_handle()` first.
2. If confidence ≥ 0.8 → use only databazaar.
3. Else gather all adapters with `can_handle() ≥ 0.3` and fan out in parallel,
   capped at 4 concurrent.
4. Merge results in `aggregate` step.
5. If zero adapters return data → return `NoDataError` with the request echoed
   back; do NOT fabricate.

## Adding a new adapter

1. Create `scripts/adapters/<name>.py` implementing the interface.
2. Register in `scripts/adapters/__init__.py`.
3. Add a fixture under `evals/fixtures/<name>/` with at least one cached
   response.
4. Add at least one eval case exercising it.
5. Add a row to the Adapters table above with status=✅ live and today's
   verified date.

## Disabled-adapter discipline

Sources die. data.gov retired CKAN; common-crawl's CDX never supported
path-glob queries. The sibling `databazaar-discovery` skill maintains a
running connector status table in `apps/discovery/RUNBOOK.md` because half
the operational scar tissue in dataset acquisition is "this source no
longer responds the way the docs claim".

Carrying that discipline here:

- Each row in the Adapters table has a **Status** + **Verified** pair.
- The build orchestrator should skip adapters with status=⛔ silently rather
  than retry-and-fail on every invocation. Burning user time on dead
  endpoints is worse than an honest "no adapter satisfied the request".
- After a successful eval run, bump the Verified date for adapters that
  fired. After a failure that turns out to be a permanent retirement (not a
  transient outage), flip the Status to ⛔ with a one-line reason and a
  pointer to the discovery commit that disabled the equivalent connector
  (if applicable).
- A weekly job should re-verify all ✅ adapters via fixture replay; entries
  with `Verified` older than ~30 days are stale and should produce a
  warning when planning a fanout.

## Web fetch ToS allowlist

`web_fetch` is the only adapter with discretion to scrape arbitrary URLs.
Hard-coded denylist (refuse + flag):

- linkedin.com (ToS)
- facebook.com / instagram.com (auth-walled)
- *.wsj.com / *.nytimes.com / *.ft.com (paywall)
- twitter.com / x.com (auth-walled)
- glassdoor.com (ToS)
- zillow.com (ToS aggregation clause)

Allowlist behavior: respect robots.txt, max 1 req/sec/host, max 1k pages/run,
User-Agent identifies the skill + a contact URL.
