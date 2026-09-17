# Checkpoint-A Dependency and License Report

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18

## Python graph

For CPython 3.14 on macOS, Django 6.1.1 requires `asgiref>=3.9.1` and `sqlparse>=0.5.0`. Its `tzdata` condition applies only on Windows. The selected exact graph is therefore Django 6.1.1, asgiref 3.12.1, and sqlparse 0.6.0. Optional extras and development/test dependencies were not selected.

| Component | Selected version | License evidence | Unresolved issue |
|---|---:|---|---|
| Django | 6.1.1 | Wheel license metadata and bundled BSD-3-Clause license; bundled Python license/notices retained | None at acquisition stage |
| asgiref | 3.12.1 | Wheel license metadata and BSD-3-Clause license retained | None at acquisition stage |
| sqlparse | 0.6.0 | Wheel license file identifies BSD-3-Clause; PyPI metadata lacks a normalized license expression | Normalize SPDX expression in eventual SBOM from the retained license text |

No native extension or platform wheel was introduced. No package was installed, so an installed-environment SBOM does not yet exist.

## Go graph

The six modules explicitly identified by the accepted manifest were acquired for metadata inspection only:

| Module | Version | License evidence |
|---|---:|---|
| `github.com/jackc/pgx/v5` | v5.11.0 | MIT license retained |
| `github.com/jackc/pgpassfile` | v1.0.0 | MIT license retained |
| `github.com/jackc/pgservicefile` | v0.0.0-20240606120523-5a60cdf6a761 | MIT license retained |
| `github.com/jackc/puddle/v2` | v2.2.2 | MIT license retained |
| `golang.org/x/sync` | v0.17.0 | BSD-3-Clause-style Go project license retained |
| `golang.org/x/text` | v0.29.0 | BSD-3-Clause-style Go project license retained |

Published module files revealed these additional modules, which were not acquired because they were undeclared components under the Checkpoint-A authorization:

| Undeclared module | Selected or required version | Discovery source |
|---|---:|---|
| `github.com/stretchr/testify` | v1.11.1 | pgx module file; supersedes older constraints |
| `github.com/davecgh/go-spew` | v1.1.1 | pgx module file |
| `github.com/kr/pretty` | v0.3.0 | pgx module file |
| `github.com/pmezard/go-difflib` | v1.0.0 | pgx module file |
| `gopkg.in/check.v1` | v1.0.0-20201130134442-10cb98267c6c | pgx module file |
| `gopkg.in/yaml.v3` | v3.0.1 | pgx module file |
| `golang.org/x/tools` | v0.36.0 | x/text module file |
| `golang.org/x/mod` | v0.27.0 | x/text module file |

The accepted manifest anticipated that `testify` appeared in pgx's module file and stated that the authoritative offline graph would come from `go list -m -json all`. It did not authorize acquiring `testify` or the other seven modules before their appearance in a reviewed acquisition diff. The acquisition therefore stopped rather than silently broadening scope.

Without Go 1.27.1, the graph cannot yet be authoritatively minimized or classified as build-, test-, or module-graph-only input. Their licenses and integrity remain unreviewed. The retained `go.sum.partial` is explicitly marked partial and contains only the six reviewed modules; it is not a build lock.

## Podman and age

| Component | Version | License evidence | Dependency/inventory limit |
|---|---:|---|---|
| Podman | 6.1.2 | Top-level Apache-2.0/GPL and release license material retained | Package rejected; payload component notices were not normalized into an SBOM or complete transitive license report |
| age | 1.3.2 | BSD-3-Clause license retained | Archive rejected; no installed-binary inventory or verifier dependency was introduced |

Neither component was installed. Retaining a top-level license does not resolve bundled-component obligations for Podman.

## PostgreSQL OCI image

The verified arm64 manifest records content digests but the config and thirteen layers were not downloaded. Consequently the image's Debian package list, package versions, transitive runtime contents, notices, and license files are unknown. The PostgreSQL License for the database does not by itself describe the full Docker Official Image.

**License finding:** Blocked until image content can be acquired from an approved immutable route and inventoried offline.

## SBOM status

No SBOM was generated because no candidate environment was installed and the OCI content is incomplete. The following SBOM inputs exist:

- exact Python lock, wheel metadata, hashes, and license files;
- partial Go module metadata, content hashes, checksum-database records, and six license files;
- Podman package metadata, scripts, payload listing, published checksum, license, and signature result;
- age artifact/proof hashes, license, and code-signature result;
- PostgreSQL OCI index and arm64 manifest with config/layer descriptors.

Calling those inputs a complete SBOM would overstate the evidence. Component-count reconciliation remains blocked for Go, Podman, and PostgreSQL.
