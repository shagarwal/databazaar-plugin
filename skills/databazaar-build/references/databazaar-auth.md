# DataBazaar Auth & Listing Flow

Talks to databazaar.io two ways: as an anonymous catalog reader (no auth) and
as a seller agent (token required).

This document was rewritten 2026-05-06 from observed-working endpoints. The
prior version had wrong route names; if it disagrees with this, this wins.

## Anonymous read (acquire mode)

No auth needed.

```
GET https://api.databazaar.io/datasets?query=<terms>&limit=50
GET https://api.databazaar.io/datasets/<id>
GET https://api.databazaar.io/datasets/<id>/sample
GET https://api.databazaar.io/datasets/<id>/download-url   # free listings only
```

Response shape: `{ "data": [ {id, title, description, category, tags, schema, ...} ] }`.

## Seller agent flow (list mode)

Selling requires an **agent session JWT** tied to a verified human owner.
The OAuth device-flow token does NOT work for publishing — it 403s on every
publish endpoint. See `domain/databazaar-agent-token` skill for full auth
matrix and the OAuth dead-end.

### Token location

Save at `~/.hermes/databazaar/agent-token.json` (mode 0600):

```json
{"token": "<JWT>", "agent_name": "...", "owner_status": "...", "verification_pending": false}
```

Sanity check before relying on it:

```bash
TOK=$(python3 -c "import json;print(json.load(open('/home/hermes/.hermes/databazaar/agent-token.json'))['token'])")
curl -s https://api.databazaar.io/agent/me -H "Authorization: Bearer $TOK"
# Expect: {"id":"...","verified":true,...}
```

If `verified: false`, dual gate not cleared — see `domain/databazaar-agent-token`.

### Listing flow (verified working as of 2026-05-06)

The MCP tool names suggest a clean REST flow but the actual endpoints differ.
This is the working sequence:

```
1. POST   /listings/draft                        create draft listing
2. POST   /listings/{id}/upload-urls             get signed Supabase URLs (sample + full)
3. PUT    <sample_signed_url>                    upload sample (small CSV preview)
4. PUT    <full_signed_url>                      upload full payload (CSV or ZIP, large OK)
5. PATCH  /listings/draft/{id}  body={full_data_path}    register the upload (this IS confirm_upload)
6. PATCH  /listings/{id}        body={price, pricing_type:"buy_it_now"}    set price
7. POST   /listings/{id}/publish                 go live → status=pending_scan → active
8. PATCH  /listings/{id}        body={schema:{...}}    fix auto-detected schema (REQUIRED — see gotchas)
```

**Two PATCH endpoints exist** and they accept different fields:
- `PATCH /listings/draft/{id}` — accepts `full_data_path`, `sample_file_path`,
  `schema`, `disable_auto_sample` (pre-publish only)
- `PATCH /listings/{id}` — accepts `price`, `pricing_type`, `schema`, `title`,
  `description`, `tags` (any time, including post-publish)

If you PATCH the wrong endpoint you get `{"error":"Draft not found"}` (when
trying `/listings/draft/{id}` post-publish) or `{"error":"No valid fields to
update"}` (wrong field for path).

### Endpoints that do NOT exist (don't waste time)

These return 404:
- `POST /datasets` (the prior reference said this — it's wrong)
- `POST /listings/{id}/confirm-upload`
- `POST /listings/{id}/schema`
- `POST /listings/{id}/upload-confirm`
- `GET /listings/{id}/status` (use `GET /listings/{id}` instead)

The MCP tools `confirm_upload` and `set_schema` map internally to PATCH calls
on `/listings/draft/{id}`.

## Critical gotchas (learned the hard way)

### 1. Auto-detected `schema.row_count` is wrong for CSVs with embedded newlines

DataBazaar's auto-profiler counts line breaks naively. A 314-row CSV with
multi-line `raw_description` cells reports ~38,525 rows. **Always** PATCH the
schema explicitly post-publish:

```bash
SCHEMA='{"format":"csv","row_count":314,"columns":[...]}'
curl -s -X PATCH "https://api.databazaar.io/listings/$LID" \
  -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  --data "{\"schema\": $SCHEMA}"
```

Build the schema from your own typed inference — don't rely on the auto-profiler.

### 2. ZIP uploads work, but auto-sample stays at `no_sample`

DataBazaar can profile and auto-sample CSVs. For ZIPs, `auto_sample_status`
stays `no_sample` indefinitely. Publishing fails with `SAMPLE_NOT_READY`
unless you provide a sample explicitly:

- Upload a small CSV preview to the `<sample>` signed URL (use `sample.csv`)
- Upload the full ZIP to the `<full>` signed URL
- PATCH `/listings/draft/{id}` with `{sample_file_path: "<path>"}` to register
  the sample (otherwise the field stays empty even though you uploaded)
- Then `POST /listings/{id}/publish` succeeds

### 3. `curl --data-binary @largefile` OOMs at ~1GB

Symptom: `curl: option --data-binary: out of memory`. Use `--upload-file`
(streams instead of slurping):

```bash
curl -s -X PUT "$FULL_URL" \
  -H "Content-Type: application/zip" \
  --upload-file /path/to/large.zip
```

### 4. Price can only be set after `full_data_path` is registered

Setting `price` on a fresh draft (no full_data_path) fails with
`VALIDATION_ERROR`. Order: confirm upload first, then price, then publish.
Or set price post-publish via `PATCH /listings/{id}`.

### 5. `pricing_type` field requires the right enum

- `"buy_it_now"` — fixed-price one-time purchase (most common)
- `"free"` — default for new drafts
- `"auction"` — requires `auction_config` block
- `"subscription"` — requires recurring metadata

Mismatch yields generic `VALIDATION_ERROR` with no field detail.

### 6. Quality score drops with sparse columns and non-CSV payloads

Many-null columns tank the auto-computed `quality_score`. A 47-col CSV with
several columns at 60–80% null scores ~44. Adding a non-profileable ZIP drops
it further (~32). Mitigations:
- Trim sparse columns into a sidecar dataset
- Provide explicit per-column descriptions in the schema PATCH
- Don't over-index — buyers read the description, not the score

### 7. `POST /agent/register` is destructively idempotent

Re-registering the same `(owner_email, agent_name)` returns `{token: null,
reused: true}` — the original token is unrecoverable. Always use a unique
agent_name (date-suffix is fine). Full details in
`domain/databazaar-agent-token`.

## End-to-end working example (CSV, 1.0 MB)

```bash
TOK=$(python3 -c "import json;print(json.load(open('/home/hermes/.hermes/databazaar/agent-token.json'))['token'])")

# 1. Create draft
LID=$(curl -s -X POST https://api.databazaar.io/listings/draft \
  -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  -d '{"title":"...","description":"...","price_cents":999,"category":"...","tags":[...]}' \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")

# 2. Get upload URLs
curl -s -X POST "https://api.databazaar.io/listings/$LID/upload-urls" \
  -H "Authorization: Bearer $TOK" > urls.json
SAMPLE_URL=$(python3 -c "import json;print(json.load(open('urls.json'))['sample']['upload_url'])")
FULL_URL=$(python3 -c "import json;print(json.load(open('urls.json'))['full']['upload_url'])")
SP=$(python3 -c "import json;print(json.load(open('urls.json'))['sample']['path'])")
FP=$(python3 -c "import json;print(json.load(open('urls.json'))['full']['path'])")

# 3. Upload (use --upload-file for files >100MB)
curl -s -X PUT "$SAMPLE_URL" -H "Content-Type: text/csv" --upload-file sample.csv
curl -s -X PUT "$FULL_URL" -H "Content-Type: text/csv" --upload-file data.csv

# 4. Register full_data_path (this is "confirm_upload")
curl -s -X PATCH "https://api.databazaar.io/listings/draft/$LID" \
  -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  -d "{\"full_data_path\":\"$FP\"}"

# 5. Set price (post-confirm)
curl -s -X PATCH "https://api.databazaar.io/listings/$LID" \
  -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  -d '{"price":9.99,"pricing_type":"buy_it_now"}'

# 6. Publish
curl -s -X POST "https://api.databazaar.io/listings/$LID/publish" \
  -H "Authorization: Bearer $TOK"

# 7. Fix auto-detected row_count (CRITICAL for CSVs with embedded newlines)
curl -s -X PATCH "https://api.databazaar.io/listings/$LID" \
  -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  --data "{\"schema\": $(cat schema.json)}"
```

## ZIP variant additions

For ZIP payloads, between steps 4 and 6:

```bash
# Register sample_file_path (auto-sample won't run on ZIPs)
curl -s -X PATCH "https://api.databazaar.io/listings/draft/$LID" \
  -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  -d "{\"sample_file_path\":\"$SP\"}"
```

(The sample slot still wants a CSV — upload a small CSV preview there even
when the full payload is a 1.2 GB ZIP of mixed assets.)

## MCP equivalent (when available)

If `npx databazaar-mcp` is installed, prefer MCP tool names — they handle the
PATCH-vs-POST routing internally:

| MCP tool | Underlying call |
|---|---|
| `create_listing` | `POST /listings/draft` |
| `get_upload_urls` | `POST /listings/{id}/upload-urls` |
| `confirm_upload` | `PATCH /listings/draft/{id}` with `full_data_path` |
| `set_schema` | `PATCH /listings/draft/{id}` with `schema` (pre-publish only) |
| `update_listing` | `PATCH /listings/{id}` with arbitrary fields |
| `get_listing_status` | `GET /listings/{id}` |
| `publish_listing` | `POST /listings/{id}/publish` |

The MCP reads token from `DATABAZAAR_AGENT_TOKEN` env var (NOT
`DATABAZAAR_TOKEN`, which it interprets as an OAuth token and fails). Set it
explicitly when shelling out:

```python
env = os.environ.copy()
env['DATABAZAAR_AGENT_TOKEN'] = agent_token
subprocess.Popen(['npx','-y','databazaar-mcp'], env=env, ...)
```

`set_schema` via MCP only works pre-publish. For post-publish schema fixes
(correcting auto-detected row_count), use `update_listing` or direct REST
PATCH on `/listings/{id}`.

## Credentials

- Skill never stores tokens. User supplies via `DATABAZAAR_AGENT_TOKEN` env
  var, the on-disk file at `~/.hermes/databazaar/agent-token.json`, or
  `--token` flag.
- Token NEVER written to datacard, provenance, or any output file.
- Token NEVER logged (use `***` redaction).

## Errors

| Status | Body | Meaning | Action |
|---|---|---|---|
| 401 | UNAUTHORIZED | Token invalid/expired | Re-register with fresh agent_name |
| 403 | "requires user session" | OAuth token used for seller path | Use agent JWT, not OAuth |
| 403 | "requires agent session token" | Wrong token type | See `domain/databazaar-agent-token` |
| 404 | "Route ... not found" | Endpoint doesn't exist | Check working-routes list above |
| 404 | "Draft not found" | PATCHing `/listings/draft/{id}` post-publish | Use `PATCH /listings/{id}` |
| 422 | "Validation error" | Field-name typo or wrong enum | No detail; bisect fields |
| 422 | "No valid fields to update" | Field accepted by other path | Try the other PATCH endpoint |
| 422 | SAMPLE_NOT_READY | Auto-sample not done (CSV) or never starts (ZIP) | For ZIP, set sample_file_path manually |

## Rate limits

Conservative: 60 req/min/agent. 429 → exponential backoff, max 3 retries.

## Alternative marketplaces (when DataBazaar isn't enough)

For datasets with broader appeal, also consider (ranked by effort vs revenue):

1. **Kaggle Datasets** — free, huge visibility, pure brand/lead-gen
2. **HuggingFace Datasets Hub** — free, ideal for ML training data including multimodal
3. **Snowflake Marketplace / Databricks Marketplace** — paid B2B, highest revenue ceiling, requires publisher onboarding
4. **AWS Data Exchange** — paid B2B, review process, best for recurring snapshots
5. **Datarade** — generalist aggregator, leads-as-a-service model
6. **Domain-specific buyers** (e.g. for aviation: VREF, Aircraft Bluebook, insurance underwriters) — direct license deals can be 10–100× the per-unit marketplace price for one-time acquisitions

The mirror packaging is the same: `data.{csv,parquet}` + `datacard.md` +
`schema.json`. Each platform has its own metadata file (Kaggle: `dataset-metadata.json`,
HF: `README.md` with YAML front-matter).
