# ADR-002: Preservation Contract

**Status:** Accepted
**Phase:** 1 — Preservation Foundation

## Context

The source archive is Mneme's system of record. Search, classifications, annotations, and AI work must never compromise the ability to recover the original record or explain how derived data was produced.

## Proposal

The preservation contract will require:

- byte-preserving retention of each accepted source item;
- hashes and manifests sufficient to detect loss, substitution, or unintended change;
- provenance for source acquisition, transformations, parsers, processing rules, and derived outputs;
- an application-independent export that does not require Mneme to interpret the preserved record;
- backups with documented scope, integrity checks, retention, and access controls;
- restore verification at defined intervals and after material changes;
- rebuildability of derived data from the source archive and recorded processing rules;
- separation of the read-only source archive from reversible, user-controlled derived annotations and classifications.

No file format, database, storage engine, filesystem, container, or implementation stack is selected here.

## Alternatives considered

- Preserve only normalized fields: rejected because normalization can lose source fidelity and provenance.
- Treat indexes or AI summaries as the archive: rejected because derived data is replaceable and must not become the sole record.

## Consequences

Preservation, recovery, and auditability become acceptance criteria rather than later conveniences. Storage and processing choices may be constrained by this contract, but remain open for a later approved decision.

## Approval boundary

Acceptance of this ADR authorizes requirements and design work only. It does not authorize real-data import, provider authentication, or implementation-stack selection.
