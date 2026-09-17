# ADR-006: Separately Approved Real-Data Dry Run

**Status:** Accepted
**Phase:** 1 — Preservation Foundation

## Context

Real correspondence is necessary for eventual validation, but importing it before preservation and security controls are accepted would create irreversible privacy and integrity risks.

## Proposal

Treat the first real-data operation as a separate approval gate and staged dry run. Before it begins, document:

- the user-selected source and narrowly bounded corpus slice;
- purpose, scope, consent, and explicit data exclusions;
- authentication and credential handling, including OAuth scopes if applicable;
- source-byte, hash, manifest, provenance, backup, and rollback checks;
- quarantine, parser isolation, resource limits, and network boundaries;
- whether any cloud service or AI model receives data;
- success criteria, stop conditions, incident handling, and recovery steps;
- deletion or retention of temporary copies, without deleting the preserved source archive.

The dry run must begin with metadata and preservation verification, proceed only with explicit authorization, and stop on integrity mismatch, unexpected data exposure, parser safety failure, credential concern, or any unexplained behavior.

## Alternatives considered

- Import the full corpus first: rejected because failures would have a larger blast radius.
- Use production-like external services during the first dry run: rejected unless separately approved and necessary after local controls are verified.

## Consequences

Real-data use becomes deliberate, narrow, auditable, and recoverable. It may delay convenience, but preserves the user's control and makes failures observable before scale.

## Approval boundary

This proposal authorizes planning only. It does not authorize authentication, inspection, download, import, indexing, classification, AI processing, cloud transfer, or production deployment.
