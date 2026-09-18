# R3-G2 Go Module-Graph Closure Authorization Request

**Status:** Accepted
**Review date:** 2026-09-18
**Request date:** 2026-09-18
**Workstream result:** Incomplete
**Result review date:** 2026-09-18
**Current authority:** Closed. The accepted request was executed only through the bounded literal metadata acquisition, then stopped because checksum-database signature and Merkle-proof verification was not proved. No retry, remediation route, graph work, or later-stage authority remains active.

The accepted evidence is recorded in [the R3-G2 evidence summary](r3-g2/README.md) and [stop record](r3-g2/STOP-RECORD.md). The authorization remains accepted as the governing boundary; `Incomplete` is the outcome of the workstream, not a withdrawal of that authorization.

## Decision requested

Authorize a separately bounded R3-G2 workstream to:

1. copy the accepted Go archive from the owner-only R3-G1 root into a new disposable R3-G2 root and reverify it;
2. extract that verified toolchain only inside the new root;
3. execute only the exact Go metadata commands named here;
4. request only exact `.info` and `.mod` metadata for the fourteen accepted module/version pairs;
5. authenticate module metadata through the Go checksum database without requesting module ZIP/source payloads;
6. calculate and independently reconcile the minimal-version-selected module graph;
7. disconnect the network path, repeat the graph commands offline, and stop for evidence review.

Approval would not authorize a module `.zip`, source checkout, package import, candidate code, compile, link, build, test, installation, service, or product runtime.

## Governing inputs and limits

This request is governed by:

- the accepted [R2 Revised Acquisition Manifest Proposal](R2-REVISED-ACQUISITION-MANIFEST-PROPOSAL.md);
- the accepted [R3-G1 authorization](R3-G1-GO-ARCHIVE-AUTHORIZATION-REQUEST.md); and
- the accepted [R3-G1 evidence summary](r3-g1/README.md).

R3-G1 established only verified archive bytes. It did not authorize extraction or execution. R3-G2 would be the first authority to extract and run that exact Go toolchain, and only for module-metadata graph closure.

Podman and age remain blocked. PostgreSQL and R3-O1 remain outside scope. Checkpoint A and Gate 2 remain open. No stack has been selected.

## Accepted toolchain input

| Field | Required value |
|---|---|
| Source path | `/tmp/mneme-phase3-r3-g1.UQ7udQ/downloads/go/go1.27.1.darwin-arm64.tar.gz` |
| Source owner/mode | UID 501; mode `0600` |
| Bytes | 68,100,347 |
| SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Static inventory | 17,353 members; all under `go/`; accepted R3-G1 safety findings |
| Expected executed identity | `go version go1.27.1 darwin/arm64` |

R3-G2 must not modify the R3-G1 root. It copies the archive to the new root, verifies byte count and SHA-256 before extraction, compares extraction paths to the accepted member inventory, and refuses to execute `go` if any identity, path, type, owner, mode, size, or extraction-boundary check fails.

No request to `dl.google.com` or another toolchain source is permitted.

## Initial graph envelope

The initial envelope is exactly fourteen module/version pairs:

| ID | Module | Version | Initial classification |
|---:|---|---:|---|
| 1 | `github.com/jackc/pgx/v5` | v5.11.0 | Direct graph root |
| 2 | `github.com/jackc/pgpassfile` | v1.0.0 | Published pgx dependency |
| 3 | `github.com/jackc/pgservicefile` | v0.0.0-20240606120523-5a60cdf6a761 | Published pgx dependency |
| 4 | `github.com/jackc/puddle/v2` | v2.2.2 | Published pgx dependency |
| 5 | `golang.org/x/sync` | v0.17.0 | Published pgx dependency |
| 6 | `golang.org/x/text` | v0.29.0 | Published pgx dependency |
| 7 | `github.com/stretchr/testify` | v1.11.1 | Metadata candidate; role unresolved |
| 8 | `github.com/davecgh/go-spew` | v1.1.1 | Metadata candidate; role unresolved |
| 9 | `github.com/kr/pretty` | v0.3.0 | Metadata candidate; role unresolved |
| 10 | `github.com/pmezard/go-difflib` | v1.0.0 | Metadata candidate; role unresolved |
| 11 | `gopkg.in/check.v1` | v1.0.0-20201130134442-10cb98267c6c | Metadata candidate; role unresolved |
| 12 | `gopkg.in/yaml.v3` | v3.0.1 | Metadata candidate; role unresolved |
| 13 | `golang.org/x/tools` | v0.36.0 | Metadata candidate; role unresolved |
| 14 | `golang.org/x/mod` | v0.27.0 | Metadata candidate; role unresolved |

R3-G2 may determine MVS selection, graph edges, and which parent module file introduces each member. Without candidate source or package imports, it cannot prove that a module is linked into a future runtime artifact. Package-level runtime/build/test classification remains `Unresolved` unless it follows strictly from the metadata graph; no source payload may be acquired to resolve it.

Discovery of any fifteenth module or any different selected version stops R3-G2 before its metadata is requested.

## Exact proxy metadata paths

If approved, `proxy.golang.org` may receive `GET` requests only for the following exact path pairs. No query string is permitted.

| Module/version | Exact allowed paths |
|---|---|
| `github.com/jackc/pgx/v5@v5.11.0` | `/github.com/jackc/pgx/v5/@v/v5.11.0.info`; `/github.com/jackc/pgx/v5/@v/v5.11.0.mod` |
| `github.com/jackc/pgpassfile@v1.0.0` | `/github.com/jackc/pgpassfile/@v/v1.0.0.info`; `/github.com/jackc/pgpassfile/@v/v1.0.0.mod` |
| `github.com/jackc/pgservicefile@v0.0.0-20240606120523-5a60cdf6a761` | `/github.com/jackc/pgservicefile/@v/v0.0.0-20240606120523-5a60cdf6a761.info`; `/github.com/jackc/pgservicefile/@v/v0.0.0-20240606120523-5a60cdf6a761.mod` |
| `github.com/jackc/puddle/v2@v2.2.2` | `/github.com/jackc/puddle/v2/@v/v2.2.2.info`; `/github.com/jackc/puddle/v2/@v/v2.2.2.mod` |
| `golang.org/x/sync@v0.17.0` | `/golang.org/x/sync/@v/v0.17.0.info`; `/golang.org/x/sync/@v/v0.17.0.mod` |
| `golang.org/x/text@v0.29.0` | `/golang.org/x/text/@v/v0.29.0.info`; `/golang.org/x/text/@v/v0.29.0.mod` |
| `github.com/stretchr/testify@v1.11.1` | `/github.com/stretchr/testify/@v/v1.11.1.info`; `/github.com/stretchr/testify/@v/v1.11.1.mod` |
| `github.com/davecgh/go-spew@v1.1.1` | `/github.com/davecgh/go-spew/@v/v1.1.1.info`; `/github.com/davecgh/go-spew/@v/v1.1.1.mod` |
| `github.com/kr/pretty@v0.3.0` | `/github.com/kr/pretty/@v/v0.3.0.info`; `/github.com/kr/pretty/@v/v0.3.0.mod` |
| `github.com/pmezard/go-difflib@v1.0.0` | `/github.com/pmezard/go-difflib/@v/v1.0.0.info`; `/github.com/pmezard/go-difflib/@v/v1.0.0.mod` |
| `gopkg.in/check.v1@v1.0.0-20201130134442-10cb98267c6c` | `/gopkg.in/check.v1/@v/v1.0.0-20201130134442-10cb98267c6c.info`; `/gopkg.in/check.v1/@v/v1.0.0-20201130134442-10cb98267c6c.mod` |
| `gopkg.in/yaml.v3@v3.0.1` | `/gopkg.in/yaml.v3/@v/v3.0.1.info`; `/gopkg.in/yaml.v3/@v/v3.0.1.mod` |
| `golang.org/x/tools@v0.36.0` | `/golang.org/x/tools/@v/v0.36.0.info`; `/golang.org/x/tools/@v/v0.36.0.mod` |
| `golang.org/x/mod@v0.27.0` | `/golang.org/x/mod/@v/v0.27.0.info`; `/golang.org/x/mod/@v/v0.27.0.mod` |

The maximum proxy object set is twenty-eight: fourteen `.info` and fourteen `.mod` objects. Repeated requests are recorded and stop the workstream; they do not authorize retries.

The following proxy paths are expressly denied:

- every `.zip` and `.ziphash` path;
- every `/@v/list`, `@latest`, version query, retraction query outside the accepted `.mod` files, or alternate version;
- every module outside the fourteen-row table;
- every direct source, Git, VCS, mirror, vanity-import, or package-manager route; and
- every upload, mutation, authentication, account, telemetry, or analytics path.

## Exact checksum-database paths

`sum.golang.org` may receive `GET` requests only for these fourteen exact lookup paths:

| Module/version | Exact lookup path |
|---|---|
| `github.com/jackc/pgx/v5@v5.11.0` | `/lookup/github.com/jackc/pgx/v5@v5.11.0` |
| `github.com/jackc/pgpassfile@v1.0.0` | `/lookup/github.com/jackc/pgpassfile@v1.0.0` |
| `github.com/jackc/pgservicefile@v0.0.0-20240606120523-5a60cdf6a761` | `/lookup/github.com/jackc/pgservicefile@v0.0.0-20240606120523-5a60cdf6a761` |
| `github.com/jackc/puddle/v2@v2.2.2` | `/lookup/github.com/jackc/puddle/v2@v2.2.2` |
| `golang.org/x/sync@v0.17.0` | `/lookup/golang.org/x/sync@v0.17.0` |
| `golang.org/x/text@v0.29.0` | `/lookup/golang.org/x/text@v0.29.0` |
| `github.com/stretchr/testify@v1.11.1` | `/lookup/github.com/stretchr/testify@v1.11.1` |
| `github.com/davecgh/go-spew@v1.1.1` | `/lookup/github.com/davecgh/go-spew@v1.1.1` |
| `github.com/kr/pretty@v0.3.0` | `/lookup/github.com/kr/pretty@v0.3.0` |
| `github.com/pmezard/go-difflib@v1.0.0` | `/lookup/github.com/pmezard/go-difflib@v1.0.0` |
| `gopkg.in/check.v1@v1.0.0-20201130134442-10cb98267c6c` | `/lookup/gopkg.in/check.v1@v1.0.0-20201130134442-10cb98267c6c` |
| `gopkg.in/yaml.v3@v3.0.1` | `/lookup/gopkg.in/yaml.v3@v3.0.1` |
| `golang.org/x/tools@v0.36.0` | `/lookup/golang.org/x/tools@v0.36.0` |
| `golang.org/x/mod@v0.27.0` | `/lookup/golang.org/x/mod@v0.27.0` |

Checksum authentication may also require tile GETs. Because exact tile coordinates are derived from signed lookup records and the client's trusted checkpoint, they cannot be truthfully predeclared as literal paths. The only permitted derived path forms are:

- `/tile/8/<level>/<tile-number>`; and
- `/tile/8/<level>/<tile-number>.p/<partial-width>`.

Every tile path must be emitted by the Go 1.27.1 checksum client as necessary to authenticate one of the fourteen allowed lookups, recorded in a pending-request ledger before transfer, requested once, and tied in evidence to the lookup that required it. At most 128 distinct tile GETs are permitted. A tile outside these forms, a 129th tile, `/latest`, a direct record-number lookup, a redirect, a repeated request, or any other checksum path stops R3-G2.

The checksum database's built-in trusted key and every signed tree head/proof result must be recorded. `GONOSUMDB` exceptions are forbidden; a sumdb verification failure cannot be bypassed with `GOSUMDB=off` during the networked pass.

## Exact host and request boundary

| Host | Permitted traffic | Maximum known object requests |
|---|---|---:|
| `proxy.golang.org` | The twenty-eight literal `.info`/`.mod` paths above, `GET` only, no query, redirect, or retry | 28 |
| `sum.golang.org` | Fourteen literal lookup paths plus at most 128 lookup-derived tile paths, `GET` only, no query, redirect, or retry | 142 |

No other application host is active. In particular, R3-G2 excludes `dl.google.com`, `go.dev`, GitHub, direct Git/VCS hosts, vanity import hosts, mirrors, package managers, PostgreSQL/Docker hosts, telemetry, updates, accounts, and cloud services.

DNS and TLS needed for the two exact hosts do not authorize an application request to another hostname. Any redirect is a stop and is not followed. Authentication, cookies, client certificates, netrc, credential helpers, proxies, retries, range/resume, alternate services, and fallbacks must be disabled.

## Disposable root and workspace

R3-G2 would use a new owner-only root created with `mktemp` as `/tmp/mneme-phase3-r3-g2.XXXXXX`. `<run-id>` below is explanatory notation only and must be replaced by the validated expanded path before any command runs.

```text
/tmp/mneme-phase3-r3-g2.<run-id>/
├── MNEME_PHASE3_DISPOSABLE.json
├── inputs/
│   └── go1.27.1.darwin-arm64.tar.gz
├── toolchain/
│   └── go/
├── workspace/
│   ├── go.mod
│   └── go.sum
├── state/
│   ├── gopath/
│   ├── gomodcache/
│   │   └── cache/
│   │       └── download/
│   │           └── sumdb/
│   │               └── sum.golang.org/
│   ├── go-build-cache/
│   └── go-tmp/
└── evidence/
    ├── acquisition.jsonl
    ├── command-transcript.jsonl
    ├── environment.json
    ├── extraction-inventory.tsv
    ├── graph-edges.txt
    ├── graph-modules.jsonl
    ├── metadata-inventory.tsv
    ├── network.jsonl
    ├── request-ledger.tsv
    ├── rollback.json
    ├── stop-register.md
    └── workspace-checksums.sha256
```

All directories are mode `0700`; files containing evidence or metadata are mode `0600`. The R3-G1 root is read-only input and is never used as an extraction, workspace, cache, or output path.

The workspace `go.mod` is exactly:

```text
module example.invalid/mneme-phase3-graph

go 1.27.1

require github.com/jackc/pgx/v5 v5.11.0
```

There is no `.go` file, package, fixture, source record, candidate code, test, vendor directory, or work file. `go.sum` may be created only as metadata evidence for authenticated `.mod` records; it is not a build lock and must be labeled accordingly.

## Process environment

Every Go command must use the extracted absolute binary path and an environment that confines all Go state to the disposable root:

| Variable | Required value or rule |
|---|---|
| `GOROOT` | `<root>/toolchain/go` |
| `GOPATH` | `<root>/state/gopath` |
| `GOMODCACHE` | `<root>/state/gomodcache` |
| `GOCACHE` | `<root>/state/go-build-cache` |
| `GOTMPDIR` | `<root>/state/go-tmp` |
| `GOENV` | `off`; no persistent Go environment file |
| `GOTOOLCHAIN` | `local`; no toolchain auto-download |
| `GOWORK` | `off` |
| `GOPROXY` | `https://proxy.golang.org`; no comma/pipe fallback and no `direct` |
| `GOSUMDB` | `sum.golang.org`; no bypass during authenticated metadata acquisition |
| `GOPRIVATE` | Empty |
| `GONOPROXY` | `none` |
| `GONOSUMDB` | Empty |
| `GOVCS` | `*:off` |
| `GOAUTH` | `off`; if unsupported, stop rather than fall back to netrc or credentials |
| `CGO_ENABLED` | `0` |

No shell profile, system path, user Go configuration, global cache, keychain, netrc, Git configuration, credential helper, or package-manager state may be read or changed for routing. The process environment must be recorded with secret values excluded.

## Exact command boundary

If approved, only these Go command forms may execute, in this order:

1. `<root>/toolchain/go/bin/go version`;
2. `<root>/toolchain/go/bin/go env -json` for the variables listed above plus `GOOS`, `GOARCH`, and `GOVERSION`;
3. from `<root>/workspace`, a networked metadata-only `go list -mod=mod -m -json all` under the exact host/path guard;
4. from the same workspace, `go mod graph` only if step 3 completed without an envelope expansion or payload request;
5. close the network path;
6. rerun `go list -mod=readonly -m -json all` with `GOPROXY=off`, the same checksum policy, and external network denied;
7. rerun `go mod graph` with `GOPROXY=off` and external network denied; and
8. stop for evidence review.

No `go install`, `go get`, `go mod download`, `go mod tidy`, `go mod vendor`, `go generate`, `go run`, `go test`, `go build`, `go tool`, package listing, package import, compiler, linker, vet, formatter, workspace command, or source-control command is permitted.

If any allowed command attempts a `.zip`, source, alternate toolchain, VCS, credential, or out-of-envelope request, the network guard rejects it and the workstream stops. The command is not retried with different flags.

## Integrity and graph checks

R3-G2 must:

1. reverify the copied toolchain archive's 68,100,347-byte count and accepted SHA-256;
2. extract only after sentinel/root/path checks and reconcile all 17,353 archive members without writing outside `<root>/toolchain`;
3. require the exact `go version go1.27.1 darwin/arm64` identity before any network activation;
4. record SHA-256 and byte count for every `.info`, `.mod`, lookup, and tile object;
5. require Go's checksum client to authenticate every selected module's `/go.mod` hash without an exception;
6. retain and hash the exact generated metadata-only `go.sum`;
7. reconcile the selected module list to no more than the fourteen-row envelope and exact accepted versions;
8. record every graph edge and the parent metadata file that introduced it;
9. confirm no `.zip`, `.ziphash`, module source directory, VCS checkout, package, binary, object, or build artifact exists;
10. close the network path and reproduce identical module-list and graph-edge outputs offline; and
11. reconcile every created path against the disposable-root inventory.

An authenticated metadata graph does not establish module source integrity because source ZIPs are expressly absent. It establishes selected versions and authenticated `go.mod` metadata only. Any later ZIP acquisition requires a separate G3 graph-approval record and user authorization.

## Stop conditions

R3-G2 stops immediately on:

- toolchain archive, extraction inventory, or executed identity mismatch;
- write outside the disposable root or read/use of a user/system Go environment or credential source;
- any host, method, path, query, module, version, redirect, retry, range/resume, authentication, proxy, mirror, or fallback outside this request;
- any `.zip`, `.ziphash`, source extraction, Git/VCS checkout, package-manager request, or package source directory;
- discovery of a fifteenth module or a different selected version;
- sumdb signature, tree, proof, lookup, tile, or `/go.mod` hash failure;
- a tile path not derived from an allowed lookup, a repeated tile, or the 129th distinct tile;
- mutation of the single-requirement graph-root `go.mod` other than metadata-only `go.sum` creation;
- compile, link, build, test, generator, formatter, vet, package import/listing, service, listener, or candidate action;
- disagreement between online and offline graph outputs;
- undeclared file, cache, process, socket, listener, credential, or environment change;
- inability to disable the network path or reconcile the exact root; or
- repository change other than a later separately reviewed normalized documentation package.

A stop preserves bounded evidence, closes the network path, makes no retry or substitution, and returns for user review.

## Required evidence package

The R3-G2 review package must include:

1. preflight Git status, commit, root realpath/owner/mode/sentinel checks, and absence of prior matching state;
2. source and copied archive byte counts and SHA-256 values;
3. complete extraction inventory and proof that every path remained under `<root>/toolchain`;
4. exact toolchain version and confined Go environment;
5. exact workspace bytes and hashes before and after graph work;
6. complete request ledger with host, method, literal/derived path, parent lookup where applicable, status, redirects, retries, bytes, SHA-256, and sanitized headers;
7. all checksum lookup records, signed tree heads, tile paths/hashes, trusted key identity, and verification outcomes;
8. metadata inventory for every `.info` and `.mod` object;
9. selected module list, versions, selection reasons, parent module, graph edges, and unresolved classifications;
10. explicit record of any discovered fifteenth module without requesting it;
11. exact `go.sum` with a statement that it covers metadata only and is not a build lock;
12. negative inventory proving zero ZIPs, source trees, VCS checkouts, package artifacts, binaries, builds, and tests;
13. byte-identical or hash-identical online/offline module-list and graph outputs;
14. network closure, process/open-file/listener checks, and complete cache/path inventory;
15. stop/anomaly/disagreement register, including explicit zero findings where applicable;
16. rollback/retention status; and
17. confirmation that no account, real data, fixture, service, PostgreSQL, Podman, age, R3-O1, Checkpoint B, or stack-selection action occurred.

Raw module metadata, checksum records, extracted toolchain, workspace, caches, and command/network logs remain outside Git. Only a separately reviewed normalized documentation summary may later be proposed for the repository.

## Rollback and retention

The R3-G1 root and verified archive remain untouched. R3-G2 cleanup acts only on the exact new sentinel-bearing root.

On interruption or rejection:

1. stop only the recorded Go/acquisition process after verifying its executable and working directory are under the R3-G2 root;
2. close the R3-G2 network path;
3. mark all partial/unverified metadata and generated graph outputs untrusted;
4. preserve only bounded sanitized evidence needed for review;
5. inventory every remaining path; and
6. do not retry, broaden scope, or remove the root until user review.

After a successful graph result, retain the complete R3-G2 root for review. Any later removal requires exact realpath, owner, mode, sentinel, non-symlink, non-mount, process/open-file, and inventory checks before removing only that root.

No global Go-cache purge, package uninstall, broad recursive deletion, wildcard target, Git cleanup/reset, or unrelated process termination is permitted.

## Specialist authorization checks

| Review function | Required finding before authorization |
|---|---|
| Maintenance / supply chain | Exact toolchain input, fourteen-module envelope, twenty-eight proxy paths, fourteen lookup paths, derived-tile rule, and no-payload boundary are coherent |
| Security / privacy | Two hosts only; no redirects/retries/auth/VCS; all state confined; no user credentials/config; network closure and raw-log redaction are enforceable |
| Licensing / cost | Metadata-only work adds no distribution action or paid/account route; license completeness remains provisional without source payloads |
| Quality / independent review | Request ledger, checksums, selected versions, graph edges, no-ZIP inventory, and online/offline equivalence are independently reproducible |
| Orchestrator / governance | Approval is R3-G2 only and stops before module payloads, G3 approval, R3-O1, R4, Checkpoint B, prototypes, or stack selection |

Any disagreement remains explicit and blocks authorization until resolved.

## Explicit uncertainties

| ID | Accepted fact requiring review | Proposed control |
|---|---|---|
| `U-R3-G2-01` | Checksum-database tile coordinates cannot be known before authenticated lookup records expose the required tree positions | Permit only the two exact tile path forms, require a signed-lookup derivation and pending-request ledger entry before each GET, cap the run at 128 distinct tiles, and stop on every other path |
| `U-R3-G2-02` | The fourteen modules are an initial envelope from accepted publisher metadata, not yet an authoritative MVS result | Block the first request for any fifteenth module or different version and return the discovered edge for review |
| `U-R3-G2-03` | A metadata graph cannot establish which modules will be linked into candidate code that does not yet exist | Keep package-level runtime/build/test classification `Unresolved`; do not acquire source to answer it |

Approval must accept these uncertainties as bounded graph-closure conditions or request a revision. They may not be silently converted into broader host, path, payload, or inference authority.

## Explicit non-authorization

This proposed request does not currently authorize anything beyond review. Even if later accepted, R3-G2 would not authorize:

- a module `.zip`, `.ziphash`, source tree, Git/VCS checkout, package import, or package-level inspection;
- any module or version outside the fourteen-row envelope;
- toolchain download, system/user installation, PATH/profile change, or global Go cache;
- candidate code, fixture, parser, service, listener, database, container, credential, key, SBOM, prototype, build, test, benchmark, or product-generated artifact;
- Podman, age, Sigsum, PostgreSQL/OCI, R3-O1, R4, Checkpoint B, production work, real data, cloud AI, or account access;
- treating metadata graph closure as source-payload integrity, offline build completeness, stack selection, or a passed Gate 2;
- committing raw evidence or pushing.

## Required explicit authorization

R3-G2 may begin only after the user gives an instruction substantively equivalent to:

> I authorize R3-G2 only under `R3-G2-GO-MODULE-GRAPH-CLOSURE-AUTHORIZATION-REQUEST.md`: copy and reverify the accepted Go archive into a fresh disposable root; extract and execute only the named Go metadata commands; contact only `proxy.golang.org` and `sum.golang.org` for the exact approved `.info`, `.mod`, lookup, and derived tile paths; acquire no ZIP or source payload; stop on any new module/version or route deviation; disconnect, reproduce the graph offline, and return with the complete evidence package. No later stage is authorized.

Acceptance of R3-G1, acceptance of this proposal as documentation, or a general instruction to continue is not R3-G2 authorization.

## Review request

Review is requested on the fourteen-module envelope, literal proxy/lookup paths, bounded derived-tile rule, first toolchain-execution boundary, disposable workspace, command list, integrity model, stop conditions, evidence package, and rollback. Until approval is explicit, the Go archive remains unextracted and unexecuted, no module request or graph command occurs, and both proposed hosts remain inactive.
