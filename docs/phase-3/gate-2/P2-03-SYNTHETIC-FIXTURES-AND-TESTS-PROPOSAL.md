# P2-03 Synthetic Fixtures and Planner Tests Proposal

**Status:** Accepted
**Proposal date:** 2026-09-18
**Review date:** 2026-09-18
**Authority:** Accepted planning decision only; no fixture or test source creation, Go invocation, build, test, planner execution, retained-input read, dependency change, network action, generated output, implementation commit, or push is authorized
**Accepted predecessors:** P2-01 commit `01a86b3`; P2-02 commit `2eb263d`
**Governing prerequisite:** [R3-G2 planner prerequisite-resolution record](R3-G2-PLANNER-PREREQUISITE-RESOLUTION.md)
**Governing design:** [R3-G2 literal checksum-tile planner](R3-G2-LITERAL-CHECKSUM-TILE-PLANNER-PROPOSAL.md)

## Purpose

P2-03 would add only synthetic fixture definitions, planner tests, and their deterministic source manifest. It would freeze the evidence needed to review parser limits, operation closure, tile-path planning, partial/full fallback behavior, sentinel enforcement, deterministic outputs, provenance classification, and failure handling before any build or test receives execution authority.

This proposal also freezes the future build and test boundary so P2-03 source review cannot silently become P3 execution authority. Every command in this document is documentary until a later P3 authorization replaces the disposable-root notation with validated literal paths and explicitly permits execution.

## Gate separation

| Gate | Permitted decision | Remains prohibited |
|---|---|---|
| `P2-03` design | Review this fixture/test design and future command boundary | Creating fixture/test source; invoking Go; building or testing |
| `P2-03` implementation | After separate approval, create only the exact synthetic source package and manifest; stop for diff review | Invoking Go; build; test; planner execution; retained inputs |
| `P2-04` review | Seven-function static review of complete P2 source | Build; test; planner execution |
| `P3` authorization | Separately authorize exact isolated build and synthetic-test commands | Retained inputs; network; verifier; graph work |
| `P4` evidence | Review build, test, binary, provenance, licensing, and isolation evidence | Planner execution until P4-E |

No approval may collapse these gates.

## Exact future repository delta

After a separate P2-03 implementation authorization, the uncommitted diff may add exactly these eight paths:

```text
experiments/phase-3/r3-g2-tile-planner/sourcebundle_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/test_helpers_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/parse_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/plan_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/output_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/run_test.go
experiments/phase-3/r3-g2-tile-planner/testdata/synthetic/cases.json
experiments/phase-3/r3-g2-tile-planner/synthetic-test-source-manifest.tsv
```

No accepted planner-owned source, copied tlog source, license, `go.mod`, provenance manifest, README, command package, or documentation file may change during P2-03 implementation. No symlink, binary fixture, archive, lookup cache, real checksum-database response, generated golden output, or executable file may be added.

The future source manifest must resolve `UNRESOLVED_P2_TEST_SOURCE_MANIFEST_SHA256` from the accepted prerequisite record. It does not resolve any P3 or P4 evidence hash.

## Dependency boundary

The future tests may use only:

- the Go 1.27.1 standard library;
- the accepted planner-owned packages at commit `2eb263d`;
- the three accepted local copied tlog files and accepted BSD license at commit `2eb263d`; and
- the static synthetic case definitions in `testdata/synthetic/cases.json`.

The following are forbidden:

- a `require`, `replace`, `exclude`, `retract`, or `tool` directive in `go.mod`;
- `go.sum`;
- another Go module or workspace file;
- a testing framework, assertion library, generator, fuzzer dependency, golden-file package, or snapshot library;
- module, VCS, proxy, checksum-service, package-manager, or network access;
- CGO or a platform library;
- a service, database, container, listener, browser, or cloud model; and
- a real verifier key, credential, token, account identifier, correspondence item, retained lookup response, checksum tile, or production datum.

Any undeclared import or dependency blocks P2-03.

## Synthetic fixture contract

`cases.json` must be UTF-8, LF-terminated, deterministically ordered by `case_id`, and contain no timestamp, hostname, temporary path, random seed, real host, live module identity, retained response bytes, or unresolved value. Synthetic module paths must use `example.invalid`. Fixed byte sequences must be visibly labeled synthetic and non-secret.

The file must use this top-level schema:

```text
schema_version
trust_label
cases[]:
  case_id
  category
  construction
  mutation
  expected_result
  expected_stop
  requirements[]
```

Required constants:

```text
schema_version = 1
trust_label = SYNTHETIC_NON_AUTHENTICATED_TEST_DATA
```

`test_helpers_test.go` may translate those declarative cases into temporary lookup files by using only fixed in-memory synthetic bytes and local copied formatting helpers. It must not read a repository path other than `cases.json`, derive entropy, consult a clock, inspect a user home, execute a process, access a cache, open a network resource, or persist generated lookup bytes outside `t.TempDir()`.

No fixture may contain a valid production signature or assert signature validity. Structurally shaped signature envelopes must be built from fixed synthetic bytes and remain labeled non-authenticated.

## Exact synthetic case inventory

| Case ID | Category | Required behavior |
|---|---|---|
| `SYN-VALID-14` | Baseline | Exactly `L01`–`L14`, deterministic synthetic paths/hashes, valid unverified structure, and complete planning |
| `SYN-SINGLE-RECORD` | Tree shape | One-record tree behavior through the lower-level parser/planner boundary |
| `SYN-POWER-OF-TWO` | Tree shape | Power-of-two tree sizes produce canonical native tile paths |
| `SYN-PARTIAL-FALLBACK` | Tile closure | Every partial primary tile receives its deterministic width-256 fallback candidate |
| `SYN-SHARED-TILES` | Deduplication | Multiple record operations share literal paths without losing origin rows |
| `SYN-MULTI-SIZE-HEADS` | Operation closure | Distinct increasing tree sizes produce complete pairwise and record-under-later-head operations |
| `SYN-EQUAL-SAME-ROOT` | Head deduplication | Equal-size/equal-root heads deduplicate while preserving source identities |
| `SYN-EQUAL-DIFFERENT-ROOT` | Variant handling | Equal-size/different-root heads remain separate and receive the variant flag |
| `SYN-ORDER-PERMUTATIONS` | Order closure | Every ordering of a bounded three-response set maps to the same conservative operation set |
| `ERR-RECORD-NEGATIVE` | Parser failure | Negative record identifier stops |
| `ERR-RECORD-NONCANONICAL` | Parser failure | Leading-zero or otherwise noncanonical record identifier stops |
| `ERR-TREE-NONCANONICAL` | Parser failure | Noncanonical or out-of-range tree size stops |
| `ERR-UTF8` | Parser failure | Invalid UTF-8 stops without normalization |
| `ERR-BLANK-RECORD-LINE` | Parser failure | Blank line inside record text stops |
| `ERR-MISSING-TERMINATOR` | Parser failure | Missing LF terminator stops |
| `ERR-MALFORMED-ROOT-BASE64` | Parser failure | Noncanonical base64 tree root stops |
| `ERR-WRONG-ROOT-LENGTH` | Parser failure | Decoded root not exactly 32 bytes stops |
| `ERR-MALFORMED-SIGNATURE` | Parser failure | Invalid structural signature line or byte length stops without verification |
| `ERR-MISSING-INPUT` | Input boundary | Missing declared file stops |
| `ERR-DUPLICATE-ID` | Manifest boundary | Duplicate or out-of-sequence ID stops |
| `ERR-UNEXPECTED-INPUT` | Input boundary | Fifteenth or undeclared directory entry stops |
| `ERR-OVERSIZED-INPUT` | Resource boundary | Input over 1,024 bytes stops before parse |
| `ERR-SYMLINK-INPUT` | Filesystem boundary | Runtime-created temporary symlink input stops; no symlink is checked into Git |
| `ERR-PATH-TRAVERSAL` | Path boundary | Absolute, parent, non-clean, tabbed, or newline path stops |
| `SYN-LARGE-TILE-NUMBER` | Canonical path | Large tile numbers exercise canonical `xNNN/` path segmentation |
| `ERR-INPUT-CAP` | Resource boundary | Input cap exhaustion stops without truncation |
| `ERR-HEAD-CAP` | Resource boundary | Head cap exhaustion stops without truncation |
| `ERR-OPERATION-CAP` | Resource boundary | Operation cap exhaustion stops without partial promotion |
| `ERR-PATH-CAP` | Resource boundary | Literal-path cap exhaustion stops without partial promotion |
| `SYN-SENTINEL-REQUIRED` | Derivation boundary | Every successful path-planning operation ends in `MNEME_PLAN_ONLY_TILE_CAPTURE` |
| `ERR-SAVE-TILES` | Derivation boundary | Any `SaveTiles` call is a hard stop |
| `SYN-OUTPUT-DETERMINISM` | Determinism | Two fresh temporary roots produce byte-identical ten-file outputs |
| `SYN-INCOMPLETE-MARKER` | Failure promotion | A forced output-write failure retains `UNVERIFIED AND INCOMPLETE` status and no promoted pass set |
| `SYN-SOURCE-PROVENANCE` | Provenance | Embedded copied source, license, and copied manifest receive exact accepted origin/license classifications |
| `SYN-NEGATIVE-INVENTORY` | Security boundary | Keys, verification, tile-body reads, network, listeners, child processes, cache, `go.sum`, and graph actions remain zero |

Cases may share helper data, but no required case ID may be omitted, renamed, merged away, or converted into an integration test that needs an external resource.

## Test-source responsibilities

| File | Exact responsibility |
|---|---|
| `sourcebundle_test.go` | Verify deterministic embedded-source inventory and exact P2-02 provenance/license classification without writing files |
| `test_helpers_test.go` | Parse `cases.json`; create bounded temporary synthetic manifests/responses; provide fixed deterministic constructors and no-network negative helpers |
| `parse_test.go` | Cover manifest parsing, file identity, syntax, UTF-8, bounds, module/version line, tree structure, and signature-envelope structure |
| `plan_test.go` | Cover head deduplication/variants, order-complete operations, tile paths, fallbacks, caps, sentinel, and forbidden save behavior |
| `output_test.go` | Cover exact schemas, ten filenames, unique literal paths, provenance output, incomplete marker, normalization, and two-root determinism |
| `run_test.go` | Cover exact flags, cap values, positional-argument rejection, exit classes, missing inputs, nonempty output roots, and no environment/home dependence |
| `cases.json` | Declarative synthetic case inventory only |
| `synthetic-test-source-manifest.tsv` | Deterministic identity of the seven test/fixture source files; the manifest does not list itself |

No test may weaken a production cap, mutate accepted source, bypass the exact command surface, or authenticate synthetic content.

## Test-to-requirement traceability

The future implementation review must map every case and test function to:

- the structural-input contract;
- all fourteen structural-sufficiency conditions relevant before retained execution;
- every accepted safety cap;
- every planner stop condition;
- every required planner output and literal-manifest field;
- the non-verifier and zero-network boundaries;
- deterministic source/provenance classification; and
- the negative inventory.

Any requirement lacking either a test or an explicit static-review justification blocks P2-03 acceptance.

## Future build boundary

Build is not authorized by P2-03. A later P3 request may authorize only one local module build, twice from clean root-contained caches for reproducibility, using the accepted Go 1.27.1 compiler binary whose expected SHA-256 is:

```text
132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598
```

The exact future build command form is:

```text
<P3_ROOT>/toolchain/go/bin/go build -mod=readonly -trimpath -buildvcs=false -o <P3_ROOT>/build-a/mneme-r3-g2-tile-plan ./cmd/mneme-r3-g2-tile-plan
<P3_ROOT>/toolchain/go/bin/go build -mod=readonly -trimpath -buildvcs=false -o <P3_ROOT>/build-b/mneme-r3-g2-tile-plan ./cmd/mneme-r3-g2-tile-plan
```

`<P3_ROOT>` is explanatory notation only. P3 must replace it with one validated literal `mktemp` result before authorization. No install, cross-compile, race build, coverage instrumentation, fuzz binary, plugin, shared library, or product artifact is permitted.

The build may read only the accepted experiment source tree copied into the P3 root and root-contained toolchain/cache paths. It may write only the two declared binaries and root-contained compiler cache/temp files.

## Future test boundary

Test execution is not authorized by P2-03. A later P3 request may authorize exactly one command over exactly two local packages:

```text
<P3_ROOT>/toolchain/go/bin/go test -mod=readonly -count=1 -shuffle=off -timeout=60s . ./internal/planner
```

The package `.` contains only the source-bundle provenance test. `./internal/planner` contains the synthetic planner tests. No `./...`, copied-tlog package test, benchmark, fuzzing, race detector, coverage upload, vet, generate, list, module, graph, install, or second test run is permitted without a revised P3 authorization.

Tests may write only beneath Go-managed package temporary directories rooted in `<P3_ROOT>/tmp` and the root-contained build cache. They must leave the repository copy byte-identical to its accepted source manifest.

## Exact future environment

Every future Go process must use an empty environment populated only with literal root-contained values and:

```text
PATH=/usr/bin:/bin
LC_ALL=C
TZ=UTC
HOME unset
TMPDIR=<P3_ROOT>/tmp
GOROOT=<P3_ROOT>/toolchain/go
GOPATH=<P3_ROOT>/state/gopath
GOMODCACHE=<P3_ROOT>/state/gomodcache
GOCACHE=<P3_ROOT>/state/gocache
GOTMPDIR=<P3_ROOT>/state/gotmp
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

External networking must be denied independently of these variables. No proxy, credential helper, netrc, SSH agent, keychain, user Go configuration, global cache, telemetry, analytics, or update mechanism may be reachable.

## Future disposable layout

P3 must use a fresh owner-only root matching:

```text
/tmp/mneme-phase3-p3.XXXXXX
```

The proposed layout is:

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
├── state/
│   ├── gopath/
│   ├── gomodcache/
│   ├── gocache/
│   └── gotmp/
└── evidence/
    ├── source-copy-manifest.tsv
    ├── environment.json
    ├── command-ledger.tsv
    ├── build-results.tsv
    ├── test-results.tsv
    ├── binary-comparison.tsv
    ├── filesystem-inventory.tsv
    ├── isolation-preflight.json
    ├── isolation-postflight.json
    ├── rollback.json
    └── stop-register.md
```

Every directory is mode `0700`; every evidence/source file is mode `0600`; binaries may be mode `0700`. The P3 request must validate owner, sentinel, non-symlink, non-mount, path identity, process, listener, open-file, and empty-root conditions before invoking Go.

## Expected future outputs

Permitted outputs are limited to:

- two local planner binaries under `build-a/` and `build-b/`;
- root-contained Go build cache and temporary compiler files;
- temporary synthetic lookup/output trees created and removed by the test process beneath `<P3_ROOT>/tmp`;
- the ten planner output filenames only inside test temporary directories;
- plain local test process output captured by the orchestrator; and
- the exact evidence records listed above.

No repository file, `go.sum`, module payload, SBOM, license report, coverage profile, fixture update, snapshot, network response, service state, database, container, or retained-input output may be generated. SBOM and final license-report work remain P4.

## P2-03 implementation evidence requirements

Before P2-03 can be accepted as an implementation-review prerequisite, the review package must include:

1. complete eight-path diff and zero other path;
2. `synthetic-test-source-manifest.tsv` with exact sizes and SHA-256 values for the seven source/fixture files;
3. exact manifest SHA-256 resolving `UNRESOLVED_P2_TEST_SOURCE_MANIFEST_SHA256`;
4. import inventory proving standard-library and accepted local packages only;
5. test-to-requirement matrix covering every required case, cap, stop condition, output, and negative control;
6. fixture-content inventory proving only `example.invalid` identities and fixed synthetic non-secret bytes;
7. static checks proving no network, process execution, home lookup, credential, verifier key, retained response, real correspondence, or external dependency path;
8. proof that accepted production and copied-source files are unchanged from commit `2eb263d`;
9. specialist findings, disagreements, uncertainties, and rejected expansions; and
10. explicit confirmation that no Go command, build, test, or generated output occurred during P2-03 implementation.

P2-03 implementation evidence must not claim that a test passed. At this gate only source completeness and reviewability can pass.

## Future P3 execution evidence requirements

A later P3 run, if separately authorized, must record:

- exact compiler binary identity and accepted SHA-256;
- complete sanitized environment and command ledger;
- source-copy identity against the accepted P2 manifest;
- offline/cache-empty preflight and postflight;
- both build exit results, binary hashes, byte comparison, and reproducibility finding;
- exact test command, package list, exit result, case/function counts, and failures;
- proof that repository source did not change;
- zero network request/listener, external module, `go.sum`, credential, key, verifier, retained-input, service, child-process-except-Go-toolchain, and graph-action counts;
- complete root inventory, stop register, and rollback state; and
- security/privacy, supply-chain, quality, licensing, architecture, preservation, and orchestrator reviews.

Those are future evidence requirements, not authority to produce them now.

## Isolation and hostile-fixture controls

- Every fixture size is bounded before parsing.
- Runtime-created files remain beneath `t.TempDir()` and use literal relative names.
- Symlink and traversal cases must fail before opening an escaped target.
- Tests must not print fixture bodies, environment values, absolute user paths, or source bytes on success.
- Failure messages may contain only case IDs and normalized relative paths.
- Fixed malformed data is treated as hostile input and never interpreted as a command, path authorization, HTML, credential, or instruction.
- No fixture may cause shell, process, plugin, dynamic-library, template, browser, or network interpretation.
- Output-write failure tests use a temporary root and do not alter repository permissions.
- Test cleanup is limited to Go-owned temporary directories; no broad recursive path or cache purge is permitted.

## Stop conditions

P2-03 preparation or later implementation must stop if:

- an implementation path outside the exact eight appears;
- accepted P2-01 or P2-02 content changes;
- a fixture resembles or contains a retained/live response, real module identity, correspondence item, credential, key, or checksum tile;
- an import is not standard-library or accepted local source;
- `go.mod`, `go.sum`, a workspace, dependency, generated file, symlink, binary, or executable fixture appears;
- a required case, requirement mapping, cap, stop condition, output schema, or negative control is missing;
- a test depends on time, randomness, host state, user configuration, global cache, external process, service, or network;
- a command invokes Go, build, test, planner, verifier, graph, or generator before P3 approval;
- a test command or environment differs from the frozen future boundary without revised review; or
- evidence, isolation, rollback, or specialist review is incomplete.

A stop preserves only bounded uncommitted source/evidence, labels P2-03 `Incomplete`, and returns for review without retry or scope expansion.

## Rollback

Before P2-03 acceptance, rollback may remove only the exact eight uncommitted P2-03 paths under a separately approved cleanup instruction after validating their identities. It must not alter accepted P2-01/P2-02 files, the owner-only P2-02 evidence root, the retained Go archive, or the Proposed planner-execution request.

Future P3 rollback must validate the exact expanded P3 root, owner, mode, sentinel, realpath/path-identity evidence, non-symlink, non-mount, process, listener, open-file, and inventory state before removing only that disposable root. No Git reset, checkout, wildcard deletion, global Go-cache cleanup, package uninstall, or unrelated-process termination is permitted.

## Specialist reviews required

| Review function | Required P2-03 finding |
|---|---|
| Security / privacy | Fixtures are wholly synthetic and bounded; path, symlink, hostile-byte, no-network, no-key, no-home, and no-process controls fail closed |
| Quality / independent verification | Every requirement, cap, output, stop condition, sentinel path, fallback rule, failure mode, and determinism claim has a precise test or static justification |
| Supply chain / maintenance | No dependency or tool is added; commands use only the accepted compiler, standard library, and local reviewed source |
| Preservation / provenance | Accepted P2 source stays byte-identical; fixture/test source and future outputs have complete manifests |
| Architecture / portability | Tests remain experimental evidence tooling and introduce no product-runtime or stack-selection commitment |
| Licensing / cost | Tests add no licensed dependency, account, service, hosted resource, or cost; copied x/mod licensing remains unchanged |
| Orchestrator / governance | P2 source review, P3 execution, P4 evidence, and P4-E retained-input execution remain separate |

Any unresolved disagreement blocks P2-03 acceptance.

## Acceptance condition

This design package may be accepted as a planning decision without authorizing source creation. P2-03 itself becomes an accepted implementation-review prerequisite only after the separately authorized eight-path source package is complete, its manifest hash is recorded, all specialist findings pass, and the user approves the exact diff.

Even then, no build or test may run until a separate P3 authorization freezes literal root paths, toolchain identity, commands, environment, timeouts, outputs, isolation checks, and rollback.

## Explicit non-authorization

This Accepted planning document does not authorize:

- creating a fixture, test file, source manifest, disposable root, toolchain copy, cache, binary, or evidence output;
- invoking Go or another compiler, linker, formatter, test runner, verifier, key, project executable, or graph command;
- adding or changing a dependency, `go.mod`, `go.sum`, workspace, lockfile, package, service, listener, database, container, or network rule;
- reading retained lookup responses, tiles, correspondence, accounts, credentials, user configuration, or production data;
- executing the planner or copied tlog source;
- accessing the network, cloud AI, telemetry, analytics, or hosted services;
- beginning P2-04, P3, P4, P4-E, R3-O1, Checkpoint B, deployment, stack selection, or production work;
- committing this proposal, P2-03 source, generated evidence, or the still-Proposed planner-execution request; or
- pushing.

## Accepted planning decision

The review accepted the exact eight-path implementation boundary, 35-case synthetic inventory, source responsibilities, dependency restrictions, future build/test commands and environment, allowed outputs, isolation, rollback, P2/P3/P4 gate separation, evidence requirements, specialist reviews, stop conditions, and explicit non-authorization as the P2-03 planning framework.

P2-03 implementation remains unresolved. Until separate fixture-generation and test-run requests are independently reviewed and explicitly approved at their proper gates, no P2-03 fixture, test, build, or execution work may begin.
