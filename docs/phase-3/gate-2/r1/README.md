# R1 Primary-Evidence Route Dossiers

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**R1 outcome:** Complete for review. No acquisition route is authorized by this package.

## Purpose

This package records publisher-controlled evidence for the four unresolved Checkpoint-A acquisition routes. It identifies exact artifacts, versions, redirect expectations, integrity and signature mechanisms, licenses, side effects, narrowly scoped future host changes, and rollback boundaries.

R1 is documentation research only. No binary, package, module, proof verifier, OCI blob, image, installer, or generated artifact was acquired or retried while preparing it.

## Package

| Dossier | R1 finding |
|---|---|
| [Podman Route](PODMAN-ROUTE-DOSSIER.md) | The v6.1.2 package route remains blocked: publisher documentation says release artifacts are signed, but the exact package has an invalid macOS signature and an incomplete official rollback story |
| [Go Route](GO-ROUTE-DOSSIER.md) | Publisher evidence establishes `dl.google.com` as the Go release CDN; the toolchain route can be proposed for R2, while module payload acquisition remains gated on graph approval |
| [age Route](AGE-ROUTE-DOSSIER.md) | The archive is exact, but proof verification requires a separately reviewed `sigsum-verify` trust chain; the route is not R2-ready |
| [PostgreSQL OCI Route](POSTGRESQL-OCI-ROUTE-DOSSIER.md) | Docker's official allowlist confirms `production.cloudfront.docker.com`; a digest-only, fourteen-blob route can be proposed for R2 |
| [Proposed Route Changes](PROPOSED-ROUTE-CHANGES.md) | Exact future manifest/allowlist changes and the unresolved decisions that precede R2 |

## Status vocabulary

- **R2-ready:** Primary evidence is sufficient to draft an exact manifest and allowlist change, but no change or acquisition is yet authorized.
- **Conditionally R2-ready:** The route is exact only after a named prerequisite dossier is accepted.
- **Blocked:** Primary evidence exposes an unresolved trust, dependency, side-effect, license, or rollback gap.
- **Deferred:** The route is intentionally removed from the claimed evidence scope; affected gates remain Unproved.

R2-ready does not mean acquired, verified, installed, or passed.

## Route summary

| Route | Exact artifact/content | Proposed disposition | Proposed host change |
|---|---|---|---|
| Podman P1 | `podman-installer-macos-arm64.pkg`, v6.1.2 | Blocked; do not reacquire or install | None |
| Go G1 | `go1.27.1.darwin-arm64.tar.gz` | R2-ready for a download-only route | Add `dl.google.com` for this exact path only |
| Go G2/G3 | pgx graph plus eight discovered modules | Metadata-graph review first; ZIP payloads remain blocked | None now; continue to constrain future traffic to `proxy.golang.org` and `sum.golang.org` |
| age A1 | Existing age v1.3.2 archive/proof plus `sigsum-verify@v0.13.1` | Blocked until the verifier's exact graph is reviewed | None now |
| PostgreSQL O1 | Frozen arm64 config plus thirteen layer blobs | R2-ready for digest-only download | Replace erroneous `production.cloudflare.docker.com` proposal with `production.cloudfront.docker.com` |

## Primary-source boundary

Evidence came from:

- official project/release repositories and release-process documentation;
- Go's official download, module, source, and license documentation;
- the age project's official release, README, Sigsum policy, and license;
- Sigsum's official documentation and source-repository metadata;
- Docker's official registry API, allowlist, Hub metadata, and Docker Official Images repositories;
- PostgreSQL's official license page;
- the already accepted Checkpoint-A request, redirect, hash, signature, package-script, and OCI-manifest evidence.

Third-party package or mirror routes are not proposed.

## Preserved boundary

- Checkpoint A remains incomplete and open.
- Gate 2 remains not passed.
- G2-C12 remains Verified only for acquisition-stop behavior observed at Checkpoint A.
- No stack has been selected.
- R2, R3, R4, Checkpoint B, installation, execution, fixtures, services, builds, and tests remain paused.

## Review request

Review is requested on the route facts, proposed host changes, blocked/deferred classifications, and exact R2 prerequisites. Acceptance of R1 would authorize no network acquisition by itself.
