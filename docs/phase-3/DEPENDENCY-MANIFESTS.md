# Proposed Dependency and Toolchain Manifests

**Status:** Accepted
**Review date:** 2026-09-17
**Acquisition state:** Nothing listed as absent has been downloaded or installed. No service or container has been started.
**Evidence checked:** 2026-09-17, from installed tool output and linked primary release/package sources.

## Dependency policy

- These pins define experimental evidence, not the Mneme product stack.
- Prefer an installed system component when it satisfies the experiment; add no convenience framework or test library.
- Direct and transitive versions are frozen before build. A missing immutable digest blocks execution until the acquisition record captures it.
- Dependency acquisition is a distinct, logged network window. Build and test execution are offline.
- Extras, optional packages, developer bundles, telemetry, automatic updates, and post-install services are excluded.
- No component may require an account, paid service, production credential, or source-data transfer.

## Recorded host baseline

| Component | Exact baseline | State | Phase-3 use |
|---|---|---|---|
| Host | Apple Silicon `arm64`, macOS 26.6.2 | Installed | Experiment host only |
| Git | Apple Git 2.54.0 | Installed | Diff and provenance evidence |
| Python | CPython 3.14.6 | Installed at `/opt/homebrew/bin/python3` | C001 runtime and one independent verifier |
| SQLite | 3.53.3 with FTS5 enabled, linked to Python | Installed | C001 derived store and Find evidence |
| OpenSSL | 3.6.3 as reported by Python | Installed | Environment evidence only; not the preservation-hash implementation contract |
| Xcode | 27.0, build 27A266a | Installed | C003 SwiftUI/WebKit probe |
| Swift | Apple Swift 6.4 (`swiftlang-6.4.0.34.1`) | Installed | C003 rendering probe |
| macOS SDK | 27.0 | Installed | C003 rendering-probe build |
| Safari/SafariDriver | 26.6.2 / system SafariDriver | Installed | C001 browser behavior probe |
| Homebrew | 6.0.21 | Installed | Inventory only; not the proposed Podman acquisition route |
| `sandbox-exec` | System binary present | Installed | Observation/fallback experiment only; not accepted as the sole isolation proof |
| Go | — | Absent | Proposed C003 runtime and second verifier |
| PostgreSQL tools/service | — | Absent | Proposed ephemeral C003 database |
| Podman | — | Absent | Proposed rootless Linux isolation/test-service harness |
| age | — | Absent | Proposed synthetic backup-encryption probe |

## EXP-C001 Python manifest

The proposed `requirements.in` has one line: `Django==6.1.1`. The fully pinned lock permits exactly the three wheels below on CPython 3.14; no optional extras are enabled.

| Package | Version | Artifact and SHA-256 | License | Primary source |
|---|---:|---|---|---|
| Django | 6.1.1 | `django-6.1.1-py3-none-any.whl`; `585fb82bf15053c42cf52e67c2f1b54a032dca384759315fd6678ab1870d1d72` | BSD-3-Clause, plus bundled Python license/notices | [Django download/support](https://www.djangoproject.com/download/), [PyPI release metadata](https://pypi.org/pypi/Django/6.1.1/json) |
| asgiref | 3.12.1 | `asgiref-3.12.1-py3-none-any.whl`; `fe386d1c2bff7259ea95929266d12a8cf9a8b5a1c2598402967d8792e7a7c094` | BSD-3-Clause | [PyPI release metadata](https://pypi.org/pypi/asgiref/3.12.1/json) |
| sqlparse | 0.6.0 | `sqlparse-0.6.0-py3-none-any.whl`; `b861c0288ce2fa56209a9a6412d2e066ac664b3873b89c26c9d8415e8e32996f` | BSD-3-Clause | [PyPI release metadata](https://pypi.org/pypi/sqlparse/0.6.0/json) |

The install must use a new temporary virtual environment, `--require-hashes`, `--no-deps`, and only the local verified wheel cache. Django’s development server is not a dependency and is used only on loopback for a bounded rendering test; it is not deployment evidence.

Python standard library modules provide hashing, JSON, MIME/email parsing for small synthetic cases, SQLite access, test execution, archive handling, and the loopback canary. No pytest, Selenium, Playwright, parser package, AI SDK, telemetry SDK, production server, or packaging framework is proposed.

## EXP-C003 Go manifest

| Component | Version | Artifact / integrity plan | License | Primary source |
|---|---:|---|---|---|
| Go toolchain | 1.27.1 | `go1.27.1.darwin-arm64.tar.gz`; SHA-256 `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` | BSD-3-Clause | [Official downloads](https://go.dev/dl/), [release policy/history](https://go.dev/doc/devel/release) |
| pgx | 5.11.0 | Go module `github.com/jackc/pgx/v5@v5.11.0`; verified by `go.sum`, module checksum database during acquisition, and offline `go mod verify` | MIT | [Changelog](https://github.com/jackc/pgx/blob/v5.11.0/CHANGELOG.md), [module file](https://raw.githubusercontent.com/jackc/pgx/v5.11.0/go.mod) |

The direct Go dependency set contains only pgx. Its published module file declares these dependencies; the acquired `go.sum` must freeze their content checksums before build:

| Module | Version in pgx 5.11.0 module file | Expected role |
|---|---:|---|
| `github.com/jackc/pgpassfile` | v1.0.0 | PostgreSQL passfile handling |
| `github.com/jackc/pgservicefile` | v0.0.0-20240606120523-5a60cdf6a761 | Service-file parsing |
| `github.com/jackc/puddle/v2` | v2.2.2 | Pool support |
| `golang.org/x/sync` | v0.17.0 | Synchronization helpers |
| `golang.org/x/text` | v0.29.0 | Text support |

`github.com/stretchr/testify` and its published indirect dependencies appear in pgx’s own module file but are not imported by the Phase-3 harness. The final offline graph from `go list -m -json all` is authoritative; any module not shown in the reviewed acquisition diff blocks build until explained. No Go web framework, ORM, migration framework, logger, telemetry library, AI SDK, or additional test library is proposed.

## Ephemeral database and isolation harness

| Component | Proposed version | Artifact / integrity rule | License posture | Primary source |
|---|---:|---|---|---|
| PostgreSQL | 18.6 | Docker Official Image tag `postgres:18.6-bookworm`; both the multi-architecture index digest and resolved `linux/arm64` image digest must be captured before pull-by-digest and frozen in `artifacts.sha256` | PostgreSQL License for database; Debian/image package licenses reported by image SBOM | [PostgreSQL 18.6 release](https://www.postgresql.org/docs/release/18.6/), [version policy](https://www.postgresql.org/support/versioning/), [official image tags](https://hub.docker.com/_/postgres) |
| Podman | 6.1.2 | Official signed macOS arm64 package from the v6.1.2 release; package digest and Apple signature/team identity must be captured and verified before installation | Apache-2.0/GPL and bundled-component notices require generated report | [Official installation guidance](https://podman.io/docs/installation), [v6.1.2 release](https://github.com/podman-container-tools/podman/releases/tag/v6.1.2) |

Podman is an experimental harness only. Docker Desktop is neither required nor authorized. No Compose file, production container configuration, startup item, login item, or durable server is created. The Podman machine is explicitly named `mneme-phase3`, has bounded CPU/memory/disk, and is stopped outside test runs.

The PostgreSQL tag is documented by the publisher, but its immutable arm64 digest is deliberately marked `ACQUISITION-BLOCKED` until registry metadata is fetched in the approved acquisition window. The database may not start from a mutable tag.

## Backup-encryption probe

| Component | Version | Artifact and SHA-256 | License | Primary source |
|---|---:|---|---|---|
| age | 1.3.2 | `age-v1.3.2-darwin-arm64.tar.gz`; `e2020b073c44f692685a24d6abc378817eb81ffaaf49fd0531ef8565f767f2f5` | BSD-3-Clause | [Official release and assets](https://github.com/FiloSottile/age/releases/tag/v1.3.2) |

Age is used only with disposable synthetic keys and synthetic backups. It is not a production encryption decision.

## Rendering dependencies

- C001 uses Django templates, browser-native sandbox/CSP behavior, and the installed SafariDriver. No JavaScript package, sanitizer package, Node runtime, browser download, or browser automation framework is added.
- C003 uses SwiftUI, WebKit, XCTest, and system SDKs from Xcode 27.0. No Swift Package Manager dependency, signing identity, provisioning profile, App Store/TestFlight service, or external device service is used.
- If the installed Safari/WebKit or Xcode toolchain changes before execution, the manifest is revised and reviewed; it is not silently floated.

## SBOM, license, and build evidence

No third-party SBOM generator is added. The reviewed harness will normalize these built-in inventories into SPDX 2.3 JSON:

- Python: lock file, verified wheel metadata, `python -m pip inspect --local`, wheel `METADATA`, and license files;
- Go: `go env`, `go version -m`, `go list -m -json all`, `go mod verify`, `go.sum`, and repository license files;
- OCI: immutable image/index digests, `podman image inspect`, image labels/history, and installed-package inventory exported from the image without network;
- Apple: `xcodebuild -version`, `swift --version`, SDK version, linked system frameworks, and test-bundle build metadata;
- standalone binaries: artifact digest, signature/proof status, embedded version, and bundled license files.

The license report lists component, version, copyright/notice source, SPDX expression where known, distribution obligation, and unresolved issue. The advisory report records the official security route checked and date. A generated SBOM is evidence only after its component count is reconciled with lock/module/image inventories.

## Acquisition allowlist

Only these hosts are proposed during the isolated acquisition window:

- `files.pythonhosted.org` and `pypi.org` for the three exact Python wheels and metadata;
- `go.dev` for the exact Go archive;
- `proxy.golang.org` and `sum.golang.org` for the frozen Go module graph, with requested module/version logs retained;
- `github.com`, `objects.githubusercontent.com`, and `release-assets.githubusercontent.com` for the exact Podman and age release artifacts and license sources;
- `registry-1.docker.io`, `auth.docker.io`, and `production.cloudflare.docker.com` solely for the digest-pinned PostgreSQL Official Image.

No fixture, source record, project evidence, credential, or identifier is sent during acquisition. Any additional host or component requires a revised manifest before access.

## Freeze conditions before build

Build remains prohibited until:

1. every artifact has exact version, source URL, byte length, SHA-256 or ecosystem checksum, signature/proof status, and license source;
2. the PostgreSQL index and arm64 image digests are captured and the mutable tag is replaced by digest reference;
3. `requirements.lock`, `go.sum`, OCI inventory, acquisition log, and `artifacts.sha256` are complete and reviewed for unexpected entries;
4. all artifacts are present in a local cache and an offline completeness check passes;
5. SBOM and license/notice generation procedures run without adding a dependency;
6. no component requires an account, post-install network, telemetry, public listener, production credential, or unreviewed native extension.

Failure keeps the affected candidate at `Still Unproved`; it does not justify substituting an unreviewed package.
