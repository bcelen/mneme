# Experimental Contracts

**Status:** Accepted
**Review date:** 2026-09-17
**Version family:** `v0.1-experimental`
**Scope:** Phase-3 synthetic feasibility evidence only; not a production format or stack decision.

## Common rules

- Accepted archive terminology remains unchanged: the **source archive** is the immutable system of record; a **source package** is the bounded set supplied together; a **source item** is a preserved member; and a **preservation envelope** is the Phase-3 directory that carries one source package plus its manifest and provenance evidence. The envelope is not a second source package.
- Contract documents and machine-readable schemas are versioned together.
- Unknown major versions are rejected. Unknown fields in the same experimental minor version are preserved where the contract permits and never silently reinterpreted.
- Text control files are UTF-8 without BOM, use LF line endings, and reject invalid UTF-8.
- Source payload bytes are opaque. No text, path, MIME, line-ending, or encoding normalization changes source bytes.
- Timestamps are UTC RFC 3339 with second precision unless subsecond evidence is material; an absent or uncertain source time remains absent or uncertain.
- Identifiers are ASCII, stable, non-secret, and contain no address, display name, provider ID, subject, or other personal data.
- Each result names its contract version, corpus release, candidate, run ID, tool/dependency identity, and evidence digest.

## Contract P-01 — Preservation profile

### Package layout and path rules

```text
preservation-envelope/
├── package.json
├── manifest.jsonl
├── manifest.sha256
├── provenance.jsonl
├── provenance.sha256
└── payload/
```

`payload/` is the source package held inside the preservation envelope. Its relative paths must be NFC UTF-8, use `/`, contain no empty, `.` or `..` components, begin with neither `/` nor a drive designator, and be unique under exact and Unicode-normalized comparison. Symlinks and other non-regular objects are prohibited in the experimental profile and produce quarantine, not dereferencing.

`manifest.jsonl` has one record per regular payload file, sorted by the raw UTF-8 bytes of `path`. Each record uses this fixed key order:

```json
{"profile":"mneme.preservation/v0.1-experimental","source_package_id":"spkg-corp-001-v1","source_item_id":"sitem-corp-001-0001","path":"payload/mailbox.mbox","size":123,"hash_algorithm":"sha256","digest":"<64 lowercase hex>"}
```

The final record count must equal package membership. `manifest.sha256` is the lowercase SHA-256 of the exact `manifest.jsonl` bytes followed by two spaces and `manifest.jsonl`.

### Package-level digest

For every manifest record, create the byte sequence:

```text
UTF8(path) NUL ASCII(size) NUL ASCII("sha256:") ASCII(digest) LF
```

Sort those sequences by `UTF8(path)` and hash their concatenation with SHA-256. `package.json` records this `payload_set_digest`, manifest digest, provenance digest, package ID, corpus release, profile version, declared source family, declared omissions, acquisition-event ID, and expected-truth ID. Hash the exact `package.json` bytes and record that digest in the separately stored release manifest. This breaks the possibility that an altered package can silently redefine its own root of trust.

### Provenance chain

`provenance.jsonl` is append-only. Each line uses fixed key order and includes `event_id`, `event_type`, `occurred_at`, `actor_type`, `actor_id`, `approved_scope`, `tool`, `tool_version`, `inputs`, `outcome`, `previous_event_digest`, and `event_digest`. `event_digest` is SHA-256 over the UTF-8, no-whitespace JSON object containing all preceding fields in that fixed order and excluding `event_digest`; the first event uses 64 zeroes for `previous_event_digest`. Corrections append events. Credentials and source content are forbidden.

### Required behavior

- SHA-256 is the sole Phase-3 experimental content hash. This does not select a production algorithm.
- Verification reads ordinary files and the documented profile; no candidate database or application runtime is required.
- Python and Go verifiers are implemented independently and share only fixtures, schemas, and expected results.
- One-byte change, wrong size, missing/extra member, path escape, case/normalization collision, altered manifest/provenance, or unsupported profile version stops parsing, indexing, export-complete, backup-valid, and restore-valid claims.
- A legacy `v0.0-experimental` fixture with a deliberately different version marker is included only to prove explicit unsupported-version failure under AT-P06.

## Contract E-01 — Application-independent export

### Export layout

```text
mneme-export-v0.1/
├── export.json
├── checksums.sha256
├── schemas/
├── source-packages/
├── provenance/events.jsonl
├── history/annotations.jsonl
├── history/classifications.jsonl
├── records/messages.jsonl
├── records/people.jsonl
├── records/identities.jsonl
├── records/conversations.jsonl
├── records/attachments-documents.jsonl
├── records/organizations.jsonl
├── records/topics.jsonl
├── records/events.jsonl
├── records/relationships.jsonl
├── records/timelines.jsonl
├── generations/processing-rules.jsonl
└── omissions.jsonl
```

- `source-packages/` contains source payloads and P-01 preservation evidence unchanged.
- Every JSONL record has `record_type`, `record_version`, stable ID, source/provenance references, state class (`source`, `user-controlled`, or `machine-derived`), generation ID when applicable, and attributes defined by a bundled schema.
- User corrections and classifications preserve ordered history sufficient for undo; current state alone is insufficient.
- Machine-derived records are exportable for explanation and migration but remain rebuildable and never redefine source facts.
- `export.json` declares `complete` or `partial`, creation tool/version, source-package set, record counts, included contract versions, allowed packaging variance, and the digest of `omissions.jsonl`.
- `checksums.sha256` covers every export file except itself using sorted relative paths. A ZIP or tar wrapper is optional transport packaging and has no semantic authority.

### Equivalence and migration

Independent inspection must enumerate and verify the directory using generic JSON and hash tools. Repeat exports compare semantic records after removing only the declared export timestamp and run ID; source bytes, stable IDs, user history, omissions, and generation identities must match exactly.

Cross-migration compares:

- exact source hashes and package membership;
- exact stable IDs and user-history event order;
- canonical semantic values and references;
- explicit transformed, unsupported, rejected, and omitted fields;
- machine-derived generation status without requiring engine-specific ranks or database internals.

A database dump may accompany recovery evidence but is never E-01 export evidence.

## Contract W-01 — Parser-worker protocol and isolation

The orchestrator writes `/input/job.json`, exposes exactly one `/input/source-item` read-only, and provides empty `/output` and bounded `/tmp` locations. The worker writes only `/output/result.json` and declared derivative files.

`job.json` includes protocol version, run/job IDs, fixture/source identifiers, expected input size and SHA-256, requested synthetic operation, and the fixed resource ceilings. It contains no arbitrary host path, URL, credential, or database connection.

`result.json` includes protocol version, job ID, one status (`success`, `unsupported`, `quarantined`, `timeout`, `crash`, `policy_violation`, or `invalid_output`), input digest observed, bounded diagnostics, output inventory and hashes, warnings, and elapsed/resource observations. Output text is untrusted until schema, count, size, path, encoding, and digest validation completes.

The fixed experimental limits are: one CPU, 256 MiB memory, 32 processes, 10 seconds wall clock, 16 MiB temporary memory, 8 MiB total output, 128 output files, nesting 32, expanded bytes 64 MiB, and expansion ratio 20:1. The isolation controls are those in `SYNTHETIC-ONLY-SAFEGUARDS.md`.

Any source-write attempt, path escape, network attempt, malformed output, timeout, crash, or ceiling breach must be contained and produce a non-success result. A failed worker cannot modify another job, the derived store, or preservation evidence.

## Contract R-01 — Safe rendering

- The default user-visible representation is escaped plain text.
- HTML rendering, when invoked by the test, occurs in a nonprivileged isolated context with no script, forms, plugins, native bridge, remote resources, navigation, cookies, persistent storage, worker, popup, or download capability.
- The web slice uses a sandboxed child context and a content policy equivalent to `default-src 'none'`, with only the minimum inline style needed for the fixture allowed by hash if required.
- The WebKit slice uses a nonpersistent website data store, denies navigation and new windows, registers no script message handler, and does not receive outbound-network entitlement.
- Source HTML is never rewritten in the archive. Any sanitized representation is a derived artifact with tool/version and source provenance.
- A loopback canary and network observation are required evidence; a visual result alone is insufficient.

## Contract D-01 — Derived state and generations

Every record is classified as:

- **source:** preserved under P-01 and never mutated;
- **user-controlled durable:** annotations, corrections, classification choices, and their history; reversible by recorded undo;
- **machine-derived:** parse output, normalized fields, links, duplicate/junk suggestions, indexes, snippets, deterministic synthetic answer records; fully reconstructible from source and recorded rules.

A generation identity is the SHA-256 of the ordered set of corpus release, verified source-package root digests, rule/tool versions, tokenizer/search settings, and contract versions. Machine-derived rows always carry one generation ID. Mixing generation IDs in a complete result is an error. A changed input creates a new generation and marks the prior one stale; it never rewrites prior provenance.

Rebuild begins with an empty derived store, imports verified user history separately, recreates machine-derived state, records failures/skips, and compares deterministic records. The deterministic model stub is labeled synthetic and cannot be presented as model evidence.

## Contract C-01 — Provenance and citation

A citation is application-issued structured data, never a free-form identifier accepted from generated text:

```json
{
  "citation_version": "mneme.citation/v0.1-experimental",
  "citation_id": "cite-<opaque-id>",
  "generation_id": "gen-sha256-<digest>",
  "source_package_id": "spkg-corp-018-v1",
  "source_item_id": "sitem-corp-018-0001",
  "representation_id": "repr-<digest>",
  "part_path": "mime/1/text",
  "byte_start": 10,
  "byte_end": 42,
  "representation_sha256": "<digest>",
  "processing_event_id": "pevent-<id>"
}
```

Offsets index UTF-8 bytes in the identified derived representation, not characters in source encodings. The representation has its own source and processing lineage. Validation requires current verified generation, known IDs, bounds, matching digest, allowed claim-to-source relationship, and complete provenance. Unknown, stale, fabricated, cross-generation, out-of-bounds, or provenance-gapped citations are rejected. User-authored statements are labeled as such rather than given fabricated source lineage.

## Contract F-01 — Deterministic Find and Ask stub

Each query case fixes corpus release, generation, query text, fields, filters, scope, limit, tokenizer/configuration identity, ranking rule, and tie-breaker. SQLite uses FTS5 from SQLite 3.53.3; PostgreSQL uses version 18.6 built-in FTS with the `simple` text-search configuration and deterministic collation for test identifiers.

Within each candidate, results sort by native rank descending and then stable source-item ID ascending. The same build, query, and generation must return identical ordered IDs across repeated runs and clean rebuilds. Native rank values are not compared across engines. Cross-engine evidence compares expected membership and documents tokenization/ranking differences rather than forcing false equivalence.

Generated snippets are escaped derivatives and never citation authority. The local Ask stub receives only allowlisted retrieved source references, returns deterministic synthetic claims/citation candidates, owns no tool or network authority, and cannot bypass the C-01 validator. Prompt-injection text remains data. Insufficient or contradictory evidence returns explicit uncertainty.

## Contract N-01 — Privacy and network routing

Every operation records one route: `local-no-model`, `local-deterministic-stub`, or `blocked-unapproved-route`. There is no cloud route. Any unrecognized route, external URL, telemetry destination, model endpoint, or fallback is blocked and auditable without content logging.

The data-flow inventory covers fixture input, preserved copy, derived DB, parser scratch, renderer process, candidate cache, logs, backup, export, and normalized evidence. Each edge names data class, direction, process identity, storage lifetime, and network namespace. Synthetic credentials authorize only a run ID and have create/revoke/expire events.

## Contract B-01 — Backup, restore, and compromise recovery

Backup scope includes P-01 source packages and preservation evidence, provenance, E-01 user-controlled history, processing-rule/configuration records, and a documented database-consistent snapshot. Machine-derived state may be omitted only when the backup records that omission and rebuild inputs are complete.

- CAND-001 uses the SQLite online backup API against a quiesced experimental writer; copying an open database file is prohibited.
- CAND-003 uses `pg_dump`/`pg_restore` for the experiment and records the exact PostgreSQL version and options; successful dump verification never substitutes for a clean restore.
- A P-01/E-01 application-independent copy is present independently of either database method.
- Synthetic backup encryption uses age 1.3.2 and a disposable run-specific key. The unencrypted comparison baseline remains only in the isolated run root.
- Simulated failure domains are `backup-a/` and `backup-b/`; they demonstrate procedure, not real physical independence.

A backup becomes `verified` only after checksums, membership, declared scope/omissions, decryption when applicable, and clean isolated restore all pass. Recovery discards machine-derived state, selects an independently verified trusted source/history point, revokes synthetic credentials, restores durable state, rebuilds derived state, and reviews provenance after the trusted point.

## Result vocabulary

Each contract test records `Pass`, `Fail`, or `Blocked` using the accepted matrix. Candidate gate calibration later uses `Synthetic Pass`, `Fail`, or `Still Unproved`. A Phase-3 pass is synthetic evidence only and never a production, real-corpus, or stack-selection claim.
