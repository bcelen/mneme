# Mneme Local Synthetic Prototype 3 — Mixed EML and mboxrd Ingestion

This experiment extends incremental ingestion (`experiments/mneme-local-prototype-2/`) to a second source family, synthetic mboxrd mailboxes, while keeping EML behavior, Find results, and citations unchanged. It reuses the corrected engine in `experiments/synthetic-hardening-1/` and prototype 2's reviewed EML fixtures by import. No existing file is modified.

## Files

- `mboxrd.py`: exact-byte segmentation, defect classification, and mboxrd escaping.
- `mbox_fixtures.py`: four pinned, wholly fictional mailbox fixtures.
- `mneme.py`: ingestion, verification, staged publication, recovery, rebuild, Find, and citation display.
- `tests/test_mbox.py`: 22 focused tests.

## Why not `mailbox.mbox`

The standard library's `mailbox.mbox` treats every `From ` line as a boundary, which matches mboxrd. It is still unsuitable as a preservation primitive: it keeps no bytes before the first envelope line, trims each message's separator line, and does not reverse mboxrd escaping. `mboxrd.py` therefore segments with `re`, and the tests use `mailbox.mbox` as an independent check that record boundaries agree.

## Identity convention (`mneme-occurrence-identity-v2`, experimental)

- **Container:** an incoming `.mbox` file. Its key is `synthetic-mbox:<file name>`.
- **Segment:** a contiguous byte range of a container. A boundary is every line that begins with `From `. Bytes before the first boundary form a `preamble` segment. The segments of a container cover every byte exactly once, so the container is exactly the concatenation of its segments.
- **Occurrence:** one preserved segment (MBOX) or one preserved file (EML). The preserved bytes of an MBOX occurrence are the segment exactly as stored, including the envelope line, mboxrd escaping, and the blank separator line.
- **Source key:** `synthetic-eml:<file name>` for EML, and `synthetic-mbox:<file name>#offset=<byte offset>` for MBOX segments.
- **Source ID:** archive-assigned `EML-NNN`, as in prototype 2, allocated to new keys in order of container key, then byte offset. `EML` here means "email occurrence", not the file format; the accepted citation grammar only allows `EML-NNN`.
- **Container observation:** each distinct `(container key, container SHA-256)` seen by an ingest is recorded once, with the ordered segment IDs that reassemble it. Re-observing identical bytes adds nothing; an appended mailbox adds a new observation that reuses the existing segment IDs.
- **Recorded boundaries:** each MBOX item records `offset`, `length`, `ordinal`, `kind`, and `starts_after_blank_line`. Verification reassembles every observed container from the preserved segments, checks its hash, re-runs segmentation on those bytes, and requires the recorded spans to match.

## Derivation

- EML occurrences take exactly the prototype-2 path through the isolated parser.
- An MBOX segment is quarantined without parsing if it is a preamble, has a malformed envelope line, is not preceded by a blank line (`ambiguous-boundary`), lacks the blank separator line (`unterminated-record`), lacks a final newline (`truncated-record`), exceeds 128 KiB (`oversized-record`), or carries no message (`empty-record`).
- Otherwise the segment is unescaped by removing the envelope line and the separator line, and removing one `>` from every line matching `^>+From `. The resulting message is parsed by the same isolated parser.
- The derived record, index occurrences, and citations bind to the preserved segment's SHA-256. The unescaped message's digest and size are recorded in the record's `mbox` field, with the rule `synthetic-mboxrd-segmentation-v1`.
- `show` for an MBOX citation re-reads the preserved segment, unescapes it, locates the cited header or MIME part, checks it against the index, and displays escaped inert text with the container span.

## Ingest, publication, and recovery

Planning happens before any staging or parsing. A known key with the same bytes and boundary context is already preserved. A known key with different bytes or boundary context rejects the whole batch. If there are no new occurrences and no new container observations, nothing is written.

Publication stages a complete new generation under `generations/.stage-*`, verifies it, renames it to the next `generation-NNNN`, and atomically replaces `CURRENT`. An exception before `CURRENT` is replaced removes everything created. If a crash prevents that cleanup, readers keep using the generation named by `CURRENT`, `verify` lists the leftovers, and `ingest` refuses until `recover` has verified `CURRENT` and removed only the unpublished leftovers.

## Commands

All state paths should be disposable paths outside the repository. Run from the repository root.

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-3/mneme.py ingest --incoming <dir of .eml/.mbox> --state <state> --recorded-at 2026-09-28T09:00:00Z
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-3/mneme.py verify --state <state>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-3/mneme.py recover --state <state>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-3/mneme.py rebuild --state <state> --output <new dir>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-3/mneme.py find --state <state> --query "lantern observatory"
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-3/mneme.py show --state <state> --citation <citation>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-3/tests/test_mbox.py
```

## Boundary

This remains an experiment. It accepts only reviewed, wholly fictional synthetic bytes, uses the Python standard library only, and makes no network, account, service, or stack commitment. The identity convention is experimental, not an accepted architecture decision. Prototype 2 refuses a prototype-3 state (unsupported identity convention), and prototype 3 does not read prototype-2 states; there is no migration between them.
