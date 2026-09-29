# Mneme Local Synthetic Prototype 4 — Find Filters

This experiment adds deterministic, inspectable filtering to Find over the mixed EML and mboxrd state of `experiments/mneme-local-prototype-3/`. Prototype 3 is loaded by path and left unchanged. Every command except `find` is prototype 3's.

## Filters

| Option | Matches | Source of truth |
|---|---|---|
| `--status indexed\|indexed_with_warnings` | processing status | `messages.json` record |
| `--family eml\|mbox` | source family | source manifest |
| `--mailbox <name>.mbox` | MBOX container name | source manifest |
| `--has-attachment` / `--no-attachment` | at least one part preserved under `attachments/` | `messages.json` parts |
| `--from <address>` | an address in the derived `From` field | `messages.json` fields |
| `--to <address>` | an address in the derived `To` field | `messages.json` fields |
| `--participant <address>` | `From` or `To` | `messages.json` fields |
| `--since` / `--until YYYY-MM-DD` | inclusive UTC day of the derived `Date` field | `messages.json` fields |

- Filters combine with AND, and with the query when one is given. They are applied in the fixed order of the table.
- Addresses are compared as lower-cased address specs, so display names and case do not matter.
- Dates are normalized to UTC. A date with a `-0000` or missing offset is interpreted as UTC and marked `no-timezone`. An invalid or missing date is never placed in a range; while a date filter is active, such candidates are listed in `undated_candidates`.
- Quarantined occurrences are never results. `--status quarantined` is rejected.

## Output

- Without filters, `find` returns prototype 3's output unchanged, byte for byte.
- With filters, the output adds `filters` (the normalized values), `filter_report` (candidate count, and for each filter how many candidates it removed and how many remain), and per-result `facts` (status, family, mailbox, attachment flag, sender and recipient addresses, date status, and UTC date).
- With a query, results and citations are exactly the unfiltered Find rows for the surviving occurrences, in the same order.
- Without a query, every non-quarantined occurrence is a candidate, and each result is cited by its indexed subject header when it has one.

Filtering is evaluated at query time from the verified current generation. It adds no derived state, so ingestion, rebuild output, and every existing hash are unchanged.

## Commands

Run from the repository root, with disposable state outside the repository.

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-4/mneme.py ingest --incoming <dir> --state <state> --recorded-at 2026-09-20T12:00:00Z
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-4/mneme.py find --state <state> --query "lantern observatory" --family mbox
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-4/mneme.py find --state <state> --participant arin.vale@example.test --since 2025-10-14 --until 2025-10-14
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-4/tests/test_filters.py
```

## Boundary

Local, offline, synthetic-only, and standard library only. No ranking, fuzzy matching, identity or person resolution, threading, `Cc`/`Bcc` filtering, UI, or stack decision.
