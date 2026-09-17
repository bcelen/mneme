# Preservation-Contract Requirements

**Status:** Accepted
**Review date:** 2026-09-17
**Authority:** ADR-002
**Implementation status:** No format, algorithm, storage engine, filesystem, database, library, or stack is selected.

## Purpose and terms

This contract defines observable preservation obligations for any future Mneme implementation.

- **Source archive:** The read-only, byte-preserving system of record containing approved source packages and their preservation evidence.
- **Source package:** The bounded set of files and contextual metadata acquired together through a separately approved operation.
- **Source item:** A preserved file, container, message representation, attachment, sidecar, or metadata object within a source package.
- **Manifest:** An application-independent inventory connecting stable identifiers, paths or object references, sizes, hashes, and provenance.
- **Provenance event:** A recorded acquisition, verification, parsing, transformation, export, backup, restore, or rebuild action.
- **Derived data:** Anything computed, extracted, linked, classified, summarized, indexed, or annotated from the source archive.
- **Reversible derived data:** Derived data that is either undoable through recorded history or fully reconstructible from the source archive and recorded processing rules.

## Normative requirements

### Source boundary and byte fidelity

| ID | Requirement | Verification evidence |
|---|---|---|
| PRES-001 | Preserve every accepted source package exactly as supplied before parsing or transformation. | Pre-ingest and post-preservation byte comparison over the complete package. |
| PRES-002 | Never rewrite, normalize, repair, deduplicate, rename in place, or delete source-archive bytes as a processing side effect. | Read-only boundary test, mutation attempt test, and audit evidence. |
| PRES-003 | Preserve container files, sidecars, directory context, and acquisition context needed to interpret the package; do not retain only extracted messages. | Package manifest and source-family completeness checklist. |
| PRES-004 | Record ambiguous encodings, line endings, separators, timestamps, and malformed structures without silently changing the source. | Fixture tests showing original bytes remain unchanged and ambiguity is reported. |
| PRES-005 | Separate source-archive identifiers from filenames, provider IDs, parsed IDs, and derived entity identifiers. | Traceability review demonstrating each namespace remains distinguishable. |

### Integrity hashes and manifests

| ID | Requirement | Verification evidence |
|---|---|---|
| PRES-006 | Compute at least one approved cryptographic content hash for each preserved file or object and for each source package as a whole. | Known-answer tests and manifest inspection; algorithm choice deferred. |
| PRES-007 | Record byte length, hash algorithm identifier, digest, acquisition time, verification time, and source-package membership in an application-independent manifest. | Manifest completeness test. |
| PRES-008 | Make manifests tamper-evident or independently verifiable and store them so corruption of one storage location cannot silently redefine integrity. | Tamper test and independent verification procedure. |
| PRES-009 | Treat a hash mismatch, missing manifest member, unexpected extra member, or size mismatch as an integrity failure that stops downstream processing. | Negative acceptance tests for each mismatch class. |
| PRES-010 | Version manifest conventions and retain the ability to verify older manifests after conventions evolve. | Compatibility test across at least two synthetic manifest versions before change acceptance. |

### Provenance and traceability

| ID | Requirement | Verification evidence |
|---|---|---|
| PRES-011 | Assign stable, non-secret identifiers to source packages, source items, provenance events, and derived artifacts without embedding personal data. | Identifier review and repeat-import test. |
| PRES-012 | Record who or what initiated an acquisition, the approved scope, acquisition route, timestamps, tool/version identity, and outcome without storing credentials. | Provenance completeness review using synthetic acquisitions. |
| PRES-013 | Record every parser, transformation, processing rule, and model operation that contributes to derived data, including version/configuration identity and source inputs. | End-to-end lineage query over the synthetic corpus. |
| PRES-014 | Allow every derived assertion presented to the user to trace to source items and relevant processing events, or be explicitly marked unsupported or user-authored. | Citation and lineage acceptance tests. |
| PRES-015 | Preserve superseded provenance and derived-history records needed for audit or undo; corrections append history rather than falsifying prior events. | Correction/undo test with history inspection. |

### Exportability and independence

| ID | Requirement | Verification evidence |
|---|---|---|
| PRES-016 | Export the source archive, manifests, provenance, and user-controlled derived data without requiring a running Mneme instance to read the preserved bytes and integrity evidence. | Clean-environment export inspection using independent tools. |
| PRES-017 | Document every exported element, omission, relationship, and version so an independent implementation can interpret the package. | Export documentation completeness review. |
| PRES-018 | Preserve source bytes in exports exactly; export must not substitute normalized or parsed representations for source items. | Hash equality between source archive and export. |
| PRES-019 | Make export repeatable and ensure identical preserved inputs produce equivalent content even if packaging metadata such as creation time differs. | Repeated export comparison with documented allowed variance. |
| PRES-020 | Report partial export, missing data, unsupported derived fields, or integrity failure prominently; never label a partial result as complete. | Fault-injection export tests. |

### Backups and restore verification

| ID | Requirement | Verification evidence |
|---|---|---|
| PRES-021 | Define backup scope for source bytes, manifests, provenance, configuration needed for interpretation, user-controlled derived history, and secrets handled through a separate recovery process. | Reviewed backup inventory with exclusions justified. |
| PRES-022 | Maintain independent failure domains appropriate to the approved risk model; exact media, count, and location are later operational decisions. | Documented failure-domain analysis. |
| PRES-023 | Encrypt and access-control backup copies according to their sensitivity, while preserving a tested recovery path for keys and credentials. | Access test and key-loss recovery exercise using synthetic data. |
| PRES-024 | Verify backup integrity on creation and at a documented interval; verification includes hashes and manifest completeness rather than file presence alone. | Scheduled synthetic verification evidence. |
| PRES-025 | Perform a clean restore into an isolated location at a documented interval and after material backup-process changes. | Restore drill report and independent integrity comparison. |
| PRES-026 | Define and review recovery-point and recovery-time objectives before production use; this contract does not set their values. | Approved operational decision before production gate. |
| PRES-027 | Ensure backup retention and deletion policies cannot delete the only valid source copy or silently erase required provenance. | Retention simulation and approval review. |

### Rebuildability and derived data

| ID | Requirement | Verification evidence |
|---|---|---|
| PRES-028 | Rebuild all machine-derived indexes, extractions, classifications, embeddings, summaries, and relationships from the source archive plus recorded rules and versioned inputs. | Empty-derived-state rebuild over the synthetic corpus. |
| PRES-029 | Preserve user-authored annotations and corrections through recorded history sufficient for undo when they cannot be reconstructed from source and processing rules; include them in the application-independent export according to the approved history-retention policy. | User-derived-data restore and undo tests. |
| PRES-030 | Distinguish deterministic rebuilds from nondeterministic model outputs and record the model, parameters, context, and citations needed to explain the latter. | Rebuild report identifying deterministic equality and allowed nondeterminism. |
| PRES-031 | Permit complete deletion and recreation of machine-derived data without modifying the source archive. | Derived-state destruction/rebuild test using synthetic data only. |
| PRES-032 | Detect processing-rule or version changes that make derived data stale and prevent silent mixing of incompatible generations. | Version-change invalidation test. |
| PRES-033 | Produce a rebuild report listing inputs, versions, outputs, failures, skips, and integrity status. | Report completeness acceptance test. |

## Failure policy

An integrity mismatch, unknown source-package boundary, missing required manifest, provenance gap, unsafe parser outcome, or unexplained source mutation is a stop condition. The affected source package remains quarantined; no downstream index, classification, or AI operation may represent it as successfully preserved.

## Deferred decisions

Hash algorithms, manifest serialization, identifier format, storage layout, backup topology, encryption mechanism, retention periods, recovery objectives, and implementation technologies remain open. A later decision must show that each choice satisfies this contract and the acceptance-test matrix.
