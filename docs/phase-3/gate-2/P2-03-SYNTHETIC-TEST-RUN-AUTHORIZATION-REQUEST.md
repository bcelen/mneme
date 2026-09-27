# P2-03 Synthetic Test Run Authorization Request

**Status:** Proposed
**Request date:** 2026-09-18
**Reconciliation date:** 2026-09-19
**Review date:** Pending
**Execution readiness:** Not ready; P2-03 source and P2-04 static review are Accepted, but P3-01 build authorization, a validated literal execution root, and final user test authorization remain unresolved
**Current authority:** Review only; no Go invocation, compilation, test run, toolchain copy, cache, disposable root, generated output, retained-input read, dependency change, network action, commit, or push is authorized
**Accepted planning decision:** [P2-03 synthetic fixtures and planner tests](P2-03-SYNTHETIC-FIXTURES-AND-TESTS-PROPOSAL.md), commit `19b9bc54092d024e2010040c1f4a9c3729ae3268`
**Accepted source-generation request:** [P2-03 fixture generation](P2-03-SYNTHETIC-FIXTURE-GENERATION-AUTHORIZATION-REQUEST.md), commit `1661b3f4e2aa4a7a6d42c030c665af5038e1b471`
**Accepted source package:** commit `649bb5bf62529bfdc7d0e84804d00f47723cafa3`
**Accepted static review:** [P2-04 specialist findings](P2-IMPLEMENTATION-REVIEW-FINDINGS.md), commit `71de695d4da565647ed791dd77e2617894a4c582`

## Purpose

This request freezes the future synthetic test-run boundary independently from fixture/test-source generation. It would eventually authorize exactly one isolated `go test` process covering the module-root provenance test and the planner package's synthetic tests.

This request does not authorize source creation, a standalone planner build, retained-input execution, or any current action. It cannot become executable merely because the planning decision or fixture-generation request is approved.

## 2026-09-19 reconciliation record

The prior Proposed request had SHA-256 `9f0cafd4980ecd62d31f565d9af5d44bf686cdb6fcaf6b49e3047734bd8319e6`. Reconciliation against the accepted P2-03 source package and accepted P2-04 findings established:

| Item | Prior request state | Reconciled state |
|---|---|---|
| P2-03 fixture/test source | Not created | Accepted at commit `649bb5bf62529bfdc7d0e84804d00f47723cafa3` |
| P2-04 implementation review | Not prepared | Accepted at commit `71de695d4da565647ed791dd77e2617894a4c582` |
| Accepted implementation commit | Placeholder | `649bb5bf62529bfdc7d0e84804d00f47723cafa3` |
| Complete source closure | One unresolved aggregate-manifest placeholder | Three accepted self-excluding manifests covering 20 rows plus the three manifests: 23 paths and 141,746 bytes |
| Synthetic-test manifest | Placeholder | SHA-256 `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` |
| Accepted findings identity | Absent | 395 lines, 33,706 bytes; SHA-256 `9afe8dc0cdb1d93462ff6dba04a52a5cd80883194c4738793700e2832d77dbb8` |
| Source bytes after P2-03 | Unresolved | No change from commit `649bb5b` through findings commit `71de695` |

No aggregate source manifest was created. The accepted complete-source closure remains the three independently hashed, self-excluding manifests accepted by P2-04. This revision does not change the proposed test command, package scope, toolchain identity, root design, isolation controls, evidence requirements, stop conditions, or approval gate.

## Hard prerequisite gates

| Prerequisite | Current state | Required accepted evidence before test execution |
|---|---|---|
| P2-03 fixture/test source | Accepted 2026-09-18 | Commit `649bb5bf62529bfdc7d0e84804d00f47723cafa3`; exact eight-path package; synthetic manifest SHA-256 `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` |
| P2-04 implementation review | Accepted 2026-09-19 | Commit `71de695d4da565647ed791dd77e2617894a4c582`; findings SHA-256 `9afe8dc0cdb1d93462ff6dba04a52a5cd80883194c4738793700e2832d77dbb8`; seven static `Pass` findings with runtime claims preserved as unproved |
| P3-01 build authorization | Not prepared | Exact offline build/toolchain/source-copy procedure accepted independently |
| P3 decision | Not prepared | User explicitly authorizes this one test command after all literal hashes and paths are resolved |

Any missing or merely Proposed prerequisite is a hard stop. Acceptance of this document as a framework would not fill a placeholder or authorize execution.

## Required accepted source identities

The accepted P2 source identities are:

| Artifact | Required value |
|---|---|
| Accepted P2 implementation source commit | `649bb5bf62529bfdc7d0e84804d00f47723cafa3` |
| Accepted P2-04 findings commit | `71de695d4da565647ed791dd77e2617894a4c582` |
| Accepted P2-04 findings SHA-256 | `9afe8dc0cdb1d93462ff6dba04a52a5cd80883194c4738793700e2832d77dbb8` |
| Complete accepted source closure | 23 regular paths; 141,746 bytes; 20 manifest rows plus three self-excluding manifests |
| Planner-owned source-manifest SHA-256 | `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84` |
| Copied-tlog manifest SHA-256 | `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d` |
| Synthetic-test source-manifest SHA-256 | `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` |
| `go.mod` SHA-256 | `611f1b084ded3e5c0014d7f420d05c58b88e2bb727fb1fa792feccd29541e742` |
| Accepted Go compiler binary SHA-256 | `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598` |

No P2 source-identity placeholder remains. This does not make the request executable: the P3-01 procedure, its accepted evidence, the validated literal replacement for `<P3_ROOT>`, and explicit user test authorization are still absent. Runtime substitution or inference is forbidden.

## Exact test scope

The future test process may load exactly two local package arguments:

```text
.
./internal/planner
```

The module-root package may execute only the accepted `sourcebundle_test.go` provenance tests. The planner package may execute only the accepted `*_test.go` files manifested by P2-03.

No `./...`, `./cmd/...`, direct `./internal/tlog` test, benchmark, fuzz target, example execution, race detector, coverage instrumentation, vet, generate, list, module, graph, install, or standalone `go build` action is included.

`go test` necessarily compiles temporary test binaries and local packages inside the isolated cache. That internal compilation is part of this one future test process. It is not standalone planner-build authority, binary-acceptance evidence, or permission to run the planner command.

## Exact future command

The future working directory must be:

```text
<P3_ROOT>/source/r3-g2-tile-planner
```

The only proposed test command is:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C TZ=UTC TMPDIR=<P3_ROOT>/tmp GOROOT=<P3_ROOT>/toolchain/go GOPATH=<P3_ROOT>/state/gopath GOMODCACHE=<P3_ROOT>/state/gomodcache GOCACHE=<P3_ROOT>/state/gocache GOTMPDIR=<P3_ROOT>/state/gotmp GOENV=off GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off GOPRIVATE= GONOPROXY= GONOSUMDB= GOVCS=*:off GOAUTH=off CGO_ENABLED=0 <P3_ROOT>/toolchain/go/bin/go test -mod=readonly -count=1 -shuffle=off -timeout=60s . ./internal/planner
```

`<P3_ROOT>` is explanatory notation only. A later revision must replace every occurrence with one validated literal owner-only root before execution approval. `HOME` and all unlisted variables remain absent because the command uses `env -i`.

The command may be invoked exactly once. The orchestration timeout is 90 seconds. A nonzero exit, timeout, signal, unexpected package, dependency lookup, or environmental deviation stops the workstream. No retry or narrower rerun is authorized.

## Toolchain boundary

The future root may contain only an independently copied accepted Go 1.27.1 toolchain whose `go` binary matches:

```text
132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598
```

Toolchain copy/extraction is not authorized by this request. It belongs to a separately reviewed P3-01 procedure. The test command may not invoke a system Go, download a toolchain, select another version, use `GOTOOLCHAIN=auto`, or reach a package manager.

Compiler/linker subprocesses launched internally by the accepted Go test driver must remain descendants of that exact toolchain and operate only within the owner-only root. No test helper or planner source may start a process.

## Disposable root and isolation

The later test run must occur under one fresh owner-only root matching the accepted P2-03 boundary:

```text
/tmp/mneme-phase3-p3.XXXXXX
```

The validated expanded root must be mode `0700`, owned by UID 501, a non-symlink, not a mount point, and contain a matching `MNEME_PHASE3_DISPOSABLE.json` sentinel. Proposed layout:

```text
<P3_ROOT>/
├── MNEME_PHASE3_DISPOSABLE.json
├── toolchain/
│   └── go/
├── source/
│   └── r3-g2-tile-planner/
├── tmp/
├── state/
│   ├── gopath/
│   ├── gomodcache/
│   ├── gocache/
│   └── gotmp/
└── evidence/
    ├── source-copy-manifest.tsv
    ├── environment.json
    ├── command-ledger.tsv
    ├── test-process.tsv
    ├── test-results.tsv
    ├── package-inventory.tsv
    ├── filesystem-preflight.tsv
    ├── filesystem-postflight.tsv
    ├── network-preflight.tsv
    ├── network-postflight.tsv
    ├── rollback.json
    └── stop-register.md
```

Every directory is mode `0700`; source and evidence files are mode `0600`. Toolchain executables may retain the accepted executable modes. The repository and all retained roots remain read-only sources; the test process receives only a byte-identical copied source tree.

External networking must be denied independently of Go environment variables. Preflight must prove no matching prior root, process, listener, connection, cache, user configuration, credential path, or inherited proxy exists.

## Input boundary

The test process may read only:

- the accepted copied source tree under `<P3_ROOT>/source/r3-g2-tile-planner`;
- the accepted local Go toolchain and standard library under `<P3_ROOT>/toolchain/go`;
- root-contained Go state/cache paths; and
- synthetic temporary files created by the accepted tests beneath `<P3_ROOT>/tmp`.

It may not read the repository checkout directly, R3-G1/R3-G2/P2-02 retained roots, real checksum lookups, checksum tiles, user-home files, global Go caches, credentials, keys, correspondence, accounts, or production data.

## Output boundary

Permitted outputs are limited to:

- Go-managed temporary test binaries and compiler/cache files beneath the declared root;
- synthetic manifests, lookup files, symlinks, and planner-output trees created only inside test-owned temporary directories;
- sanitized local stdout/stderr from the one test command; and
- the twelve exact evidence files listed in the root layout.

The process may not write the source copy, repository, `go.mod`, `go.sum`, workspace files, fixture source, snapshots, golden files, coverage profiles, standalone planner binaries, SBOMs, license reports, network responses, service state, databases, containers, or production paths.

Every temporary fixture and planner output must remain synthetic, unverified, and disposable. Planner output generated inside a test is test-local evidence only; it must not be promoted to R3-G2 retained-input evidence or a tile-acquisition manifest.

## Required preflight

Before invoking Go, a later authorized operator must:

1. resolve the execution-root notation to an accepted literal value and confirm every source, toolchain, command, and root identity is literal;
2. verify the accepted repository commit and all three source-manifest hashes;
3. copy the accepted source independently into the root and prove byte identity without modifying the repository;
4. verify the toolchain binary and complete toolchain provenance under accepted P3-01 evidence;
5. validate root owner, mode, sentinel, path identity, non-symlink, non-mount, empty output/cache state, and allowed inventory;
6. prove external network denial and zero prior process/listener/connection;
7. confirm `go.mod` has no dependency directive and `go.sum` is absent;
8. verify exact test package arguments and command bytes;
9. confirm no retained-input, key, credential, user-home, service, or global-cache path exists beneath the root; and
10. stop if any check differs.

No preflight step may invoke Go. Go is invoked only once by the accepted test command.

## Required evidence after the run

The review package must include:

1. accepted commit and source/toolchain identity reconciliation;
2. literal expanded root, sentinel, owner, mode, path-identity, mount, process, listener, and open-file evidence;
3. exact sanitized environment and one-command ledger;
4. test-process executable, ancestry, working directory, start/exit state, timeout state, and exit code;
5. exact package inventory proving only `.` and `./internal/planner` ran;
6. test case/function counts, pass/fail/skip status, and sanitized failure details;
7. source pre/post hash comparison proving zero mutation;
8. complete root filesystem inventory and root-contained cache/temp writes;
9. zero external dependency, module download, `go.sum`, workspace, network request/listener, credential, key, verifier, retained-input, planner-command, standalone-build, graph-command, service, and production-output counts;
10. isolation postflight, stop register, rollback/retention state, uncertainties, and disagreements; and
11. all seven specialist findings.

Test success would not accept P4 evidence, authorize retained-input planner execution, or prove checksum integrity.

## Stop conditions

Stop without retry, repair, fallback, or narrower rerun if:

- a prerequisite, literal path, hash, placeholder resolution, source copy, toolchain identity, root control, or network-denial check fails;
- Go attempts a dependency, proxy, checksum-service, VCS, toolchain, credential, user-home, or external path access;
- a package other than `.` or `./internal/planner` is selected as a test target;
- `go.mod`, `go.sum`, source, fixture, snapshot, golden file, or repository content changes;
- a test reads retained/live data, uses a verifier/key, launches a helper process, opens a listener, or contacts a host;
- the command exits nonzero, times out, receives a signal, or is invoked a second time;
- an output escapes the root or an undeclared output/evidence file appears;
- source/postflight, process, network, filesystem, rollback, or specialist evidence cannot reconcile; or
- P3-01, the literal-root revision, final user test authorization, or another required gate remains incomplete.

On stop, preserve the bounded owner-only root and evidence, mark the result `Incomplete`, do not rerun any package or case, and return for review.

## Rollback and retention

After either success or stop, retain the exact owner-only root until user review. Do not alter the repository or accepted retained roots.

Cleanup requires a separate explicit instruction and must validate the exact expanded root, UID, mode, sentinel, path identity, non-symlink, non-mount, process, listener, open-file, and complete inventory state before removing only that root. No wildcard deletion, Git reset, checkout, global Go-cache cleanup, package uninstall, toolchain removal outside the root, or unrelated-process termination is permitted.

## Specialist reviews required

| Review function | Required finding |
|---|---|
| Security / privacy | Network denial, hostile synthetic inputs, path/symlink controls, no key/credential/home/retained-data path, and root confinement pass |
| Quality / independent verification | Exact packages/cases ran once; results, caps, failures, sentinel, fallback, outputs, and determinism evidence are complete |
| Supply chain / maintenance | Exact compiler/source identities pass; no dependency, download, `go.sum`, workspace, or undeclared tool appears |
| Preservation / provenance | Repository and accepted source remain unchanged; copied source and test outputs have complete provenance |
| Licensing / cost | No new dependency, account, external service, paid resource, or license obligation appears |
| Architecture / portability | Test run remains disposable experimental evidence with no product-stack commitment |
| Orchestrator / governance | Test authority does not include standalone build acceptance, retained-input execution, verifier, graph, R3-O1, or later gates |

Any disagreement or non-`Pass` finding blocks acceptance of the test evidence.

## Explicit non-authorization

This Proposed request does not authorize:

- creating the disposable root, copying a toolchain/source tree, invoking Go, compiling, or running tests;
- creating or modifying the accepted fixture/test source or reopening the completed fixture-generation workstream;
- running `go build`, `go vet`, `go generate`, `go list`, `go mod graph`, another graph command, benchmark, fuzz, race, coverage, install, or planner command;
- adding a dependency, changing `go.mod`, creating `go.sum`, or contacting a proxy, checksum service, VCS host, package manager, or any network host;
- reading retained lookups, tiles, correspondence, credentials, accounts, keys, user configuration, or production data;
- using a verifier, cloud AI, telemetry, analytics, service, listener, database, or container;
- beginning P4, P4-E, R3-O1, Checkpoint B, deployment, stack selection, or production work;
- committing this request, test evidence, generated output, or the still-Proposed planner-execution request; or
- pushing.

## Independent approval gate

This request must remain Proposed until P3-01 is independently accepted, the execution root and every remaining execution identity are literal, and the user reviews and explicitly authorizes the fully resolved request. P2-03 source acceptance and P2-04 static-review acceptance satisfy only those two prerequisites.

Approval of fixture generation does not approve this request. Approval of this request does not authorize fixture generation or standalone build work.

## Review request

Review is requested on the hard prerequisites, source/toolchain identities, one-command/two-package scope, internal-compilation boundary, environment, root layout, inputs, outputs, isolation, evidence, stop conditions, rollback, specialist reviews, and independent approval gate.

Until a fully resolved revision is separately accepted and explicitly authorized, no synthetic test process may begin.
