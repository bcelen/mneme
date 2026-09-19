# First Synthetic Mneme Vertical Slice: Implementation Approval

**Status:** Accepted
**Prepared:** 2026-09-19
**Review date:** 2026-09-20
**Decision requested:** Approve one bounded implementation and test pass under the scope below. This is not a new phase plan or a stack-selection decision.

## Purpose

Build the smallest end-to-end Mneme path that proves the central product contract:

> synthetic EML -> byte-preserved source plus SHA-256 manifest -> minimal derived metadata and index -> deterministic Find -> source display with provenance and citation

The slice is local, offline, synthetic-only, disposable, and reversible. It must use one already-installed local runtime and its standard library only. The runtime identity must be recorded with the results, but its use here does not select the Mneme implementation stack.

## Authorized implementation boundary

All new implementation, fixture, and test files must remain under `experiments/vertical-slice-1/`. The later evidence report may be added as `docs/SYNTHETIC-VERTICAL-SLICE-RESULTS.md`. Generated execution state must use a fresh temporary directory and must not be committed.

The implementation may:

1. create one wholly fictional, inert, plain-text EML fixture using reserved example addresses;
2. copy that fixture byte-for-byte into a temporary source archive before parsing;
3. record an application-independent manifest containing a stable synthetic source ID, byte count, SHA-256 digest, source-package membership, provenance, and processing version;
4. derive only the fields needed for the slice, such as sender, recipients, date, subject, message ID, and searchable plain text;
5. build a minimal disposable index from the derived record;
6. run deterministic Find with specified normalization, stable result ordering, and repeatable citations;
7. display the preserved source as inert text together with its source ID, SHA-256, provenance, and an unambiguous line or byte locator; and
8. if useful for citation-flow testing, add a deterministic Ask stub that accepts only Find results and produces a fixed template with their citations. It may not call a model or generate unsupported claims.

No existing accepted document or pending document may be changed. In particular, the six documents already awaiting disposition, `tools/handoff/`, and the halted checksum-planner work are outside this approval.

## Required behavior and evidence

The implementation and tests must demonstrate:

- the preserved copy is byte-identical to the fixture and independently matches the manifest SHA-256 and byte count;
- parsing and indexing never alter the fixture or preserved copy;
- a missing member, changed byte, size mismatch, or hash mismatch stops derivation and Find;
- every derived field and Find result traces to the source ID, source digest, processing rule/version, and relevant source locator;
- repeating the same query against the same generation returns the same ordered results and citations;
- deleting all derived state and rebuilding it from the preserved source and recorded rules reproduces the deterministic metadata, index, results, and citations;
- source display resolves a citation back to the preserved bytes without interpreting HTML or loading external content;
- the optional Ask stub cites only supplied Find results and returns an explicit insufficient-evidence response when no result supports the question;
- execution creates no network traffic, listener, persistent service, account access, telemetry, or state outside the declared temporary root; and
- the final review includes the complete diff, fixture and file hashes, runtime identity, commands run, test results, temporary-root inventory, and cleanup result.

These checks provide narrow evidence for `PRES-001`, `PRES-006` through `PRES-009`, `PRES-011` through `PRES-014`, `PRES-028`, `PRES-031`, `AT-P01`, `AT-P03` through `AT-P05`, `AT-L01`, `AT-L03`, `AT-M07`, and, if the stub is included, the citation boundary of `AT-M08`. They do not claim full satisfaction of those requirements beyond this fixture and slice.

## Explicit exclusions

This approval does not permit accounts, real correspondence, cloud AI, external embeddings, network access, dependency acquisition, containers, databases, persistent services, deployment, production configuration, mobile clients, hostile-content parsing, attachments, sending email, mutation of source data, handoff-automation use, route screening, checksum-planner work, stack selection, commit, or push.

## Failure, rollback, and review

Stop on any scope expansion, source mutation, integrity mismatch, provenance gap, nondeterministic Find result, unsupported citation, network attempt, dependency request, persistent process, write outside the authorized paths or temporary root, or contact with real data. Preserve the failure evidence and do not work around the condition.

Rollback consists of removing the isolated temporary execution root and, only after review, the newly created `experiments/vertical-slice-1/` and results document. No rollback may alter the six pending documents or any previously accepted record.

Approval of this proposal authorizes the bounded implementation and its synthetic tests as one unit. It does not accept their outcome. The complete implementation diff and evidence must return for preservation, security/privacy, and quality review before any commit or follow-on work.
