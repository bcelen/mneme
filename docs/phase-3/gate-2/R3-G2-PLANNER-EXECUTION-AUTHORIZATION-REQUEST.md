# R3-G2 Planner Execution Authorization Request

**Status:** Proposed
**Request date:** 2026-09-18
**Review date:** Pending
**Execution readiness:** Not ready; P2 implementation review, P3 synthetic build/test authorization, and P4 build/test evidence acceptance remain unsatisfied
**Current authority:** Review only. No retained-input read, planner implementation, build, test, execution, network action, verifier action, acquisition, graph work, or later-stage action is authorized
**Governing design:** [Accepted R3-G2 literal checksum-tile planner](R3-G2-LITERAL-CHECKSUM-TILE-PLANNER-PROPOSAL.md)

## Decision requested

After all named prerequisites are satisfied and every unresolved value in this request is replaced by accepted evidence, authorize exactly two deterministic offline executions of one accepted planner binary over two independently copied sets of the same fourteen retained R3-G2 lookup responses.

The proposed executions would:

1. validate exact retained-input identity without modifying the accepted R3-G2 root;
2. perform structural parsing only, with no signature or Merkle verification;
3. prove whether the retained responses are structurally sufficient for order-complete tile-path derivation;
4. produce two independently generated literal tile manifests;
5. compare all deterministic outputs byte-for-byte; and
6. stop for review before any network request, tile acquisition, native verifier, `go list`, `go mod graph`, or `go.sum` action.

This request is not currently executable. The planner source, synthetic tests, build evidence, binary path, binary SHA-256, and source-manifest SHA-256 do not yet exist as accepted artifacts. Approval of this document as planning would not fill those gaps or authorize execution.

## Prerequisite gates

The accepted planner design defines gates P1–P6. Current state:

| Gate | State | Required before retained-input execution |
|---|---|---|
| `P1` Planner design | Accepted 2026-09-18 | Complete |
| `P2` Implementation diff | Not prepared | Exact planner source, copied tlog files, license, local module, synthetic fixtures, and tests reviewed |
| `P3` Synthetic build/test | Not authorized | Exact offline build and synthetic test commands authorized |
| `P4` Build/test evidence | Not available | Binary identity, source manifest, SBOM/license report, test results, no-network evidence, and specialist reviews accepted |
| `P4-E` Retained execution | This proposed request | May be considered only after P2–P4 are complete and this request contains no unresolved value |

No instruction may collapse P2, P3, P4, and P4-E into one implicit approval. If this document is accepted before the prerequisites are complete, its status may become `Accepted as an execution framework`, but execution authority remains closed until a later explicit authorization cites the completed artifact hashes and exact binary.

## Exact retained inputs

The source root is the accepted owner-only R3-G2 root:

```text
/tmp/mneme-phase3-r3-g2.l4nJHn
```

Only the following fourteen regular files may be read after explicit retained-execution authorization. The table is transcribed from accepted R3-G2 evidence; this request does not reread the files.

| ID | Exact path relative to source root | Bytes | SHA-256 |
|---:|---|---:|---|
| `L01` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/jackc/pgx/v5@v5.11.0` | 365 | `12bfc2f97e5de2475b60d648f0dfead1a512b1833e68b4d3a376b4de4c1b343a` |
| `L02` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/jackc/pgpassfile@v1.0.0` | 368 | `777d62110cc679e85cf8360b3bd8737a0a541197510346e3347b0564b508fcd4` |
| `L03` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/jackc/pgservicefile@v0.0.0-20240606120523-5a60cdf6a761` | 433 | `a11e72b1d82e0325dbf45e51392f7620a97de551c563fec7fcd42f4c7ae5a4c4` |
| `L04` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/jackc/puddle/v2@v2.2.2` | 369 | `0bf8624e3d652ae989d1379ecbe99877fa36d11f5684141ea5795cdd31f380bd` |
| `L05` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/golang.org/x/sync@v0.17.0` | 353 | `4211b7912629a3704824366185427fc9427178a8d87691ffcb9e7effbf9b3de0` |
| `L06` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/golang.org/x/text@v0.29.0` | 353 | `d3a1044f6b6a2c48d0c44c7a52b0cd8e559e5d01749c041adf78a774d0f71b9a` |
| `L07` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/stretchr/testify@v1.11.1` | 373 | `0fa45b4eb123f847f0a687dbaef2151a72d93bc4d957b08bf8808ffb24bd57a6` |
| `L08` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/davecgh/go-spew@v1.1.1` | 364 | `00c7d7d34e97836f4c466fb58ab6fffde752abca5990e97d4986d731c331fc47` |
| `L09` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/kr/pretty@v0.3.0` | 356 | `95084f042ed8b704ddd6457ddfae3fa3859ea787c7ea686108504dc4d8cb6d4c` |
| `L10` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/github.com/pmezard/go-difflib@v1.0.0` | 370 | `e8b74b212142f28a7dc1df9cf10b141b2938ada83a377409a49f6cedf552fbcf` |
| `L11` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/gopkg.in/check.v1@v1.0.0-20201130134442-10cb98267c6c` | 406 | `f1cea5b5a51a08a48a680b2a2a4f4c077ff30556915af8331b7c21c4bf881b79` |
| `L12` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/gopkg.in/yaml.v3@v3.0.1` | 349 | `165cefbf5d9b5ee1c7176e6ce631bca875caf5e247fc8c39cc44c33160f064d1` |
| `L13` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/golang.org/x/tools@v0.36.0` | 355 | `531c502b98e62475e5c7689e56683ad906612122aaf9644393a7a1d49837f60c` |
| `L14` | `state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/golang.org/x/mod@v0.27.0` | 351 | `bf4b897f725f8fc0854ece39588058cdb667696445f906d58e9b8abd5269396b` |

The complete input payload is exactly 5,165 bytes. No recursive directory read is authorized. Every source path is opened individually only after realpath, root containment, owner, mode, regular-file, non-symlink, size, and SHA-256 checks pass.

Each future destination filename is fixed as `lookups/<ID>.lookup`, where `<ID>` is the literal `L01`–`L14` value in the table. Each `lookup-inputs.tsv` has this exact field order:

```text
input_id
source_relative_path
destination_relative_path
bytes
sha256
```

Rows are ordered `L01` through `L14`, use LF endings, and contain no absolute path, timestamp, or unresolved field.

The following accepted evidence records may be read only for preflight reconciliation, not as planner payload:

| Evidence record | Expected identity |
|---|---|
| `evidence/metadata-inventory.tsv` | 7,211 bytes; SHA-256 `f474dbc5fe97266a74f32f138af583aea9175b396f95862284a1f1e96926ff20` |
| `evidence/literal-request-results.tsv` | 9,886 bytes; SHA-256 `f042983b6a1b9546e7c7e4290c2b4916a82d586fd5c75875ac4cd634f3fb06ce` |
| `evidence/request-ledger.tsv` | 4,667 bytes; SHA-256 `280dce056710cbd7b521ce9853393a28cd24fb3c1717603ba99fcfedd7006731` |
| `evidence/workspace-checksums.sha256` | 106 lines; SHA-256 `d142dcea343eef409fba750c8ef425b703dceb685d39c876b297040d2353bf8b` |
| `evidence/cache-inventory.tsv` | 108 lines; SHA-256 `b1032a2c4aa1e00bd836544d9bcf8c7e4180446e21a44f4c2d79467bd0fb29c2` |

No other path under either retained root may be read. In particular, the future execution excludes `.info`, `.mod`, toolchain, Go cache, checksum tiles, keys, credentials, source payloads, and correspondence.

## Required accepted planner artifacts

Before this request can become executable, P4 evidence must freeze all of the following:

| Artifact | Required accepted value |
|---|---|
| Planner repository path | `experiments/phase-3/r3-g2-tile-planner/` |
| Planner binary name | `mneme-r3-g2-tile-plan` |
| Planner binary SHA-256 | `UNRESOLVED_P4_BINARY_SHA256` |
| Planner source-manifest SHA-256 | `UNRESOLVED_P4_SOURCE_MANIFEST_SHA256` |
| Synthetic-test report SHA-256 | `UNRESOLVED_P4_TEST_REPORT_SHA256` |
| SBOM SHA-256 | `UNRESOLVED_P4_SBOM_SHA256` |
| License-report SHA-256 | `UNRESOLVED_P4_LICENSE_REPORT_SHA256` |
| No-network evidence SHA-256 | `UNRESOLVED_P4_NETWORK_EVIDENCE_SHA256` |

Every `UNRESOLVED_*` value is a hard execution blocker. A later revision must replace it with accepted evidence; runtime substitution, environment expansion, or user inference is forbidden.

## Disposable execution roots

After authorization, create exactly one owner-only parent root using the template:

```text
/tmp/mneme-phase3-r3-g2-planner.XXXXXX
```

The validated expanded path is `<root>`. It must be owned by UID 501, mode `0700`, a non-symlink, not a mount point, and contain a matching `MNEME_PHASE3_DISPOSABLE.json` sentinel before retained inputs are read.

Required layout:

```text
<root>/
├── MNEME_PHASE3_DISPOSABLE.json
├── bin/
│   └── mneme-r3-g2-tile-plan
├── inputs-a/
│   ├── lookup-inputs.tsv
│   └── lookups/
├── inputs-b/
│   ├── lookup-inputs.tsv
│   └── lookups/
├── outputs/
│   ├── run-a/
│   └── run-b/
└── evidence/
    ├── command-transcript.jsonl
    ├── determinism-checks.sha256
    ├── environment.json
    ├── execution-summary.md
    ├── input-copy-manifest.tsv
    ├── isolation-preflight.json
    ├── isolation-postflight.json
    ├── planner-artifact-manifest.tsv
    ├── rollback.json
    ├── stop-register.md
    └── workspace-checksums.sha256
```

Every directory is mode `0700`; every file is mode `0600`; the binary may be mode `0700`. `inputs-a` and `inputs-b` are independent byte copies made directly from the accepted source files, not copies of each other.

## Exact planner outputs

Each of `outputs/run-a/` and `outputs/run-b/` must contain exactly:

```text
planner-inputs.tsv
response-structure.jsonl
tree-heads.tsv
operation-matrix.tsv
tile-origins.tsv
literal-tile-manifest.tsv
structural-sufficiency.json
planner-source-manifest.tsv
negative-inventory.json
stop-register.md
```

No other planner-created file is permitted. In particular, neither output may contain a key, tile body, network response, cache entry, Go environment file, `go.sum`, module payload, binary, database, or correspondence content.

The deterministic comparison covers all ten output files. If `stop-register.md` contains run-specific timestamps or paths, the planner design must be revised before execution; deterministic output exceptions are not permitted by this request.

## Exact command boundary

This section freezes command forms but does not authorize running them. The later P4 revision must replace `<root>` and every unresolved artifact hash with accepted literal values before execution.

### Permitted system commands

Only these system utilities may be invoked for root creation, identity checks, copying, permissions, inventory, hashing, comparison, and postflight:

```text
/usr/bin/mktemp
/usr/bin/id
/usr/bin/stat
/usr/bin/realpath
/usr/bin/find
/usr/bin/shasum
/usr/bin/wc
/usr/bin/cmp
/usr/bin/diff
/usr/bin/env
/usr/bin/pgrep
/bin/cp
/bin/chmod
/bin/ls
/bin/mkdir
/bin/ps
/sbin/mount
/usr/sbin/lsof
/usr/sbin/netstat
```

No shell profile, package manager, Git command, network client, compiler, linker, test runner, service manager, container tool, or Go command is part of planner execution.

### Planner identity command

Before either run:

```text
/usr/bin/shasum -a 256 <root>/bin/mneme-r3-g2-tile-plan
```

The result must exactly equal the later accepted P4 binary hash.

### Planner executions

Run A:

```text
/usr/bin/env -i PATH=/usr/bin:/bin TMPDIR=<root>/tmp-a LC_ALL=C TZ=UTC <root>/bin/mneme-r3-g2-tile-plan --mode plan --input-manifest <root>/inputs-a/lookup-inputs.tsv --input-root <root>/inputs-a/lookups --tile-height 8 --max-inputs 14 --max-heads 14 --max-operations 400 --max-literal-paths 4096 --output-root <root>/outputs/run-a
```

Run B:

```text
/usr/bin/env -i PATH=/usr/bin:/bin TMPDIR=<root>/tmp-b LC_ALL=C TZ=UTC <root>/bin/mneme-r3-g2-tile-plan --mode plan --input-manifest <root>/inputs-b/lookup-inputs.tsv --input-root <root>/inputs-b/lookups --tile-height 8 --max-inputs 14 --max-heads 14 --max-operations 400 --max-literal-paths 4096 --output-root <root>/outputs/run-b
```

`<root>/tmp-a` and `<root>/tmp-b` must exist as empty owner-only directories before execution. `HOME` is unset; the planner must not query or derive a user home directory. No proxy, Go, authentication, key, or other locale variable is inherited. If the accepted binary requires another environment variable, this request must be revised and reviewed.

Each planner command executes exactly once with an orchestration timeout of 60,000 milliseconds. A nonzero exit, signal, timeout, extra process, or missing output stops the workstream; neither command is retried.

### Determinism comparison

For each exact output filename, compare Run A and Run B with:

```text
/usr/bin/cmp -s <root>/outputs/run-a/<filename> <root>/outputs/run-b/<filename>
/usr/bin/shasum -a 256 <root>/outputs/run-a/<filename> <root>/outputs/run-b/<filename>
```

The complete command ledger must expand `<filename>` to the ten exact output names before authorization. A directory-wide wildcard or recursive comparison is not permitted.

## Input-copy controls

Input copying is part of the future authorized execution, not a current action. For every `L01`–`L14` row and for each of `inputs-a` and `inputs-b`:

1. resolve the literal source path and prove containment under the exact accepted source root;
2. reject a symlink, hard-link anomaly, non-regular file, owner mismatch, mode mismatch, size mismatch, or hash mismatch;
3. copy the file once to a normalized planner-owned relative path determined by `lookup-inputs.tsv`;
4. write the destination as `lookups/<ID>.lookup` and set mode `0600`;
5. independently recheck destination size and SHA-256; and
6. record source and destination identities in `input-copy-manifest.tsv`.

The two destination sets must be copied independently from the retained source. No source file is opened for writing. No metadata or content is normalized.

## Isolation preflight

Before reading any retained input, evidence must establish:

- repository state is clean at a recorded commit;
- no prior matching planner root, process, open file, or listener exists;
- the expanded root passes owner, mode, realpath, sentinel, non-symlink, and non-mount checks;
- the accepted binary and all P4 artifacts match accepted hashes;
- all output and temporary directories are empty and owner-only;
- external network access is denied for the planner process;
- proxy variables, `GOENV`, `GOPROXY`, `GOSUMDB`, `GONOSUMDB`, `GONOPROXY`, `GOPRIVATE`, `GOAUTH`, `GOVCS`, credential variables, and user configuration paths are absent from the planner environment;
- `HOME` is absent and the planner has no user-home lookup path;
- no verifier key or checksum tile exists in the root;
- the planner binary has no undeclared dynamic dependency or network capability according to accepted P4 evidence; and
- no system or user Go command, cache, config, or package-manager state is reachable through the command environment.

If external network denial cannot be proved before the first retained-input read, stop without copying an input.

## Structural sufficiency checks

The planner may emit `Structurally sufficient for literal tile planning` only when both runs independently establish all of the following:

1. exactly fourteen declared inputs and no other input file;
2. exact accepted path, byte count, and SHA-256 for every input;
3. one unambiguous record body and signed-note envelope per response;
4. one exact expected module/version `/go.mod h1:` line per response;
5. canonical signed-64-bit record IDs and tree sizes with `0 <= recordID < ownTreeSize`;
6. 32-byte decoded tree roots and structurally preserved signature envelopes, without signature verification;
7. complete distinct-head inventory, including equal-size/different-root variants;
8. an order-complete matrix for every possible retained-head merge and every possible record-check head;
9. derivation through the exact accepted tile-planning source at tile height 8;
10. `MNEME_PLAN_ONLY_TILE_CAPTURE` as the required result of every derivation;
11. zero `SaveTiles`, tile reads, hash-authentication results, keys, verifier operations, network actions, child processes, or listeners;
12. one literal primary path for every planned tile and one deterministic full fallback candidate for every partial tile;
13. no wildcard, regex, range, unresolved path, noncanonical path, data-tile path, duplicate manifest row, or output beyond the approved caps;
14. exact output schema and no extra output file; and
15. byte-identical Run A and Run B outputs for all ten deterministic files.

The result remains a structural planning conclusion. It does not authenticate a note, tree, record, module hash, or tile.

## Previously unknown path control

The planner is required to expose paths not known before planning. A newly derived path is not an anomaly merely because it was previously unknown; it becomes a reviewable manifest row only if it is produced by the exact operation matrix and canonical tlog algorithm.

Completeness is established by:

- using every retained response rather than a sample;
- preserving every distinct unverified tree head;
- considering every pairwise head consistency relationship;
- considering every record under its own head and every possible later current head;
- recording the full tile set requested by the accepted `TileHashReader` planning algorithm before returning the planning sentinel; and
- adding the deterministic full-width counterpart of every partial tile.

Any path observed later during native verification that is absent from the accepted literal manifest is proof that planning was incomplete. The verifier must stop; the path is not automatically added or acquired.

## Failure conditions

Stop without retry, repair, substitution, or output promotion if:

- a P2–P4 prerequisite or accepted hash is absent;
- repository or root isolation preflight fails;
- a source or destination input differs by path, type, owner, mode, size, or hash;
- a fifteenth input, undeclared file, symlink, mount, hard-link anomaly, open file, or prior process appears;
- retained input parsing is malformed, ambiguous, noncanonical, oversized, or requires normalization;
- a required module/version line, record ID, tree size, tree root, or signature envelope is absent;
- order-complete operation coverage cannot be proved;
- copied tile-planning source or planner binary differs from accepted P4 evidence;
- the planner reads or requests a key, tile, network path, cache, credential, user configuration, or undeclared dependency;
- a derivation does not return `MNEME_PLAN_ONLY_TILE_CAPTURE`;
- the planner invokes `SaveTiles`, returns an authentication result, creates a child process, or opens a listener;
- any output path, schema, count, cap, or filename deviates;
- a data-tile path, wildcard, regex, range, duplicate, unresolved value, or noncanonical path appears;
- Run A or Run B exits nonzero, times out, or receives a signal;
- any of the ten deterministic outputs differs between runs;
- external network denial or postflight closure cannot be proved; or
- any verifier, Go command, graph command, `go.sum`, R3-O1, acquisition, or later-stage action is attempted.

On failure, do not run the other planner invocation if it has not started. Preserve bounded evidence, mark structural sufficiency `Incomplete`, and return for review.

## Postflight and evidence requirements

Before stopping for review, record:

1. repository commit and clean-state evidence;
2. disposable-root sentinel, realpath, owner, mode, mount, process, and open-file evidence;
3. accepted planner artifact hashes and binary identity;
4. exact source and destination input manifests for both copies;
5. complete sanitized command and environment records;
6. zero-network and zero-listener preflight/postflight evidence;
7. both complete output trees with sizes, modes, and hashes;
8. per-output byte comparison and determinism result;
9. structural-sufficiency result and every individual check;
10. counts of inputs, heads, operations, origins, primary paths, fallback candidates, and unique paths;
11. explicit zero counts for keys, verifier calls, signature checks, tile reads, `SaveTiles`, authentication results, child processes, network actions, Go commands, caches, `go.sum`, module payloads, and graph actions;
12. complete anomaly, uncertainty, disagreement, and stop registers;
13. workspace checksum inventory; and
14. rollback and retention state.

Raw retained lookup bytes and planner output remain outside Git under the owner-only disposable root. Only a separately reviewed normalized documentation summary may later be proposed for the repository.

## Rollback and retention

The accepted R3-G1 and R3-G2 roots remain untouched. The planner root is retained owner-only after either success or stop until the user reviews the evidence.

On interruption or failure:

1. terminate only a process whose executable, PID, and working directory match the recorded planner root;
2. confirm external network denial and zero listener;
3. mark all outputs `UNVERIFIED` and `INCOMPLETE` in the evidence summary;
4. inventory every remaining path and open file;
5. do not rerun, repair, broaden a cap, change an input, replace the binary, or promote a manifest; and
6. wait for explicit user direction.

Any later cleanup must validate the exact root, UID, mode, realpath, sentinel, non-symlink, non-mount, process/open-file state, and complete inventory before removing only that root. No broad recursive target, wildcard deletion, Go-cache cleanup, package uninstall, Git reset, or unrelated process termination is permitted.

## Specialist authorization findings required

Before retained-input execution can be authorized, all seven reviews must find:

| Review function | Required finding |
|---|---|
| Preservation / provenance | Exact retained inputs, independent copies, byte identity, immutable source handling, and output provenance are complete |
| Security / privacy | Hostile-input limits, owner-only roots, no-network isolation, no key/verifier path, no child process, and rollback fail closed |
| Supply chain / maintenance | Exact source, binary, compiler, SBOM, dependencies, hashes, and build evidence are accepted |
| Licensing / cost | Copied BSD license obligations are satisfied; no account, service, or cost is introduced |
| Quality / independent verification | Synthetic tests, operation closure, caps, sentinel behavior, two-run determinism, and schemas are adequate |
| Architecture / portability | Planner remains experimental evidence tooling and does not select a product stack or production dependency |
| Orchestrator / governance | P2–P4 and this execution gate are complete and no acquisition, verifier, graph, or later-stage authority leaks through |

Any disagreement remains explicit and blocks execution.

## Explicit non-authorization

This proposed request does not authorize:

- reading or copying a retained lookup response or evidence record;
- creating the disposable planner root;
- implementing, copying source into, building, testing, installing, or executing the planner;
- resolving an `UNRESOLVED_*` value without accepted P4 evidence;
- invoking Go, a verifier, a verifier key, `sumdb.Client`, Ed25519, Merkle verification, or hash authentication;
- making a network request, retrying a lookup, changing the allowlist, or acquiring a tile;
- starting a service, listener, database, container, or local proxy;
- creating `go.sum` or running `go list`, `go mod graph`, another graph command, build, test, or project code;
- reading `.info`, `.mod`, ZIP, ZIP hash, module source, correspondence, account, credential, user configuration, or unrelated cache data;
- beginning R3-O1, R4, Checkpoint B, a prototype, deployment, cloud AI, real-data work, or stack selection;
- committing this request or any implementation, evidence, output, or generated artifact; or
- pushing.

## Required explicit authorization

Planner execution may occur only after P2–P4 are complete, this request has been revised to replace every unresolved value, all seven specialist findings are accepted, and the user gives an instruction substantively equivalent to:

> I authorize the R3-G2 planner execution only under the accepted, fully resolved `R3-G2-PLANNER-EXECUTION-AUTHORIZATION-REQUEST.md`: read exactly the fourteen retained lookup files, make two independent owner-only copies, execute the exact accepted planner binary once against each copy with external networking denied, compare the ten exact output files, and stop for review. No verifier, key, network request, tile acquisition, lookup retry, Go command, graph action, `go.sum`, R3-O1, or later-stage action is authorized.

General approval of the planner design, acceptance of this request as a framework, or an instruction to continue is insufficient.

## Review request

Review is requested on:

1. the fourteen exact retained inputs and five preflight evidence records;
2. the unresolved P2–P4 prerequisites that keep this request non-executable;
3. the exact disposable layout, ten output files, command forms, environment, and two-run determinism requirement;
4. the isolation, input-copy, structural-sufficiency, and previously unknown path controls;
5. failure, postflight, rollback, retention, and evidence requirements; and
6. the explicit boundary that planner execution must receive a later, fully resolved approval.

Until those prerequisites are completed and a later explicit authorization is given, the planner remains unimplemented and unexecuted, the retained inputs remain unread by it, R3-G2 remains `Incomplete`, and all acquisition, verifier, graph, R3-O1, and later-stage paths remain closed.
