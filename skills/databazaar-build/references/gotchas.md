# Build Skill — Operational Gotchas

Things the sibling `databazaar-discovery` pipeline learned the hard way and
that this skill should encode from day one. Each entry has a one-line rule
and a one-paragraph "why".

## 1. Treat 429 / 503 as ambiguous, not failed

**Rule:** When any adapter (especially `web_fetch`, `huggingface`,
`kaggle`, `github`) gets a 429 or 503, mark the source `ok=true` with a
`status="ambiguous"` flag and retry with exponential backoff (2s, 8s,
30s). Do NOT mark the source as dead/unreachable. Treat 4xx other than
429 and 5xx other than 503 as real failures.

**Why:** Discovery's initial reachability check treated 429 as a hard
"unreachable" signal. The result was 787 perfectly fine candidates getting
demoted from `haiku_passed` to `heuristic_rejected` during a HuggingFace
rate-limit storm — `repair-reachability-429.ts` had to be written to
restore them. The build skill talks to the same flaky upstream and will
hit the same wall.

Reference fix: `apps/api/src/routes/datasets.federation.ts` and
`apps/discovery/src/lib/reachability.ts` in the agentdatamarketplace repo.

## 2. Cross-source dedupe via stable hash

**Rule:** When `acquire` fans out across multiple adapters (e.g. user asks
for "GDP per capita" and both `databazaar` and `world_bank` return data),
deduplicate using `sha256(normalized_title + canonical_url)` per result
*before* the merge step. Same dataset reuploaded to multiple indexes is
common (HF mirrors of Kaggle datasets, etc.) and naive merge produces
duplicates with conflicting provenance.

**Why:** Discovery's `dedupe_hash` column on `discovery_candidates` (see
migration `20260430000001`) handles exactly this — the same MegaMath shard
indexed by HuggingFace and again by some HF mirror gets one row, not two.
The build skill's `acquire` parallel fanout has the same shape and needs
the same hash.

`canonical_url` here means: lowercase scheme+host, strip trailing slash,
strip query params except `dataset=` / `id=`, sort path components for
known catalog URLs. Title normalization: lowercase + collapse whitespace.

```python
def dedupe_hash(title: str, url: str) -> str:
    norm_title = " ".join(title.lower().split())
    norm_url = canonicalize_url(url)
    return hashlib.sha256(f"{norm_title}|{norm_url}".encode()).hexdigest()
```

## 3. Anthropic OAuth + Opus needs a Claude-Code system prefix

**Rule:** If you ever wire an LLM call into the build skill (datacard
polish, license interpretation, ranking adapter results), and the auth is
an OAuth token from `~/.claude/.credentials.json` rather than a real
`sk-ant-api...` key, the system prompt MUST start with the literal
content block `"You are Claude Code, Anthropic's official CLI for Claude."`
as content block index 0. String-concatenation does NOT satisfy the check.

**Why:** Anthropic gates OAuth-bearer Opus requests behind a Claude-Code
identity check on the system prompt. Without the prefix, every Opus call
returns `429 rate_limit_error` with an empty `"Error"` message regardless
of remaining session quota. Discovery debugged this for hours; the
canonical fix lives in
`apps/discovery/src/lib/anthropic.ts:34-50` (`withClaudeCodePrefix`).

```python
# Equivalent in Python (Anthropic SDK):
client.messages.create(
    model="claude-opus-4-7",
    system=[
        {"type": "text", "text": "You are Claude Code, Anthropic's official CLI for Claude."},
        {"type": "text", "text": <your real system prompt>},
    ],
    messages=[...],
    extra_headers={"anthropic-beta": "oauth-2025-04-20"},
)
```

If the key is a real API key (`sk-ant-api...`), skip the prefix — it's
harmless but unnecessary.

## 4. supabase-js range pagination caps at 1000 rows

**Rule:** When the `databazaar` adapter pages through catalog results,
`.range(0, n)` silently caps `n` at 999 unless you set
`global.fetch.headers["Range-Unit"]: "items"`. To paginate beyond 1000,
issue multiple range queries.

**Why:** Discovery hit this fetching `discovery_candidates` lists; the
first 1000 came back fine, results 1001+ silently went missing. The
pagination loop in `apps/discovery/src/cli/backfill-reachability.ts` is
the working pattern — page in chunks of 500–1000 rather than asking for
more.

## 5. HF concurrency cliff at ~3 parallel requests

**Rule:** When the `huggingface` adapter or `web_fetch` adapter targets HF
URLs (parquet shards, dataset card fetches, etc.), cap parallel requests
at **3 per host**. Higher concurrency reliably produces 429s within the
first few seconds and the recovery cost is worse than serial.

**Why:** Discovery initially ran 8-way concurrent reachability checks
against HF; that's what triggered the 787-candidate demotion incident.
The fix in `apps/discovery/src/cli/backfill-reachability.ts` was
`CONCURRENCY = 3`.

## 6. UTC-midnight budget rollover for any LLM-using path

**Rule:** If your adapter or post-process step charges against a daily
budget cap (e.g. spend tracking on a Tier-1-style ranker), key the daily
ledger by `UTC` date, not local. Operator running at 5pm Pacific does NOT
get a fresh budget at midnight Pacific — they get one at midnight UTC.

**Why:** Discovery's `discovery_budget_ledger` keys on `day` as a
PostgreSQL `DATE` which Supabase serialises as UTC. Operator briefly
thought their Opus budget had been wiped at midnight local; it had not.
The same ambiguity will bite anyone wiring up cost-aware adapters here.

---

This file is intentionally short — only entries that have already cost a
real engineer real time go here. Resist the urge to fill it with
"theoretical" gotchas; those go in adapter docstrings or eval cases, not
this list.
