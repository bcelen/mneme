# Mneme Local Identities 1 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; committed on a feature branch, awaiting review.
**Run date:** 2026-10-05.

## Runtime

- Linux container: CPython 3.11.15 and 3.10.20. Not yet run on the accepted macOS CPython 3.9.6 runtime.
- Python standard library only; no network access.

## Verification

`tests/test_identities.py`: 7 tests pass. Expected values for `mira.sol@example.test` were worked out by hand from the fixtures before running: 16 occurrences (6 as sender, 10 as recipient), 13 distinct source hashes (`EML-001`, `EML-005`, `EML-016` share bytes, as do `EML-018` and `EML-022`), 11 EML and 5 MBOX, first seen 2025-10-14T09:30:00Z, last seen 2025-10-28T09:00:00Z, one undated occurrence (`EML-009`), and correspondents Arin (sent 5, received 4), Nila (sent 1, received 4), and Rowan (received 2). The tests also cover address normalization, quarantine exclusion, citations that resolve through `show`, read-only and deterministic behavior, validation, and the CLI.

Deliberate mutations: hiding duplicates, counting invalid dates as dated, and splitting an address by display name were each caught. Case-sensitive addresses initially survived, because every fixture address is lower-case; a direct parser test was added and now catches it. Removing the quarantine guard is an equivalent mutation: the engine never gives quarantined records address fields, so they cannot involve any identity either way. The guard is kept as defense in depth.

## CLI evidence

State: the standard four-batch synthetic state (`generation-0004`, 30 sources, source manifest `d45c73114e0c6685da3f3134eea04a246cbc467708135eabd3fb115e04e049f8`).

| Address | Occurrences | Distinct hashes | Sender / recipient | Undated | First seen (UTC) | Last seen (UTC) | Display names |
|---|---:|---:|---|---:|---|---|---|
| `arin.vale@example.test` | 12 | 9 | 5 / 7 | 0 | 2025-10-14T09:30:00Z | 2025-10-30T17:45:00Z | Arin Vale |
| `jose.nunez@example.test` | 1 | 1 | 0 / 1 | 0 | 2025-10-15T15:45:00Z | 2025-10-15T15:45:00Z | José Núñez |
| `mira.sol@example.test` | 16 | 13 | 6 / 10 | 1 | 2025-10-14T09:30:00Z | 2025-10-28T09:00:00Z | Mira Sol, Míra Sol |
| `nila.hart@example.test` | 8 | 8 | 6 / 2 | 1 | 2025-10-14T09:30:00Z | 2025-10-30T17:45:00Z | Nila Hart |
| `rowan.pike@example.test` | 2 | 2 | 2 / 0 | 0 | 2025-10-19T07:15:00Z | 2025-10-27T10:05:00Z | Rowan Pike |
| `zoe.akin@example.test` | 1 | 1 | 1 / 0 | 0 | 2025-10-15T15:45:00Z | 2025-10-15T15:45:00Z | Zoë Akın |

`identities` output SHA-256 `8d0ff71c64779cc65692be02124320f3f9224b4405e4bb533590ef5a17290835`; `identity --address MIRA.SOL@example.test` output SHA-256 `3e87d846ae9787ad9f6d781aa262ed2f7859490425b2612a967933d87b388962`. An address with no occurrence stops with exit 2.

## Limitations

- Only `From` and `To` are available; `Cc`, `Bcc`, `Reply-To`, and `Sender` are not derived by the accepted engine.
- First and last seen use the message's own `Date` header, which the sender controls.
- No person model, alias linking, or user annotation. Those are user-controlled modeling decisions.
- Computed on every call by scanning all records; fine only at synthetic scale.
