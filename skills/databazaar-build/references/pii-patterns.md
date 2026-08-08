# PII Detection Patterns

PII detection is a **hard gate** — if patterns are detected and not redacted,
the skill must refuse to publish and warn the user.

## Tier 1 — auto-redact (high confidence)

| Pattern | Regex / method | Action |
|---|---|---|
| Email | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | Redact to `<email>` |
| US phone | `\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b` | Redact to `<phone>` |
| SSN-shape | `\b\d{3}-\d{2}-\d{4}\b` | **Block publish entirely.** |
| Credit-card-shape | Luhn check on 13-19 digit sequences | **Block publish entirely.** |
| IBAN | `\b[A-Z]{2}\d{2}[A-Z0-9]{4,30}\b` (validated checksum) | Redact |
| API key shapes | `(sk-\|pk_\|dbz_live_\|AKIA)[A-Za-z0-9]{20,}` | **Block publish entirely.** |

## Tier 2 — flag for review (lower confidence, context-dependent)

| Pattern | Method |
|---|---|
| Person name (column-level) | Heuristic: column name matches `(name\|first\|last\|fullname)` AND values are 2-4 capitalized tokens |
| Street address | NER + presence of street-suffix tokens (St, Ave, Rd, Blvd) |
| DOB | Date column + reasonable birth-year range (1900-2020) |
| IP address | `\b(?:\d{1,3}\.){3}\d{1,3}\b` validated as routable |
| Geo precision | Lat/lon with >4 decimals (sub-10m precision) |

Tier 2 detections produce a `pii_report.json` entry with `severity: "review"`
and require explicit user acknowledgement before publish.

## Aggregation refusal patterns

Refuse the request entirely if it implies aggregating PII about private
individuals:

- "Email addresses of all [profession] in [city]"
- "Phone numbers of [group]"
- "Home addresses of [group]"
- "Salaries of named individuals"
- "Medical conditions of [named persons]"

Public-figure exception: aggregating *public-record* facts about elected
officials, executives in their professional capacity, etc., is allowed —
but datacard must flag it as "public-figure data" with sources.

## False-positive handling

- A column of email-shaped strings that are all `noreply@*` or `*@example.com`
  is not PII — flag, don't redact.
- A "phone" column where the values are clearly product SKUs or fake (all
  555-01XX) — flag, don't redact.

## Reporting

`pii_report.json` schema:

```json
{
  "scanned_at": "ISO timestamp",
  "row_count": 12345,
  "detections": [
    {
      "column": "contact_email",
      "pattern": "email",
      "tier": 1,
      "match_count": 66,
      "action": "redacted",
      "sample_redacted": ["<email>", "<email>"]
    }
  ],
  "blocked": false,
  "blockers": []
}
```

If `blocked: true`, `scripts/build.py` exits with non-zero and writes the
reason to stderr.
