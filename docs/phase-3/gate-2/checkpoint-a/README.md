# Phase-3 Gate-2 Checkpoint-A Evidence

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Checkpoint outcome:** Incomplete; fail closed. Checkpoint B is not authorized by this package.

## Purpose

This package records the dependency-acquisition and integrity evidence produced under the user's Checkpoint-A authorization. It is evidence about experimental prerequisites only. It does not select a stack, authorize candidate implementation, or change the Phase-2 no-selection finding.

The acquisition process followed the accepted rule that a mismatch is a stop condition, not permission to substitute another source or component. The Python wheel set was fully acquired and verified. The Go toolchain, complete Go graph, Podman installer, age executable archive, and PostgreSQL image content did not satisfy all accepted controls and therefore were not retained as executable inputs.

## Package contents

| Document | Contents |
|---|---|
| [Acquisition Register](ACQUISITION-REGISTER.md) | Artifact-by-artifact URLs, versions, filenames, sizes, hashes, retained state, and disposition |
| [Integrity and Signature Report](INTEGRITY-AND-SIGNATURE-REPORT.md) | Independent hash checks, signatures/proofs, archive inspection, OCI digests, and installer-side-effect findings |
| [Dependency and License Report](DEPENDENCY-AND-LICENSE-REPORT.md) | Python and Go dependency graphs, license evidence, OCI inventory limits, and unresolved components |
| [Network and Redirect Report](NETWORK-AND-REDIRECT-REPORT.md) | Allowlisted requests, redirects, blocked hosts, credential handling, and network-window closure |
| [Cache and Cleanup Report](CACHE-AND-CLEANUP-REPORT.md) | Retained cache/evidence, removed executable artifacts, installation absence, and repository boundary |
| [Checkpoint-A Decision](CHECKPOINT-A-DECISION.md) | Fail-closed conclusion, Gate-2 control updates, blockers, and approval boundary |

## Outcome summary

| Acquisition slice | Outcome | Reason |
|---|---|---|
| Django 6.1.1 and its two required wheels | Verified and retained | Exact versions and hashes matched accepted pins and PyPI metadata; wheels are pure Python; metadata and licenses were captured |
| Go 1.27.1 toolchain | Rejected before download | `go.dev` redirected to unallowlisted `dl.google.com` |
| Six reviewed Go modules | Metadata retained; executable archives rejected | The Go verifier was unavailable and published module files exposed eight undeclared graph members |
| Podman 6.1.2 installer | Rejected and removed | Published hash matched, but macOS reported an invalid package signature and scripts disclosed unapproved destructive/privileged side effects |
| age 1.3.2 archive | Rejected and removed | Exact hash matched, but the Sigsum proof could not be verified and the binary had only an ad-hoc linker signature |
| PostgreSQL 18.6 OCI metadata | Index and arm64 manifest verified and retained | Registry headers and independent hashes agreed on immutable digests |
| PostgreSQL 18.6 OCI content | Rejected before blob transfer | Registry blob retrieval redirected to unallowlisted `production.cloudfront.docker.com`; the accepted manifest instead named `production.cloudflare.docker.com` |

## Scope preserved

- No candidate code was built or installed.
- No fixture, credential, key, Podman machine, container, database, listener, service, prototype, or test was created or run.
- No account, real correspondence, live archive, cloud AI, external embedding service, telemetry, analytics, production infrastructure, or public endpoint was accessed.
- No stack was selected and no stack-selection ADR was created.
- No acquisition artifact was added to Git or placed in the repository.
- Nothing was pushed.

## Evidence location and durability

The review cache is outside the repository at `/tmp/mneme-phase3-checkpoint-a.H9KN5d`. It is an owner-only disposable directory with the sentinel `MNEME_PHASE3_DISPOSABLE.json`. At review time it contains approximately 8.5 MB: three verified Python wheels, non-executable Go metadata and checksum-database records, an age proof, Podman checksum and inspection evidence, two OCI metadata documents, normalized inventories, checksums, licenses, and signature reports.

The `/tmp` location is intentionally temporary and is not a preservation store. This documentation is the durable normalized record proposed for the repository. The raw cache must remain uncommitted. Any future removal must validate the exact path, owner, sentinel, and inventory first; no broad deletion or global prune is permitted.

## Review boundary

Checkpoint A is not complete enough to proceed. Review is requested on the recorded evidence and the blockers in `CHECKPOINT-A-DECISION.md`. Checkpoint B, fixture creation, dependency installation, service initialization, and prototype work remain paused.
