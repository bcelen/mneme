# P3-01 Offline Build and Execution-Root Authorization Proposal

**Status:** Proposed
**Proposal date:** 2026-09-19
**Review date:** Pending
**P3 item:** `P3-01`
**Root creation state:** Not created; no literal expanded root exists
**Execution readiness:** Not ready; root allocation, root validation, toolchain extraction, source copying, Go invocation, and build execution are not authorized
**Current authority:** Review this document only; do not create a root, read or copy the retained Go archive, extract or execute Go, copy source, create a cache, build, test, access the network, or generate evidence
**Governing prerequisite:** [R3-G2 planner prerequisite-resolution record](R3-G2-PLANNER-PREREQUISITE-RESOLUTION.md)
**Accepted P2 source:** commit `649bb5bf62529bfdc7d0e84804d00f47723cafa3`
**Accepted P2 review:** [P2-04 specialist findings](P2-IMPLEMENTATION-REVIEW-FINDINGS.md), commit `71de695d4da565647ed791dd77e2617894a4c582`
**Dependent request:** [P2-03 synthetic test-run authorization request](P2-03-SYNTHETIC-TEST-RUN-AUTHORIZATION-REQUEST.md), status `Proposed`, SHA-256 `d7b83e514feb16238b2228b623a692f95c5cd2e2aff6af4bb20ded95f537ca65`

## Purpose

P3-01 defines the future offline build boundary and the root, compiler, command, environment, isolation, write, rollback, and evidence controls that must exist before a synthetic test can be authorized.

This proposal does not create or validate a root and does not execute any command described below. It cannot honestly record a literal expanded `mktemp` result while root creation is forbidden. The notation `<P3_ROOT>` is therefore a deliberate blocker, not an executable substitution mechanism.

P3-01 may become executable only after a separately authorized root-resolution step creates one fresh root, validates it, records its literal identity, and produces a revised P3-01 document with every `<P3_ROOT>` occurrence replaced. The final explicit test authorization request must use that same accepted literal identity and the exact accepted P3-01 document hash.

## Governing accepted identities

### P2 source closure

| Artifact | Accepted identity |
|---|---|
| P2 implementation source commit | `649bb5bf62529bfdc7d0e84804d00f47723cafa3` |
| P2-04 findings commit | `71de695d4da565647ed791dd77e2617894a4c582` |
| P2-04 findings SHA-256 | `9afe8dc0cdb1d93462ff6dba04a52a5cd80883194c4738793700e2832d77dbb8` |
| Complete source closure | 23 regular paths; 141,746 bytes; 20 manifest rows plus three self-excluding manifests |
| Planner-owned source manifest | SHA-256 `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84` |
| Copied-tlog manifest | SHA-256 `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d` |
| Synthetic-test source manifest | SHA-256 `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` |
| `go.mod` | 59 bytes; SHA-256 `611f1b084ded3e5c0014d7f420d05c58b88e2bb727fb1fa792feccd29541e742` |

No aggregate source manifest is introduced. The three accepted self-excluding manifests remain the authoritative source closure.

### Toolchain identity

| Field | Required identity |
|---|---|
| Retained archive root | `/tmp/mneme-phase3-r3-g1.UQ7udQ` |
| Retained archive path | `/tmp/mneme-phase3-r3-g1.UQ7udQ/downloads/go/go1.27.1.darwin-arm64.tar.gz` |
| Archive byte count | 68,100,347 |
| Archive SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Archive platform | Go 1.27.1, Darwin arm64 |
| Future compiler path | `<P3_ROOT>/toolchain/go/bin/go` |
| Future compiler SHA-256 | `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598` |
| Permitted version result after execution authority | `go version go1.27.1 darwin/arm64` |

The retained archive has accepted verified-byte and static-inspection evidence only. This proposal does not authorize opening, copying, extracting, installing, or executing it. A later root-resolution authorization must revalidate the archive's path, type, owner, mode, byte count, and SHA-256 before a copy or extraction.

The toolchain may exist only below the future root. It must not write `/usr/local/go`, `/etc/paths.d/go`, a shell profile, Homebrew state, a global cache, or another system/user location.

## Staged approval model

| Stage | State | Permitted result |
|---|---|---|
| `P3-01-D` — design review | Current | Review this Proposed document only; no filesystem or process action |
| `P3-01-R` — root resolution | Not authorized | Create and validate one root, copy/extract the accepted toolchain, copy accepted source, and produce static preflight evidence; no Go invocation |
| `P3-01-L` — literal revision | Blocked | Replace every `<P3_ROOT>` with the validated literal path, record evidence hashes, and present the complete revised diff |
| `P3-01-B` — build execution | Blocked | Only after separate explicit authorization, invoke the two exact offline build commands and stop for evidence review |
| Final synthetic-test authorization | Blocked | Only after P3-01 review and accepted root identity, revise the test request with the same literal root and accepted P3-01 hash |

Approval of one stage does not authorize the next. In particular, review of this proposal does not authorize root creation, and root resolution would not authorize Go or a build.

## Literal root-resolution contract

The only permitted future root-allocation command path is `/usr/bin/mktemp`, using the exact template:

```text
/tmp/mneme-phase3-p3.XXXXXX
```

The resulting expanded path must be recorded exactly once as `<P3_ROOT>` and must satisfy all of these checks before any retained archive or repository source is read for copying:

1. it is an absolute path directly beneath `/tmp` and matches the template's fixed prefix;
2. it is newly created, owned by UID 501, and mode `0700`;
3. it is a directory, not a symlink, hard link, mount point, alias, or pre-existing path;
4. its physical path and textual path agree under the accepted path-identity method;
5. it contains only the matching `MNEME_PHASE3_DISPOSABLE.json` sentinel before layout creation;
6. the sentinel records the literal root, run identifier, authorization-document hash, owner UID, creation time, source commit, toolchain archive hash, and allowed path inventory;
7. no prior matching process, open file, listener, connection, root, cache, or evidence path exists; and
8. any missing or anomalous check stops before toolchain or source copying.

The future root-resolution package must record the literal root and SHA-256 of its sentinel. Until then, `<P3_ROOT>` is unresolved and every command below is documentary only.

## Proposed root layout

The future root may contain exactly:

```text
<P3_ROOT>/
├── MNEME_PHASE3_DISPOSABLE.json
├── toolchain/
│   └── go/
├── source/
│   └── r3-g2-tile-planner/
├── build-a/
├── build-b/
├── tmp/
│   ├── build-a/
│   ├── build-b/
│   └── test/
├── state/
│   ├── build-a/
│   │   ├── gopath/
│   │   ├── gomodcache/
│   │   ├── gocache/
│   │   └── gotmp/
│   ├── build-b/
│   │   ├── gopath/
│   │   ├── gomodcache/
│   │   ├── gocache/
│   │   └── gotmp/
│   └── test/
│       ├── gopath/
│       ├── gomodcache/
│       ├── gocache/
│       └── gotmp/
└── evidence/
    ├── root-allocation.json
    ├── sentinel.sha256
    ├── source-copy-manifest.tsv
    ├── toolchain-archive-recheck.tsv
    ├── toolchain-extraction-manifest.tsv
    ├── compiler-identity.tsv
    ├── environment-build-a.json
    ├── environment-build-b.json
    ├── command-ledger.tsv
    ├── process-ledger.tsv
    ├── filesystem-preflight.tsv
    ├── filesystem-postflight.tsv
    ├── network-preflight.tsv
    ├── network-observation.tsv
    ├── network-postflight.tsv
    ├── build-results.tsv
    ├── binary-comparison.tsv
    ├── workspace-checksums.sha256
    ├── rollback.json
    └── stop-register.md
```

Directories must be mode `0700`. Source and evidence files must be mode `0600`. Accepted toolchain executables and the two future build outputs may retain mode `0700`. No path may be a symlink, hard link to a path outside the root, mount point, socket, device, FIFO, or alias.

The `test/` state and temporary directories are reserved for the later final test request. P3-01 may create them during an authorized root-resolution step but may not invoke a test or write test output.

## Exact command-path allowlist

Only these command paths may be proposed in the later literal ledger:

| Path | Future purpose |
|---|---|
| `/usr/bin/mktemp` | Allocate the one fresh root |
| `/usr/bin/id` | Record owner identity |
| `/usr/bin/stat` | Record path type, mode, owner, inode, and link count |
| `/usr/bin/realpath` | Establish physical path identity; absence or failure is a stop requiring revised review |
| `/usr/bin/find` | Enumerate only named root/source/toolchain subtrees |
| `/usr/bin/shasum` | Calculate SHA-256 identities |
| `/usr/bin/wc` | Calculate independent byte counts |
| `/usr/bin/cmp` | Compare exact files and binaries |
| `/usr/bin/diff` | Produce bounded local comparisons |
| `/usr/bin/env` | Create the empty Go process environment |
| `/usr/bin/tar` | Extract only the accepted archive into the root |
| `/usr/bin/pgrep` | Observe matching processes |
| `/usr/bin/sandbox-exec` | Apply the reviewed deny-network/write-confinement profile; never sole isolation evidence |
| `/usr/sbin/lsof` | Observe open files, listeners, and connections |
| `/usr/sbin/netstat` | Observe network state |
| `/sbin/mount` | Reject a mount-point root |
| `/bin/chmod` | Apply owner-only modes |
| `/bin/cp` | Copy accepted source/archive bytes into the root |
| `/bin/ls` | Produce bounded directory evidence |
| `/bin/mkdir` | Create only the literal layout directories |
| `<P3_ROOT>/toolchain/go/bin/go` | Future accepted compiler/test driver; blocked until explicit Go authorization |

No shell profile, package manager, downloader, VCS client, service manager, container runtime, interpreter, installer, compiler other than the accepted Go binary, or command found through ambient `PATH` may be added.

The final literal ledger must expand every root-relative command path and argument. It must not use command substitution, wildcard source selection, unresolved environment variables, aliases, functions, search-path discovery, retries, or fallbacks.

## Source-copy contract

A later root-resolution step may copy only the accepted 23-path source closure from:

```text
/Users/bogac/dev/forgejo/mneme/experiments/phase-3/r3-g2-tile-planner
```

Before copying, static checks must prove that the source tree is unchanged from commit `649bb5b` and that all 20 manifest rows plus the three self-excluding manifest hashes reconcile. The destination must initially be absent and then contain exactly the same 23 regular files, relative paths, byte counts, modes, and SHA-256 values.

The repository is a read-only copy source. No source file, manifest, module file, fixture, test, license, or repository metadata may be written or normalized. No `.git` directory is copied into the root.

`source-copy-manifest.tsv` must record source path, destination path, byte count, SHA-256, source commit, source manifest class, mode, copy result, and post-copy comparison for every path.

## Toolchain extraction contract

A later root-resolution step must:

1. revalidate the retained archive without modifying it;
2. copy the archive once into a root-owned staging location recorded in the command ledger;
3. verify the copied archive's size and SHA-256;
4. extract only beneath `<P3_ROOT>/toolchain/`;
5. require the single top-level `go/` tree and the accepted no-link/no-traversal static archive properties;
6. reject an absolute, traversal, duplicate, link, device, FIFO, privileged-mode, or out-of-root member;
7. remove no retained artifact and install nothing globally;
8. statically hash `<P3_ROOT>/toolchain/go/bin/go` and require `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598`; and
9. stop before executing the binary.

The copied archive may be retained inside the root only until extraction evidence is accepted. Its exact path and later disposition must be recorded; no cleanup is implied by this proposal.

## Exact future build environments

Each future Go process must use `/usr/bin/env -i`. `HOME` and every unlisted variable are absent.

Build A environment:

```text
PATH=/usr/bin:/bin
LC_ALL=C
TZ=UTC
TMPDIR=<P3_ROOT>/tmp/build-a
GOROOT=<P3_ROOT>/toolchain/go
GOPATH=<P3_ROOT>/state/build-a/gopath
GOMODCACHE=<P3_ROOT>/state/build-a/gomodcache
GOCACHE=<P3_ROOT>/state/build-a/gocache
GOTMPDIR=<P3_ROOT>/state/build-a/gotmp
GOENV=off
GOTOOLCHAIN=local
GOWORK=off
GOPROXY=off
GOSUMDB=off
GOPRIVATE=
GONOPROXY=
GONOSUMDB=
GOVCS=*:off
GOAUTH=off
CGO_ENABLED=0
```

Build B uses the identical values except that every `state/build-a` and `tmp/build-a` path is replaced by its `build-b` counterpart.

No proxy variable, credential helper, netrc path, SSH agent, keychain path, user Go configuration, global cache, telemetry variable, analytics variable, update mechanism, locale variation, or inherited environment value is permitted.

## Exact future build commands

The future working directory for both commands is:

```text
<P3_ROOT>/source/r3-g2-tile-planner
```

Build A:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C TZ=UTC TMPDIR=<P3_ROOT>/tmp/build-a GOROOT=<P3_ROOT>/toolchain/go GOPATH=<P3_ROOT>/state/build-a/gopath GOMODCACHE=<P3_ROOT>/state/build-a/gomodcache GOCACHE=<P3_ROOT>/state/build-a/gocache GOTMPDIR=<P3_ROOT>/state/build-a/gotmp GOENV=off GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off GOPRIVATE= GONOPROXY= GONOSUMDB= GOVCS=*:off GOAUTH=off CGO_ENABLED=0 <P3_ROOT>/toolchain/go/bin/go build -mod=readonly -trimpath -buildvcs=false -o <P3_ROOT>/build-a/mneme-r3-g2-tile-plan ./cmd/mneme-r3-g2-tile-plan
```

Build B:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C TZ=UTC TMPDIR=<P3_ROOT>/tmp/build-b GOROOT=<P3_ROOT>/toolchain/go GOPATH=<P3_ROOT>/state/build-b/gopath GOMODCACHE=<P3_ROOT>/state/build-b/gomodcache GOCACHE=<P3_ROOT>/state/build-b/gocache GOTMPDIR=<P3_ROOT>/state/build-b/gotmp GOENV=off GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off GOPRIVATE= GONOPROXY= GONOSUMDB= GOVCS=*:off GOAUTH=off CGO_ENABLED=0 <P3_ROOT>/toolchain/go/bin/go build -mod=readonly -trimpath -buildvcs=false -o <P3_ROOT>/build-b/mneme-r3-g2-tile-plan ./cmd/mneme-r3-g2-tile-plan
```

Each command may run at most once, in order, with a proposed command timeout of 120 seconds and orchestration timeout of 150 seconds. Build B must not start if Build A stops. No retry, alternate flag, narrower package, cache reuse, system Go, install, test, vet, generate, list, graph, module, race, coverage, fuzz, cross-build, plugin, shared-library, or fallback command is included.

These command forms are not executable while `<P3_ROOT>` remains unresolved or while this document remains Proposed.

## Isolation requirements

External network denial must be enforced independently of Go environment variables. The later literal revision must include a reviewed `sandbox-exec` profile or an equivalently narrow host control that:

- denies all network operations;
- permits process execution only for the accepted Go toolchain descendants and listed observation utilities;
- permits reads only from the root-contained toolchain/source/state plus required system runtime libraries;
- permits writes only beneath the exact root state, temporary, build, and evidence paths;
- denies user-home, keychain, SSH agent, credential, retained lookup, correspondence, repository-write, service, listener, database, container, and device paths; and
- fails closed on an unlisted access.

`sandbox-exec` must not be the sole proof. Evidence must combine the reviewed source capability scan, empty environment, `GOPROXY=off`, `GOSUMDB=off`, `GOVCS=*:off`, root-contained caches, process ancestry, filesystem observation, and pre/during/post network observation.

Before any future Go invocation, preflight must establish:

1. accepted literal root and sentinel identity;
2. exact toolchain archive, extraction, compiler, and source-copy identities;
3. empty independent Build A and Build B cache/temp/output paths;
4. no `go.sum`, workspace, dependency payload, VCS metadata, credential, key, retained input, or unexpected executable in the source copy;
5. no prior matching Go/compiler process, open file, listener, or connection;
6. exact command and environment bytes;
7. external network denial active before process creation; and
8. repository source unchanged and not writable by the build process.

Any unavailable isolation control, command-path mismatch, or evidence gap is a stop requiring revised review. Observation alone must not be substituted for prevention.

## Writable-location allowlist

Future root resolution may write only:

- `<P3_ROOT>/MNEME_PHASE3_DISPOSABLE.json`;
- the exact directory layout;
- `<P3_ROOT>/toolchain/` and its bounded archive staging path;
- `<P3_ROOT>/source/r3-g2-tile-planner/` during the one source copy; and
- `<P3_ROOT>/evidence/` static root-resolution evidence.

Future Build A may additionally write only:

- `<P3_ROOT>/build-a/mneme-r3-g2-tile-plan`;
- `<P3_ROOT>/tmp/build-a/`;
- `<P3_ROOT>/state/build-a/`; and
- the exact Build A evidence rows.

Future Build B may additionally write only the corresponding `build-b`, `tmp/build-b`, `state/build-b`, and Build B evidence paths.

The repository, retained Go root, user home, global Go locations, `/usr/local`, `/etc`, `/Library`, `/Applications`, system temporary paths outside the literal root, and every retained-input/evidence root are read-only or inaccessible. No other output is permitted.

## Future build result and evidence requirements

If separately authorized, the build workstream must stop with a review package containing:

1. literal root, sentinel, owner, mode, physical path, non-symlink, non-mount, and prior-state evidence;
2. archive source/destination, byte-count, SHA-256, copy, extraction, and complete toolchain inventory evidence;
3. compiler path, type, mode, SHA-256, and authorized version-output evidence;
4. all 23 source-copy rows and three accepted manifest reconciliations;
5. exact Build A and Build B environments and command bytes;
6. sandbox/isolation profile identity and enforcement result;
7. process executable, ancestry, working directory, start/stop, timeout, signal, and exit evidence;
8. network preflight, during-build observation, and postflight with zero request, connection, DNS, and listener results;
9. complete preflight and postflight filesystem inventories;
10. Build A and Build B output paths, types, modes, byte counts, and SHA-256 values;
11. exact binary byte comparison and reproducibility finding;
12. source pre/post comparison proving zero mutation;
13. explicit zero counts for dependency download, external module, `go.sum`, workspace, VCS access, credential, key, retained-input read, test, planner execution, graph command, service, database, container, and write outside the root;
14. complete command, anomaly, uncertainty, disagreement, and stop registers;
15. `workspace-checksums.sha256` for every retained root artifact except its documented self-exclusion; and
16. rollback/retention state plus the four required specialist findings.

Build success would not authorize tests, accept a binary for retained-input execution, prove portability, close P4, or prove checksum integrity.

## Stop conditions

Stop without retry, repair, substitution, cleanup, narrower command, or fallback if:

- the literal root, sentinel, owner, mode, physical path, mount, link, emptiness, or prior-state check differs;
- the retained or copied archive differs by path, type, owner, mode, size, or SHA-256;
- extraction exposes an undeclared member type/path or writes outside the root;
- the compiler path or SHA-256 differs;
- any source path, count, byte count, hash, mode, or manifest differs;
- an undeclared dependency, module, workspace, tool, executable, cache, credential, key, retained input, or output appears;
- the isolation profile is absent, unreviewed, fails to load, or permits an unlisted path or network operation;
- a proxy, DNS lookup, network request, connection, listener, VCS action, package-manager action, telemetry action, or user-state access is attempted;
- Go tries to update `go.mod`, create `go.sum`, acquire a toolchain/module, or read a global cache/configuration;
- a command, argument, environment value, working directory, process descendant, timeout, or invocation count differs;
- Build A exits nonzero, times out, is signaled, or lacks complete evidence;
- Build B differs from Build A's accepted command except for literal `build-b` paths;
- either binary is absent, non-regular, outside its path, or differs from the other binary;
- source changes, an output escapes the root, or postflight cannot reconcile; or
- any test, planner execution, retained-input read, verifier/key use, graph action, R3-O1 action, later gate, commit, or push is attempted.

On stop, preserve bounded evidence and the exact root owner-only, mark P3-01 `Incomplete`, and return for review. Do not rerun, broaden access, edit source, remove evidence, or infer success.

## Rollback and retention

No rollback action is currently needed because this proposal creates nothing.

After a future authorized root-resolution or build attempt, retain the exact owner-only root until user review. Cleanup requires a separate explicit instruction and must first revalidate:

- the literal root and sentinel hashes;
- UID 501 ownership and mode `0700`;
- physical-path equality, non-symlink, and non-mount status;
- complete expected inventory;
- zero matching process, open file, listener, and connection; and
- the exact rollback scope recorded in `rollback.json`.

Cleanup may remove only that literal root. It must not use a wildcard, unresolved variable, Git reset/checkout, global Go-cache cleanup, package uninstall, retained-archive deletion, repository edit, or unrelated-process termination. If any cleanup precondition fails, preserve the root and stop.

## Required specialist reviews

| Review function | Required finding before P3-01 execution approval |
|---|---|
| Security / privacy | Literal root, denied network, empty environment, read/write confinement, no user/credential/retained-data path, process controls, and fail-closed rollback are complete |
| Supply chain / maintenance | Archive, extraction, compiler, source, command, cache, and no-dependency boundaries are exact and independently hashable |
| Quality / independent verification | Two independent clean-build commands, timeouts, output identities, reproducibility comparison, evidence schemas, and stop conditions are complete |
| Orchestrator / governance | Root resolution, build execution, test authorization, P4 evidence, retained-input execution, R3-O1, commit, and push remain separate gates |

Any non-`Pass` finding or disagreement blocks P3-01 execution.

## Acceptance and root-resolution gates

This document may be approved only as a planning framework while `<P3_ROOT>` remains unresolved. Such approval would not make P3-01 executable or authorize root creation.

Before P3-01 can be marked Accepted for execution:

1. a separate instruction must authorize only root resolution and static toolchain/source preparation;
2. that work must create and validate exactly one root without invoking Go;
3. the literal root, sentinel hash, source-copy manifest hash, toolchain-extraction manifest hash, compiler hash, and isolation-profile hash must be inserted into a revised document;
4. every `<P3_ROOT>` occurrence must be replaced with the exact literal path;
5. the revised P3-01 SHA-256 must be reported separately;
6. all four specialist reviews must be `Pass` with no disagreement; and
7. the user must explicitly accept the fully literal P3-01 revision and separately authorize any Go/build action.

Only after that review may the final synthetic test authorization request be revised with the same root identity and exact accepted P3-01 hash. Preparing that final request must not execute a build or test.

## Explicit non-authorization

This Proposed package does not authorize:

- creating, reserving, probing, or validating a P3 root;
- reading, copying, extracting, installing, or executing the retained Go archive or toolchain;
- copying the accepted source tree or creating a cache, binary, sandbox profile, sentinel, or evidence file;
- invoking Go, a compiler, linker, formatter, test runner, planner, verifier, key, project executable, generator, or graph command;
- building, testing, benchmarking, fuzzing, vetting, installing, or running any source;
- changing source, fixtures, tests, manifests, `go.mod`, dependencies, `go.sum`, workspace files, authorization requests, or the planner-execution request;
- reading retained checksum responses, tiles, correspondence, accounts, credentials, keys, user configuration, or production data;
- accessing the network, DNS, cloud AI, telemetry, analytics, a package service, VCS host, database, listener, container, or production system;
- beginning P3 execution, P4, P4-E, R3-O1, Checkpoint B, stack selection, deployment, or real-data work;
- committing this proposal or any later artifact; or
- pushing.

## Review request

Review is requested on:

1. the deliberate unresolved-root boundary and staged root-resolution gate;
2. accepted source, archive, and compiler identities;
3. proposed root layout and exact command-path allowlist;
4. independent Build A/Build B environments, commands, caches, and timeouts;
5. network denial, read/write confinement, process, filesystem, and user-state isolation;
6. writable locations, expected outputs, evidence, stop, rollback, and retention controls;
7. the four specialist review conditions; and
8. the requirement that the final test request use the later accepted literal root and exact P3-01 hash.

Until a fully literal revision is separately accepted and explicitly authorized, no P3 root may be created and no Go process, build, or test may begin.
