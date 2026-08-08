# Recycled-identifier caveat catalog

Some identifiers used as join keys for public-records enrichment are reissued
by their authority. Joining naively produces false matches that look like
matches on the *current* aircraft / vehicle / device but actually describe a
*previous* holder of that ID.

When a dataset joins on any of these identifiers, the build script auto-injects
a **Temporal validity** section into `datacard.md` and includes a per-row
`identifier_first_issued` column when the source data exposes it.

## FAA N-numbers (US aircraft tail numbers)

- **Recycled:** Yes. The FAA reassigns N-numbers after a previous registration
  is cancelled or expired (typically 5+ years post-deregistration).
- **Anchor field:** `airworthiness_date` (or `cert_issue_date`) from the FAA
  Releasable Aircraft database (`MASTER.txt`). NTSB events with
  `event_date < airworthiness_date` describe a previous aircraft.
- **Real-world example (May 2026 SR-22 dataset):** 38/302 N-numbers had NTSB
  hits, but ~30 of those were 1968–1995 events on aircraft predating Cirrus
  (which started production in 1999).

## Vehicle Identification Numbers (VIN)

- **Recycled:** Effectively no within the standardized 17-digit era (1981+).
  Pre-1981 VINs are non-unique by design.
- **Anchor field:** model year encoded in VIN position 10. Reject any
  enrichment event predating that model year.

## US license plates (state-issued)

- **Recycled:** Yes, aggressively. Plate numbers are reissued by state DMVs
  within a few years of cancellation. *Do not* use plates as a join key for
  historical enrichment without a state + issue-date anchor — the false-match
  rate is high and the join is essentially worthless.

## MAC addresses

- **Recycled:** Yes. Some manufacturers reuse OUI ranges; randomized client
  MACs are not stable per device. Treat any MAC-keyed enrichment as
  best-effort, not authoritative.

## Phone numbers

- **Recycled:** Yes. US carriers reassign disconnected numbers after an aging
  period (~45–90 days). For enrichment, prefer the disconnect-date anchor from
  carrier portability records.

## SSN

- **Recycled:** No (officially). But SSN-keyed enrichment is in practice
  blocked by the skill's PII guardrails — never reach this case.

## Domain names

- **Recycled:** Yes (drop-catching). WHOIS history APIs expose registration
  intervals; filter enrichment to current-owner interval only.

## Datacard injection

When the build script detects any of these identifiers as a column in
`schema.json` (column name match against the patterns below), it appends:

```
## Temporal validity

This dataset joins on `<identifier>`, which is reissued by <authority>. To
avoid false matches when interpreting the enrichment columns, filter on
`<anchor_column> >= <identifier_first_issued>` for any historical event.

Approximate false-match rate in this dataset: <observed>%.
```

Patterns the auto-injection looks for:

| Identifier | Column-name regex | Anchor column |
|---|---|---|
| FAA N-number | `^(registration_)?n_?number$\|^tail(_number)?$` | `faa_airworth_date` or `faa_cert_issue_date` |
| VIN | `^vin$` | `model_year` |
| US plate | `^(license_)?plate$` | `plate_issue_date` |
| MAC | `^mac(_address)?$` | (none — note as best-effort) |
| Phone | `^phone(_number)?$` | `phone_first_assigned` |
| Domain | `^domain(_name)?$` | `whois_registered_at` |
