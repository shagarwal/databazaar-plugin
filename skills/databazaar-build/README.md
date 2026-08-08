# databazaar-build — Anthropic Skill

A reusable [Anthropic skill](https://docs.anthropic.com/en/docs/build-with-claude/skills)
that builds clean, agent-ready datasets on demand and (optionally) lists
them on [databazaar.io](https://databazaar.io).

This is the **consumer-side** skill in the DataBazaar umbrella — it acquires
data on a caller's behalf. Its sibling `databazaar-discovery` is the
**operator-side** pipeline that builds the marketplace's inventory. See
[`../README.md`](../README.md) for how the two relate.

## Quick start

```bash
cd skills/databazaar-build
python scripts/build.py acquire \
  --request "World Bank GDP per capita by country" \
  --out ./out
```

Outputs:
- `data.csv` — the dataset
- `schema.json` — typed schema
- `datacard.md` — rubric-compliant datacard
- `provenance.json` — per-row source attribution
- `sample.csv` — ≤1k row sample
- `pii_report.json` — PII scan
- `listing_suggestion.json` — title, category, tags, suggested price

## Modes

| Mode | Status | Purpose |
|---|---|---|
| `acquire` | ✅ v0.2 (databazaar + HuggingFace + World Bank) | Plain-English → dataset |
| `aggregate` | ⬜ stubbed | Multi-source merge |
| `prepare` | ✅ v0.2 (CSV/JSON, schema inference, PII scan) | Clean up proprietary input |
| `list` | ⬜ stubbed | Publish to databazaar.io |

## Layout

```
SKILL.md             — skill manifest (Anthropic format)
references/          — domain knowledge files referenced by SKILL.md
scripts/             — orchestrator, normalizer, adapters, eval harness
evals/
  cases/             — YAML test cases
  fixtures/          — cached source responses
  runs/              — timestamped run records (auditable)
  notes/             — iteration log
```

## Running evals

```bash
python scripts/eval.py             # all cases
python scripts/eval.py --case 01   # one
python scripts/eval.py --tag refusal
```

Each run writes to `evals/runs/<timestamp>-<sha>/` with a `summary.json`
plus per-case artifacts. Commit the run record alongside skill changes —
that's the audit trail.

## Status

**v0.3** — eval suite expanded 10 → 71 cases (generator-driven).
70/70 graded pass (100%), 1 xfail (known empty-input gap).
3 real adapter bugs surfaced and fixed during expansion.
See `evals/notes/2026-05-04-v0.3.md` for coverage matrix and v0.4 priorities.

## Why this skill exists

Most "build me a dataset" agent invocations today require humans to
hand-stitch sources, document provenance, and decide on schemas. This
skill compresses that to one call, with built-in:

- Provenance (every row tagged with source + retrieval timestamp)
- Datacard generation (rubric-compliant, no hand-waving)
- PII scanning (gated)
- ToS guardrails (allowlist / denylist for web fetching)
- One-flag publish path to databazaar.io for sellers
