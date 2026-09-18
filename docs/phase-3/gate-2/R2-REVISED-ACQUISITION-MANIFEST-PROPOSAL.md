# R2 Revised Acquisition Manifest Proposal

**Status:** Accepted
**Review date:** 2026-09-18
**Proposal date:** 2026-09-18
**Current authority:** Documentation and review only. No manifest or allowlist change in this proposal is applied.

## Purpose

This R2 proposal translates the accepted R1 route dossiers into an exact, staged acquisition-manifest and host/path-allowlist change for later review. It does not authorize a network request, installation, extraction, execution, service, fixture, build, test, or prototype.

The governing inputs are:

- the accepted [Checkpoint-A Remediation Proposal](CHECKPOINT-A-REMEDIATION-PROPOSAL.md);
- the accepted [Checkpoint-A evidence package](checkpoint-a/README.md);
- the accepted [R1 route dossiers](r1/README.md); and
- the accepted Phase-3 [dependency policy](../DEPENDENCY-MANIFESTS.md) and [rollback contract](../ROLLBACK-AND-CLEANUP.md).

Checkpoint A remains incomplete, Gate 2 remains not passed, and no stack has been selected.

## Route decisions preserved

| Route | R2 disposition | Consequence |
|---|---|---|
| Podman 6.1.2 | **Blocked and deferred** | Remove the package from acquirable inputs. Container-backed evidence and every Podman-dependent control remain `Blocked` or `Unproved`. |
| Go 1.27.1 toolchain | **Eligible for a separately approved R3-G1 archive-only request** | Use only the exact `dl.google.com` archive route. Stop after byte/hash/archive evidence; do not execute the toolchain or acquire module payloads. |
| Go module graph | **Metadata-only boundary proposed; payloads blocked** | The six retained module metadata records and eight named candidates define the initial graph envelope. No `.zip` payload may be requested before authoritative graph review and approval. |
| age 1.3.2 | **Blocked** | Do not reacquire the archive or acquire/build `sigsum-verify`. The exact verifier graph and v1.3.2 proof-policy compatibility remain prerequisites. |
| PostgreSQL 18.6 OCI content | **Eligible for a separately approved R3-O1 digest-only request** | Request only one accepted config and thirteen accepted layers, through the exact anonymous registry/CDN route. Never request the mutable tag. |

R2 does not combine the Go and PostgreSQL routes into one acquisition authorization. Each later R3 workstream requires its own explicit user approval and evidence stop.

## Exact proposed manifest changes

The following changes are proposed for the accepted dependency manifest. They are stated here for review and are **not** applied to `docs/phase-3/DEPENDENCY-MANIFESTS.md`.

### Recorded-host baseline

| Existing component | Proposed replacement state | Proposed replacement Phase-3 use |
|---|---|---|
| Go — Absent | `Absent; exact archive route accepted at R1 and proposed at R2` | Archive acquisition only after separate R3-G1 approval; no execution until another approval |
| PostgreSQL tools/service — Absent | `Absent; exact arm64 OCI metadata retained; content incomplete` | Digest-only content acquisition after separate R3-O1 approval; no import or service |
| Podman — Absent | `Absent; blocked and deferred` | No acquisition, installation, machine, container, socket, or substitute runtime |
| age — Absent | `Absent; blocked pending verifier trust chain` | No reacquisition, verifier, execution, key, or encryption probe |

### Go toolchain entry

Replace the proposed Go artifact route with:

| Component | Version | Exact artifact | Expected size | Integrity/signature | License | State |
|---|---:|---|---|---|---|---|
| Go toolchain | 1.27.1 | `https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz` | Publisher-rounded `65 MB`; exact byte count is an acquisition evidence field | SHA-256 `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12`; no detached signature advertised | BSD-style Go license | Proposed for R3-G1 archive-only acquisition |

The request is direct to the accepted publisher CDN, so no redirect is expected. Any redirect, alternate host, different filename, different version, authentication request, or mismatched hash is a stop. The absence of a publisher-provided exact byte count is recorded as uncertainty `U-R2-GO-01` and was explicitly accepted at Gate R2-A. The independently recorded response byte count and SHA-256 are authoritative; the publisher's rounded 65 MB description is not an acceptance value. The response byte count and any `Content-Length` must be recorded and agree before the archive can be retained.

R3-G1 may acquire and statically inspect the archive only. Extraction, `go version`, checksum-database verification, graph calculation, compilation, installation, profile changes, and module requests remain outside that workstream.

### Go graph boundary

The initial metadata envelope contains these fourteen modules and no others:

| Class | Module | Version | R2 payload authority |
|---|---|---:|---|
| Direct | `github.com/jackc/pgx/v5` | v5.11.0 | None; retained `.info`, `.mod`, and checksum evidence only |
| Published pgx dependency | `github.com/jackc/pgpassfile` | v1.0.0 | None; retained metadata only |
| Published pgx dependency | `github.com/jackc/pgservicefile` | v0.0.0-20240606120523-5a60cdf6a761 | None; retained metadata only |
| Published pgx dependency | `github.com/jackc/puddle/v2` | v2.2.2 | None; retained metadata only |
| Published pgx dependency | `golang.org/x/sync` | v0.17.0 | None; retained metadata only |
| Published pgx dependency | `golang.org/x/text` | v0.29.0 | None; retained metadata only |
| Metadata candidate | `github.com/stretchr/testify` | v1.11.1 | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |
| Metadata candidate | `github.com/davecgh/go-spew` | v1.1.1 | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |
| Metadata candidate | `github.com/kr/pretty` | v0.3.0 | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |
| Metadata candidate | `github.com/pmezard/go-difflib` | v1.0.0 | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |
| Metadata candidate | `gopkg.in/check.v1` | v1.0.0-20201130134442-10cb98267c6c | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |
| Metadata candidate | `gopkg.in/yaml.v3` | v3.0.1 | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |
| Metadata candidate | `golang.org/x/tools` | v0.36.0 | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |
| Metadata candidate | `golang.org/x/mod` | v0.27.0 | None; `.info`/`.mod` may be proposed only at a later G2 approval gate |

After a verified toolchain exists and a new approval is given, G2 would use an isolated, source-free main module with exactly:

```text
module example.invalid/mneme-phase3-graph

go 1.27.1

require github.com/jackc/pgx/v5 v5.11.0
```

The workspace is a future disposable graph input, not candidate code. Its only permitted outputs would be the selected module list, module-graph edges, classifications, exact `.info`/`.mod` requests, checksum lookups, and unresolved members. Discovery of a fifteenth module stops the metadata pass. No `.zip` endpoint, source checkout, direct VCS fallback, package import, compilation, or test is permitted before a separately accepted G3 graph record.

The current `go.sum.partial` remains partial evidence and must not be renamed or represented as a build lock.

### Podman entry

Replace the Podman acquisition row and related package language with:

| Component | Version | Artifact identity | State | Gate effect |
|---|---:|---|---|---|
| Podman | 6.1.2 | `podman-installer-macos-arm64.pkg`, SHA-256 `88def43af7fbe7baf40fc2f12d69267f6d845768020709900fb1b8c3bfe015b3` | `BLOCKED-SIGNATURE-AND-ROLLBACK`; deferred; not acquirable | Container-backed, rootless-isolation, and Podman-dependent evidence stays `Blocked` or `Unproved` |

No package-manager route, alternate runtime, source build, replacement version, or installer exception is implied. The package's matching hash does not override its invalid macOS signature, privileged/destructive scripts, or incomplete bounded rollback.

### age entry

Replace the age acquisition row with:

| Component | Version | Existing evidence | State | Missing evidence |
|---|---:|---|---|---|
| age | 1.3.2 | Archive SHA-256 `e2020b073c44f692685a24d6abc378817eb81ffaaf49fd0531ef8565f767f2f5`; proof SHA-256 `26e3fcc371f19e35c7d37500baf8e82c4386538dc6f47e66f4e0fefec50531e4`; proof retained | `BLOCKED-SIGSUM-TRUST-CHAIN`; archive not acquirable | Exact `sigsum-verify@v0.13.1` graph, verifier integrity/bootstrap, licenses, and compatibility of policy `sigsum-generic-2025-1` with the v1.3.2 proof |

Neither the age archive nor a verifier/module is part of an R3 request under this proposal. Backup and restore work remains possible only without claiming age-specific encryption evidence; encryption-specific controls remain `Unproved`.

### PostgreSQL OCI entry

Replace the mutable-tag acquisition language with:

| Field | Exact value |
|---|---|
| Product identity | Docker Official Image packaging for PostgreSQL 18.6, source commit `e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc`, directory `18/bookworm` |
| Retained multi-architecture index | 6,491 bytes; `sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af` |
| Retained target manifest | `linux/arm64/v8`; 3,454 bytes; `sha256:4d155aa3f2c2cc1838bb70e81396f76373ec7275ec9ce9cf32873cd677c9a992` |
| Acquisition identity | Platform-manifest digest only; the tag `18.6-bookworm` is evidence metadata and must not be requested |
| Authentication | Anonymous, pull-only, repository-scoped bearer token for `library/postgres`, held in memory only |
| Signature posture | Content-addressed integrity and Official Images provenance; no detached image signature established |
| Runtime authority | None: no image import, runtime initialization, container, volume, network, database, listener, or command |

The exact proposed R3-O1 content set is:

| Object | Bytes | SHA-256 digest |
|---|---:|---|
| Config | 10,055 | `b85269e8c6aa961524542eb4dcca44c4aa1deba2cf507e9e28d5ba8f971aeab9` |
| Layer 01 | 28,117,289 | `75782e20ea1f4a9d9259bc20a5ecbbea8d5943bf5370bf0f5727900728f1cc9a` |
| Layer 02 | 1,170 | `545481733576eae22997a02807d7947613125ef556fc5267d8b71b8633888312` |
| Layer 03 | 4,519,566 | `60ec89b686ebd79b724a8429c13f58185a441a1c483bf8819931d566db040829` |
| Layer 04 | 1,203,841 | `f54f79a42a2dfe06e33db86854c4f0484d3fd98636de77570703312d26f0df24` |
| Layer 05 | 8,066,459 | `63ba4d1b9b1aa469776fb0250fffeace022a871a88d423518cc33fa388ffc663` |
| Layer 06 | 1,108,983 | `22a8987b6f5cb2778463a82a1f33a53b667e76f57aed25ffcba1f70b16c9ab59` |
| Layer 07 | 116 | `7ef8a510d41418d6cf3f98cf24533b81adcba4bd5689ae1e60c89ad5c4336e3f` |
| Layer 08 | 3,140 | `7105667d1505a2ae58b986439108a7fd8a3a8cab26eb47f1009ae60c3986ff2e` |
| Layer 09 | 112,194,873 | `840f3b8b2441f35405e77774444fdc3233c4c83ea240af495f58ad95390c67be` |
| Layer 10 | 19,319 | `3d2cfabac35eb0d31771041e04952ee51afdfb69a6d41a2dbae864f63bd7a070` |
| Layer 11 | 128 | `ca026fbec3730f56a63cea66221e2aadbf90e89f796f967dee89cfddeaf09819` |
| Layer 12 | 6,107 | `db077a768c3b2e74f651728b16ce42dd1adba16a42ec7b3402c1209f8204cfef` |
| Layer 13 | 186 | `53367cc5fc824588caec6e186b0a5641c4c80e25a36002faed84d4eb6e9dfb2a` |

The expected total is exactly fourteen content objects and 155,251,232 bytes. Each object must be requested by digest and independently hashed before acceptance. The object count, individual sizes, digests, and total must reconcile before any offline inspection. No referrer, signature object, attestation, vulnerability database, helper image, alternate architecture, or base-image pull is authorized.

## Exact proposed allowlist changes

These are line-level changes to the acquisition allowlist in `docs/phase-3/DEPENDENCY-MANIFESTS.md`. They are not applied by this proposal.

### Add

| Host | Method and exact path boundary | Workstream | Stop behavior |
|---|---|---|---|
| `dl.google.com` | One `GET` for `/go/go1.27.1.darwin-arm64.tar.gz` | R3-G1 only | Stop on redirect, authentication, changed path, non-200 response, size disagreement, or hash mismatch |
| `production.cloudfront.docker.com` | `GET` only for registry-generated `/registry-v2/docker/registry/v2/blobs/sha256/<prefix>/<one-of-14-accepted-digests>/data`; ephemeral signed query accepted only from the immediately preceding registry 307 and never persisted | R3-O1 only | Stop on direct navigation, unlisted digest/path, redirect from CDN, credential request, or content mismatch |

### Remove

| Host | Reason |
|---|---|
| `production.cloudflare.docker.com` | Erroneous hostname: neither observed at Checkpoint A nor named by the accepted publisher evidence |

### Retain but narrow or disable

| Host | R2 state | Exact restriction |
|---|---|---|
| `go.dev` | Evidence only; disabled in R3-G1 | Do not request the redirecting archive route; use the exact accepted CDN URL directly |
| `proxy.golang.org` | Disabled in R3-G1; reserved for a separately approved metadata-only G2 pass | No `.zip`; exact `.info`/`.mod` paths only after a new approval |
| `sum.golang.org` | Disabled in R3-G1; reserved for separately approved G2/G3 evidence | Exact lookup/tile requests generated by the frozen graph only; no request before graph-stage approval |
| `pypi.org` | Disabled | Existing Python metadata is retained and no reacquisition is required |
| `files.pythonhosted.org` | Disabled | Existing three wheels are retained and verified; no reacquisition is required |
| `github.com` | Disabled for acquisition | Podman and age are blocked; R1 links remain documentation evidence only |
| `objects.githubusercontent.com` | Disabled | No accepted R3 object route uses it |
| `release-assets.githubusercontent.com` | Disabled | Podman and age artifact reacquisition is prohibited |
| `auth.docker.io` | R3-O1 only | One anonymous token request with `service=registry.docker.io` and `scope=repository:library/postgres:pull`; no refresh token, account, login, push, payment, or credential helper |
| `registry-1.docker.io` | R3-O1 only | `GET /v2/library/postgres/blobs/sha256:<one-of-14-accepted-digests>`; do not request a tag, index, alternate manifest, catalog, referrer, or upload endpoint |

Every unlisted host is denied. Wildcard subdomains, DNS aliases treated as equivalent, direct VCS fallback, mirrors, package managers, update services, telemetry, analytics, security-scanner feeds, and convenience download hosts are excluded.

R3-G1 and R3-O1 must use separate network windows and separate roots. Approval of one route does not activate hosts assigned to the other.

## Exact request and redirect expectations

### R3-G1 — Go archive only

| Sequence | Request | Expected result |
|---:|---|---|
| 1 | `GET https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz` | `200`; no redirect; archive bytes only |

No request to `go.dev`, module proxy, checksum database, Git, package manager, telemetry, or updater is allowed.

### R3-O1 — PostgreSQL content only

| Sequence | Request | Expected result |
|---:|---|---|
| 1 | `GET https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/postgres:pull` | `200`; anonymous pull token held only in process memory |
| 2–15 | `GET https://registry-1.docker.io/v2/library/postgres/blobs/sha256:<accepted-digest>` | `307` to the exact accepted CloudFront host/path or `200` content from the registry |
| 2a–15a | Follow an accepted `307` to `production.cloudfront.docker.com` | `200`; bytes must match the requested descriptor digest and size |

The retained index and platform manifest are inputs, not network targets. The mutable tag is never requested. A `401` may be used only to confirm the documented anonymous bearer challenge before the single token request; repeated auth negotiation, login, or wider scope is a stop. A `429` is a stop and does not authorize retry loops, credentials, payment, or a mirror.

## Cache and evidence paths

The accepted Checkpoint-A root `/tmp/mneme-phase3-checkpoint-a.H9KN5d` is read-only evidence for R2. It must not be renamed, supplemented, or reused as a download destination.

Each future R3 workstream must create a fresh owner-only root with `mktemp` and immediately record the expanded absolute path. The notation `<run-id>` below is a design placeholder only; no command may run until it has been replaced by the recorded path and validated. Each root has mode `0700`, is outside the repository, and contains a matching `MNEME_PHASE3_DISPOSABLE.json`.

### R3-G1 layout

```text
/tmp/mneme-phase3-r3-g1.<run-id>/
├── MNEME_PHASE3_DISPOSABLE.json
├── downloads/
│   └── go/
│       ├── go1.27.1.darwin-arm64.tar.gz.part
│       └── go1.27.1.darwin-arm64.tar.gz
└── evidence/
    ├── acquisition.jsonl
    ├── archive-inventory.json
    ├── checksums.sha256
    ├── environment.json
    ├── network.jsonl
    └── rollback.json
```

The `.part` path exists only during transfer. It is renamed only after byte-count and SHA-256 acceptance. There is no extraction, `GOROOT`, `GOPATH`, `GOBIN`, `GOCACHE`, `GOMODCACHE`, `GOENV`, module workspace, or installed binary in R3-G1.

### R3-O1 layout

```text
/tmp/mneme-phase3-r3-o1.<run-id>/
├── MNEME_PHASE3_DISPOSABLE.json
├── inputs/
│   └── oci/
│       ├── index.json
│       └── linux-arm64-v8-manifest.json
├── downloads/
│   └── oci/
│       └── blobs/
│           └── sha256/
│               ├── <14 accepted digest filenames>.part
│               └── <14 accepted digest filenames>
└── evidence/
    ├── acquisition.jsonl
    ├── blob-inventory.json
    ├── checksums.sha256
    ├── environment.json
    ├── network.jsonl
    ├── package-license-scan-plan.json
    └── rollback.json
```

The two `inputs` files are verified copies of the retained accepted metadata. No Docker configuration, credential file, image store, content store, runtime root, socket, volume, database directory, or decompressed layer is created. The anonymous token is never written to disk; signed query values and authorization headers are redacted before evidence is retained.

## Integrity and stop rules

For either route:

1. record clean repository status and the exact expanded disposable root before network access;
2. verify owner, mode, realpath, sentinel, non-symlink, and non-mount status;
3. enable only the one workstream's host/path set;
4. write only to the declared `.part` file;
5. record status, redirect host/path, filename, byte count, and sanitized headers;
6. close the transfer before hashing independently;
7. delete the `.part` file immediately on interruption, size mismatch, or hash mismatch;
8. reject an unknown host, path, method, component, redirect, authentication scope, account request, telemetry route, mutable identifier, or undeclared file;
9. disconnect the workstream network path after the exact object set completes or on the first stop;
10. present evidence before extraction, execution, decompression, package inventory, graph work, or another workstream.

TLS, response headers, and a registry token do not replace independent content hashing. A digest match does not establish a detached publisher signature where none exists.

## Rollback procedure

Rollback is per workstream and never targets the accepted Checkpoint-A root, repository, home directory, global cache, package installation, or unrelated process.

1. Stop the exact acquisition process and close its network path.
2. Confirm that no process has an executable, working directory, or open file beneath the recorded workstream root.
3. Reconcile every path against the root inventory; report any undeclared path and stop cleanup.
4. Delete any rejected or incomplete `.part` file by its recorded absolute path.
5. Retain accepted bytes only until their evidence package is reviewed. Retention does not make them executable or installable.
6. If removal is authorized, revalidate owner, mode, realpath, sentinel, non-symlink, non-mount, and exact inventory, then remove only the recorded workstream root.
7. Confirm the root is absent and that no process, listener, credential, token file, service, image store, database, module cache, or installed tool remains.
8. Record completion or the exact unresolved cleanup item; never broaden the target.

No global cache purge, package uninstall, `git clean`, Git reset, wildcard deletion, global process kill, container prune, image prune, or credential-helper cleanup is permitted.

## Specialist reviews

These R2 findings are part of the proposal; acceptance requires the named reviewer function to agree or record a disagreement.

| Review | R2 finding | Required condition before any R3 request |
|---|---|---|
| Maintenance / supply chain | Go and OCI identities are immutable and route-bounded; Podman and age remain correctly blocked | Preserve the accepted `U-R2-GO-01` treatment; verify the independently recorded Go response byte count and SHA-256, 14-object OCI reconciliation, and no signature overstatement |
| Security / privacy | Separate host windows, anonymous memory-only Docker token, redaction, no direct VCS/account fallback, and no runtime state minimize exposure | Confirm host/path enforcement can fail closed and that signed CDN queries and auth headers cannot enter durable logs |
| Licensing / cost | Go license is known; PostgreSQL and packaging licenses do not cover all layer contents; no account or paid route is allowed | Keep OCI license status Blocked until offline layer inventory; stop on rate-limit bypass, login, payment, or new terms |
| Quality / independent review | Counts reconcile to one Go artifact and fourteen OCI objects; the Go graph has a visible 14-module envelope | Independently compare every digest/size/path with accepted Checkpoint-A and R1 records; treat any fifteenth module or blob as a stop |
| Orchestrator / governance | R2 changes documentation only and retains one-stage-at-a-time authority | Do not infer R3, R4, Checkpoint B, prototype, or stack-selection authority from R2 acceptance |

Preservation/corpus review is not triggered because R2 writes no source-like path and handles no fixture or correspondence. It becomes mandatory if a later route could affect preservation or backup semantics. Product/UX and research/AI remain informed observers; R2 contains no product behavior or AI route.

## Uncertainty, gap, disagreement, and rejection records

| ID | Type | Record | Effect |
|---|---|---|---|
| `U-R2-GO-01` | Accepted uncertainty | Publisher evidence records the Go archive as 65 MB but not an accepted exact byte count | Accepted at Gate R2-A; a future R3-G1 must treat the independently recorded response byte count and SHA-256 as authoritative |
| `G-R2-GO-01` | Gap | No verified Go toolchain or authoritative graph exists | Module metadata expansion, ZIP acquisition, build, and verification remain blocked |
| `G-R2-AGE-01` | Gap | Sigsum verifier graph/bootstrap and v1.3.2 policy compatibility are absent | age remains blocked and is excluded from R3 |
| `G-R2-OCI-01` | Gap | Debian package, notice, license, and SBOM inputs are unavailable until blobs are inspected offline | OCI license/composition evidence remains Blocked after acquisition until separate offline review |
| `D-R2-01` | Disagreement placeholder | No disagreement is currently recorded | Any reviewer disagreement remains open in this table; it is not resolved by majority vote |
| `R-R2-PODMAN-01` | Rejection | Do not renew the Podman v6.1.2 package route | Invalid package signature, privileged/destructive effects, and incomplete rollback |
| `R-R2-AGE-01` | Rejection | Do not reacquire age or bootstrap an undeclared verifier | Would bypass graph-before-payload and verifier trust-chain review |
| `R-R2-OCI-TAG-01` | Rejection | Do not request `postgres:18.6-bookworm` by tag | The accepted immutable index/platform identities already exist; tag acquisition is mutable and unnecessary |
| `R-R2-COMBINED-01` | Rejection | Do not run Go and OCI acquisition in one window | Separate evidence stops and route-specific host boundaries are required |

Missing evidence is not scored as low risk and does not become accepted through R2 wording.

## Approval gate

Review of this proposal must make two decisions separately:

### Gate R2-A — Governance acceptance

The user may accept, reject, or request revisions to:

1. the exact proposed dependency-manifest replacements;
2. the addition of `dl.google.com` and `production.cloudfront.docker.com` under the stated path restrictions;
3. removal of `production.cloudflare.docker.com`;
4. disabled/narrowed status of all other acquisition hosts;
5. the Podman deferment and age blocker;
6. the fourteen-module metadata envelope and no-module-payload rule;
7. the fourteen-object PostgreSQL scope and no-tag rule;
8. cache, redaction, stop, retention, and rollback controls; and
9. uncertainty `U-R2-GO-01`.

Acceptance of R2-A would authorize marking and committing this documentation proposal only if the user says so. It would not apply the proposed edits to the accepted dependency manifest or allowlist and would not authorize a network request.

### Gate R2-B — Separate R3 workstream authorization

After R2-A is accepted, a new explicit instruction must name exactly one next workstream:

- **R3-G1:** one Go archive request, hash/archive evidence, then stop; or
- **R3-O1:** one anonymous PostgreSQL content set of fourteen exact blobs, then stop.

The recommended first workstream is R3-G1 because it is one artifact, requires no credential or redirect, and is the prerequisite for later graph closure. This recommendation is sequencing only; it is not stack selection.

Gate R2-A accepted `U-R2-GO-01`; that acceptance does not activate R3. No general phrase such as “continue” or acceptance of this R2 document activates R3.

## Explicit non-authorization

This proposal does not authorize:

- applying the dependency-manifest or allowlist changes described above;
- contacting `dl.google.com`, `production.cloudfront.docker.com`, or any other host;
- acquiring or retrying Go, any Go module, Podman, age, Sigsum, OCI content, or any other artifact;
- extracting, installing, importing, executing, compiling, building, testing, or starting anything;
- creating a fixture, credential, key, service, listener, container, runtime machine, image store, database, prototype, SBOM, or generated artifact;
- creating the future graph workspace or cache roots described above;
- beginning R3, R4, Checkpoint B, stack selection, or a stack-selection ADR;
- committing this R2 proposal or pushing any commit.

## Review request

Review is requested on the complete R2 manifest/allowlist proposal and the two-part approval gate. Until Gate R2-A and then one Gate R2-B workstream are explicitly approved, the accepted Checkpoint-A state remains unchanged and no network acquisition resumes.
