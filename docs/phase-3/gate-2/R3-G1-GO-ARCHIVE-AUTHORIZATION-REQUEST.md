# R3-G1 Go Archive Acquisition Authorization Request

**Status:** Accepted
**Review date:** 2026-09-18
**Request date:** 2026-09-18
**Current authority:** R3-G1 only under this accepted request. Host/path permission is temporary and limited to the one authorized archive GET.

## Decision requested

Authorize one bounded R3-G1 acquisition workstream for the exact Go 1.27.1 macOS arm64 archive. The workstream would make one direct HTTPS archive request, independently record the received byte count and SHA-256, perform non-executing archive-structure inspection, disconnect its network path, and stop for evidence review.

Approval would not authorize installation, extraction, execution, module access, graph calculation, compilation, tests, or any other R3 workstream.

## Governing decisions

This request is governed by the accepted [R2 Revised Acquisition Manifest Proposal](R2-REVISED-ACQUISITION-MANIFEST-PROPOSAL.md) and preserves these decisions:

- `U-R2-GO-01` is accepted. The publisher's rounded 65 MB description is informational only.
- The authoritative transfer evidence is the independently recorded response byte count and SHA-256.
- Podman remains blocked and deferred.
- age remains blocked.
- all Go module payloads remain blocked pending a later metadata-graph and graph-approval stage;
- PostgreSQL remains outside R3-G1 and limited to its separately proposed fourteen-object digest set;
- no accepted project manifest or persistent allowlist is edited by R3-G1; and
- no stack has been selected.

Checkpoint A remains incomplete and Gate 2 remains not passed regardless of the R3-G1 outcome.

## Exact acquisition object

| Field | Authorized value if approved |
|---|---|
| Product | Go toolchain |
| Version | 1.27.1 |
| Platform | macOS arm64 |
| Filename | `go1.27.1.darwin-arm64.tar.gz` |
| Exact URL | `https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz` |
| Method | One `GET` |
| Query | None |
| Expected response | `200`; no redirect |
| Expected byte count | Not predeclared under accepted `U-R2-GO-01`; record actual completed response count independently |
| Required SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Signature posture | No detached signature advertised in the accepted evidence; do not overstate hash verification as signature verification |
| License | BSD-style Go license, already recorded in R1/R2 evidence |

No metadata request, `HEAD`, range request, retry, mirror request, version fallback, package-manager request, or alternate archive is authorized.

## Temporary host/path activation

If and only if this request is explicitly approved, the R3-G1 acquisition guard may activate exactly:

| Host | Method | Path | Window |
|---|---|---|---|
| `dl.google.com` | `GET` | `/go/go1.27.1.darwin-arm64.tar.gz` | One R3-G1 request only |

The request must disable automatic redirects. DNS resolution and TLS connection needed for this exact host are incidental to the one request; they do not authorize another application host or path.

The following remain inactive:

- `go.dev`;
- `proxy.golang.org`;
- `sum.golang.org`;
- direct Git or VCS hosts;
- package managers and mirrors;
- PostgreSQL/Docker registry and CDN hosts;
- GitHub and release-asset hosts;
- update, telemetry, analytics, account, login, support, or AI services; and
- every unlisted host.

A redirect, DNS/CNAME observation does not add a host to the application allowlist. Any HTTP redirect or request for authentication stops R3-G1 without following or retrying it.

## Preflight conditions

Before network activation, the operator must:

1. record a clean Git status and the current commit identity;
2. confirm no prior R3-G1 root or transfer process is active;
3. create one fresh owner-only temporary root with `mktemp` using `/tmp/mneme-phase3-r3-g1.XXXXXX`;
4. record the expanded absolute root and validate mode `0700`, owner, realpath, non-symlink, and non-mount status;
5. create and verify a matching `MNEME_PHASE3_DISPOSABLE.json` sentinel;
6. record the exact one-host, one-method, one-path network rule;
7. verify that automatic redirects, retries, cookies, credential helpers, proxy fallbacks, netrc use, client-certificate lookup, telemetry, and update checks are disabled;
8. confirm adequate free space without modifying a global cache or installation path; and
9. stop if any prerequisite differs from this request.

Preflight creates only the approved disposable acquisition root, sentinel, empty declared directories, and acquisition evidence records. It creates no product or experiment fixture, credential, key, tool installation, module workspace, service, listener, prototype, build, test, or repository file.

## Exact future cache layout

The expanded root is recorded before any write. `<run-id>` below is explanatory notation and must never be passed unresolved to a command.

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

The `.part` path is the only transfer destination. The final archive path may be created by an atomic same-directory rename only after the completed response count and SHA-256 pass. No path under `/usr/local`, `/opt`, a home-directory toolchain location, the repository, the accepted Checkpoint-A cache, or a global Go cache is in scope.

## Authorized sequence if approved

1. Complete and record the preflight checks.
2. Activate only the temporary `dl.google.com` host/path rule.
3. Issue the single direct `GET` with redirects and retries disabled.
4. Stream the response only to the declared `.part` file while independently counting received body bytes.
5. Record the final status, sanitized response headers, independently counted body bytes, and `Content-Length` when present.
6. Close the HTTP client and disable the R3-G1 network path before parsing or hashing the file.
7. Require status `200`. If `Content-Length` is present, require it to equal the independently counted body bytes. Absence of `Content-Length` is recorded and does not replace the independent count.
8. Compute SHA-256 independently and require the exact accepted digest.
9. Perform static archive inspection without extraction or executable invocation. Record member count, paths, types, link targets, declared sizes, ownership/mode metadata, and total expanded-size estimate.
10. Reject absolute paths, traversal, escaping links, device nodes, FIFOs, malformed headers, duplicate-path ambiguity, or unreasonable expansion.
11. Rename the `.part` file to the final cache filename only after steps 7–10 pass.
12. Reconcile the cache to one archive plus the declared evidence files.
13. Present the complete R3-G1 evidence for review and stop.

No second request is permitted even after a transient failure. A failed or interrupted request ends the workstream and requires a new user decision.

## Stop conditions

R3-G1 stops immediately on:

- any URL, host, method, path, query, filename, version, or platform difference;
- any redirect or automatic retry attempt;
- authentication, account, payment, cookie, client certificate, credential-helper, or interactive prompt;
- non-`200` response;
- response framing error, truncation, unexpected extra response, or byte-count disagreement;
- SHA-256 mismatch;
- archive path/type/link/size hazard;
- undeclared file, process, socket, listener, cache, environment change, or installer behavior;
- telemetry, update, proxy fallback, mirror, or external lookup;
- request to `go.dev`, a Go module service, Git/VCS, or any PostgreSQL/OCI host;
- repository change other than the later normalized documentation evidence explicitly reviewed by the user; or
- inability to close the network path and reconcile the exact root.

A stop cannot be bypassed by accepting the publisher's rounded size, retrying, changing tools, adding a host, choosing another version, using a package manager, or weakening integrity checks.

## Evidence required at the stop

The review package must state:

1. expanded temporary root, owner, mode, sentinel identity, and timestamps;
2. current commit and clean preflight status;
3. exact requested URL, method, request count, result, and absence of redirects/retries;
4. sanitized connection and response metadata with secrets, cookies, and ephemeral transport values excluded;
5. independently recorded response body byte count and any server `Content-Length`;
6. independent SHA-256 and comparison with the accepted digest;
7. static archive inventory and all safety findings;
8. exact cache inventory and file sizes/hashes;
9. network-disable confirmation and observed destination summary;
10. stop-condition and anomaly register, including zero findings explicitly;
11. confirmation that no archive extraction or executable invocation occurred;
12. confirmation that no Go module, checksum lookup, toolchain cache, installation, service, fixture, build, or test exists; and
13. rollback/retention status.

The archive, raw network logs, and temporary evidence remain outside Git. Only a separately reviewed, normalized, redacted documentation package may later be proposed for the repository.

## Result classification

| Result | Meaning | Next action |
|---|---|---|
| `Verified archive bytes` | One response completed; independent byte count recorded; SHA-256 matched; static archive checks passed | Retain the exact archive in the disposable cache for review; do not extract or execute |
| `Stopped — route deviation` | Host/path/method/redirect/auth/retry boundary failed | Preserve bounded sanitized evidence, remove incomplete bytes, and return for user direction |
| `Stopped — integrity or archive failure` | Byte count, hash, or static archive checks failed | Remove rejected bytes, preserve normalized evidence, and return for user direction |
| `Incomplete` | Transfer did not complete or evidence could not reconcile | Remove partial bytes, preserve normalized evidence, and return for user direction |

No R3-G1 result passes Checkpoint A or Gate 2, approves the Go toolchain for execution, closes the Go graph, or authorizes R3-O1.

## Rollback and retention

On interruption or rejection:

1. close the exact acquisition client and network path;
2. verify no process has an executable, working directory, or open file beneath the recorded root;
3. remove the exact recorded `.part` file after validating its realpath is beneath the sentinel root;
4. retain only sanitized evidence needed for review; and
5. report the remaining root inventory without broad cleanup.

After successful verification, retain the archive and evidence in the disposable root until user review. Retention is not installation or execution authority. If later removal is authorized, validate the exact root, owner, mode, realpath, sentinel, inventory, non-symlink, and non-mount state before removing only that root and confirming its absence.

No global cache purge, package uninstall, broad recursive deletion, wildcard target, Git cleanup/reset, or unrelated process termination is permitted.

## Specialist authorization checks

| Review function | Required finding before authorization |
|---|---|
| Maintenance / supply chain | Exact URL/version/hash agrees with accepted R1/R2 evidence; rounded publisher size is non-authoritative under accepted `U-R2-GO-01` |
| Security / privacy | One host/path, no redirect/retry/auth, owner-only root, disabled credential/proxy fallbacks, and no durable secret or external data transfer |
| Licensing / cost | Recorded Go license route; no account, payment, package manager, additional component, or distribution action |
| Quality / independent review | One request, one expected archive, exact hash, explicit byte-count rule, archive-safety checks, and evidence reconciliation are independently checkable |
| Orchestrator / governance | Authorization is R3-G1 only; stop occurs before extraction, execution, modules, graph work, another route, R4, Checkpoint B, or stack selection |

Any disagreement is recorded and blocks authorization until resolved explicitly.

## Explicit exclusions

Approval of R3-G1 would not authorize:

- editing or committing the accepted dependency manifest or persistent allowlist;
- a request to any host or path other than the one exact Go archive URL;
- a second request, redirect, retry, resume/range request, mirror, or fallback;
- downloading `.info`, `.mod`, `.zip`, checksum-database, Git, or source payloads;
- extracting or executing the Go archive or writing `GOROOT`, `GOPATH`, `GOBIN`, `GOCACHE`, `GOMODCACHE`, or `GOENV`;
- running `go version`, `go env`, `go list`, `go mod`, a compiler, linker, build, or test;
- acquiring or using Podman, age, Sigsum, PostgreSQL, OCI objects, Python artifacts, or any other dependency;
- creating a fixture, account credential, key, service, listener, container, image, database, prototype, SBOM, or product-generated artifact;
- accessing an account, real correspondence, live archive, cloud AI, telemetry, or production infrastructure;
- beginning R3-O1, G2/G3 graph work, R4, Checkpoint B, prototype implementation, stack selection, or a stack-selection ADR; or
- committing acquisition evidence or pushing.

## Required explicit authorization

R3-G1 may begin only after the user gives an instruction substantively equivalent to:

> I authorize R3-G1 only under `R3-G1-GO-ARCHIVE-AUTHORIZATION-REQUEST.md`: make one direct, no-redirect, no-retry GET for the exact Go 1.27.1 macOS arm64 archive; record the authoritative response byte count and independently verify SHA-256; perform static archive inspection without extraction or execution; disconnect and stop for evidence review. No module, other host, installation, execution, build, test, R3-O1, or later stage is authorized.

Approval of Gate R2-A, approval of `U-R2-GO-01`, or a general instruction to continue is not R3-G1 authorization.

## Review request

Review is requested on the one-request boundary, authoritative byte-count/hash rule, temporary host/path activation, cache layout, stop conditions, evidence package, rollback, and exact authorization language. Until approval is explicit, R3-G1 remains unstarted and `dl.google.com` remains inactive.
