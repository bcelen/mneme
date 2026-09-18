# P2-03 Synthetic Fixture and Test-Source Generation Authorization Request

**Status:** Accepted
**Request date:** 2026-09-18
**Review date:** 2026-09-18
**Execution readiness:** Authorized only for the exact static source-generation procedure and repository boundary in this document
**Current authority:** Create the exact seven synthetic fixture/test-source files and one deterministic source manifest, perform static evidence review, and stop; no Go invocation, build, test, retained-input read, dependency, network action, implementation commit, or push is authorized
**Accepted planning decision:** [P2-03 synthetic fixtures and planner tests](P2-03-SYNTHETIC-FIXTURES-AND-TESTS-PROPOSAL.md), commit `19b9bc54092d024e2010040c1f4a9c3729ae3268`
**Accepted implementation baseline:** P2-02 commit `2eb263dfbea3fd891c93d20fbca53f586489608c`

## Accepted decision

The review authorizes one static source-authoring workstream that creates exactly seven synthetic fixture/test-source files and one deterministic source manifest, then stops for complete diff and specialist review.

The workstream would not invoke Go, compile or execute the test source, generate runtime lookup files, execute the planner, or claim that any test passes. It would close only the source-preparation portion of P2-03.

## Exact repository boundary

The future uncommitted diff may add exactly these eight paths:

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

The first seven paths are source/fixture inputs. The eighth is their review manifest and must not list itself. Every accepted path at commit `2eb263d`, including `go.mod`, planner logic, copied tlog source, licenses, and provenance manifests, must remain byte-identical.

No other path may be created, modified, renamed, deleted, staged, or committed under this request.

## Exact source responsibilities

| Path | Required responsibility |
|---|---|
| `sourcebundle_test.go` | Static tests for deterministic embedded-source rows and exact P2-02 origin/license classifications |
| `internal/planner/test_helpers_test.go` | Fixed synthetic constructors, bounded `cases.json` loader, temporary manifest/lookup writer, and no-network/no-process helpers |
| `internal/planner/parse_test.go` | Structural parser, input identity, manifest, hostile-byte, path, size, and envelope cases |
| `internal/planner/plan_test.go` | Head, operation, tile, fallback, cap, sentinel, and forbidden-save cases |
| `internal/planner/output_test.go` | Exact output schemas/names, literal-path uniqueness, incomplete marker, normalization, provenance, and determinism cases |
| `internal/planner/run_test.go` | Exact flags, fixed caps, exit classes, environment independence, input/output-root failure cases |
| `testdata/synthetic/cases.json` | Declarative definitions for the accepted 35 synthetic case IDs only |
| `synthetic-test-source-manifest.tsv` | Deterministic identity of the seven preceding files |

No source file may contain a test that requires a network, external process, service, user home, credential, verifier key, real checksum response, checksum tile, account, correspondence item, or production datum.

## Exact fixture identity boundary

`cases.json` must contain exactly the 35 case IDs accepted in the planning decision:

```text
SYN-VALID-14
SYN-SINGLE-RECORD
SYN-POWER-OF-TWO
SYN-PARTIAL-FALLBACK
SYN-SHARED-TILES
SYN-MULTI-SIZE-HEADS
SYN-EQUAL-SAME-ROOT
SYN-EQUAL-DIFFERENT-ROOT
SYN-ORDER-PERMUTATIONS
ERR-RECORD-NEGATIVE
ERR-RECORD-NONCANONICAL
ERR-TREE-NONCANONICAL
ERR-UTF8
ERR-BLANK-RECORD-LINE
ERR-MISSING-TERMINATOR
ERR-MALFORMED-ROOT-BASE64
ERR-WRONG-ROOT-LENGTH
ERR-MALFORMED-SIGNATURE
ERR-MISSING-INPUT
ERR-DUPLICATE-ID
ERR-UNEXPECTED-INPUT
ERR-OVERSIZED-INPUT
ERR-SYMLINK-INPUT
ERR-PATH-TRAVERSAL
SYN-LARGE-TILE-NUMBER
ERR-INPUT-CAP
ERR-HEAD-CAP
ERR-OPERATION-CAP
ERR-PATH-CAP
SYN-SENTINEL-REQUIRED
ERR-SAVE-TILES
SYN-OUTPUT-DETERMINISM
SYN-INCOMPLETE-MARKER
SYN-SOURCE-PROVENANCE
SYN-NEGATIVE-INVENTORY
```

They must be ordered by raw UTF-8 `case_id`. The top-level values must be:

```text
schema_version = 1
trust_label = SYNTHETIC_NON_AUTHENTICATED_TEST_DATA
```

Synthetic module identities must use `example.invalid`. Fixed root, signature-shaped, and record bytes must be generated from visibly synthetic constants. They must not be copied or derived from a live checksum service, retained lookup, real module response, credential, or key.

The JSON fixture defines source parameters only. Runtime lookup files and symlinks may be constructed later inside `t.TempDir()` by separately authorized tests; they must not be checked into Git.

## Dependency and import boundary

The seven source files may import only:

- Go standard-library packages; and
- the accepted local module packages already present at commit `2eb263d`.

No external import path, new module directive, `go.sum`, workspace, generator directive, build tag, CGO declaration, dynamic import, plugin, testing framework, assertion library, fuzzing package, or snapshot library is permitted.

Test source may reference copied local tlog APIs only through the accepted local module path. It may not modify or wrap copied bytes in another package.

## Exact source-manifest contract

`synthetic-test-source-manifest.tsv` must have exactly this header:

```text
path	bytes	sha256	owner	p2_item	review_role
```

It must contain exactly seven rows ordered by raw UTF-8 path. Required fixed values are:

```text
owner = planner-test-owned
p2_item = P2-03
```

Each `review_role` must equal the corresponding responsibility in this request using one normalized hyphenated identifier. Byte counts and lowercase SHA-256 values must be independently calculated after the seven files are complete.

The complete manifest SHA-256 resolves `UNRESOLVED_P2_TEST_SOURCE_MANIFEST_SHA256` only after user acceptance. It must be reported separately rather than inserted into the manifest itself.

## Authorized source-generation procedure if approved

1. Record the current commit and confirm the only unrelated working-tree item is the unchanged Proposed planner-execution request.
2. Verify every accepted experiment path against commit `2eb263d`.
3. Create only the seven literal source/fixture paths using the reviewed patch mechanism.
4. Perform static, non-executing review of imports, fixture identities, case coverage, forbidden capabilities, path literals, and deterministic ordering.
5. Calculate each source file's byte count and SHA-256 using system file utilities only.
6. Create the exact seven-row source manifest using the reviewed patch mechanism.
7. Reconcile the manifest against all seven files and calculate its SHA-256.
8. Verify the complete Git diff contains exactly the eight authorized paths, run whitespace/status checks, and stop for review.

No formatter, generator, compiler, Go command, test runner, script, project executable, fixture builder, package manager, or network tool may run. Static source authoring must not create a temporary runtime fixture or output tree.

## Static evidence requirements

The review package must provide:

1. complete eight-path diff and line counts;
2. exact source-manifest bytes and SHA-256;
3. independent byte-count/hash reconciliation for all seven rows;
4. import inventory grouped into standard-library and accepted local paths;
5. exact 35-case inventory and zero missing/extra/duplicate case IDs;
6. test-to-requirement matrix covering every accepted requirement, cap, output, stop condition, and negative control;
7. forbidden-capability scan covering network, process execution, user home, credential, verifier/key, retained-input, real correspondence, external service, dependency, and `go.sum` paths;
8. baseline comparison proving all accepted production/copied-source files are unchanged from `2eb263d`;
9. specialist findings, disagreements, uncertainties, and rejected expansions; and
10. explicit zero counts for Go invocations, builds, tests, planner executions, generated runtime fixtures, network requests, retained-input reads, verifier/key uses, graph commands, commits, and pushes.

Evidence may establish source completeness only. It must not claim that code compiles or tests pass.

## Isolation boundary

Source generation occurs only in the existing repository checkout. It must not create a toolchain root, Go cache, temporary test root, service, listener, database, container, process helper, or external connection.

No raw source or fixture body may be copied outside the repository except ordinary tool-call transport needed to apply the reviewed patch. No source may be sent to an external service or model endpoint.

The accepted owner-only P2-02 evidence root and R3-G1 archive remain untouched.

## Stop conditions

Stop without repair, retry, substitution, or scope expansion if:

- a ninth repository path appears;
- an accepted file differs from commit `2eb263d`;
- a required file, case ID, manifest row, requirement mapping, or negative control is missing;
- a fixture contains a non-`example.invalid` module identity, real response, retained byte, credential, key, correspondence datum, or checksum tile;
- a source imports an external package or adds a dependency, module/workspace directive, build tag, CGO, generator, or `go.sum` path;
- a runtime fixture, symlink, binary, generated output, cache, executable, service, or listener is created;
- a Go, build, test, planner, verifier, graph, package-manager, or network command is attempted;
- a source/manifest hash cannot be reconciled; or
- static evidence or specialist review is incomplete.

A stop leaves P2-03 `Incomplete`, preserves the bounded uncommitted diff, and returns for review. No automatic cleanup or retry is authorized.

## Rollback

On interruption or rejection, do not alter accepted P2 files. Preserve the exact uncommitted eight-path diff until user direction.

Cleanup requires a separate explicit instruction and may remove only the validated eight uncommitted P2-03 paths after confirming they were absent at commit `2eb263d`. No Git reset, checkout, wildcard deletion, broad cache cleanup, accepted-file edit, or unrelated-file removal is permitted.

## Specialist reviews required

| Review function | Required finding |
|---|---|
| Security / privacy | Fixture constants are synthetic, bounded, non-secret, non-executable, and contain no network, key, credential, retained-input, or user-state path |
| Quality / independent verification | All 35 cases and accepted requirements have exact tests or explicit static justification; manifest and diff reconcile |
| Supply chain / maintenance | Imports are standard-library/local only; no dependency, generator, build tag, CGO, workspace, or `go.sum` appears |
| Preservation / provenance | Accepted source remains unchanged and every new source/fixture byte is manifested |
| Architecture / portability | Test source remains local experimental evidence tooling with no product-stack commitment |
| Licensing / cost | No new licensed dependency, account, service, hosted resource, or cost is introduced |
| Orchestrator / governance | Source creation stops before Go, build, test, P2-04, P3, retained inputs, verifier work, R3-O1, or commit |

Any unresolved finding or disagreement blocks P2-03 acceptance.

## Explicit limits

This Accepted request does not authorize:

- creating or modifying any repository path outside the exact eight-path boundary;
- invoking Go, a formatter, compiler, linker, test runner, generator, planner, verifier, key, graph command, or project executable;
- adding a dependency, changing `go.mod`, creating `go.sum`, or using a workspace, package manager, service, listener, database, or container;
- reading retained lookup responses, tiles, correspondence, credentials, accounts, user configuration, or production data;
- accessing the network, cloud AI, telemetry, analytics, or hosted services;
- beginning P2-04, P3, P4, P4-E, R3-O1, Checkpoint B, deployment, stack selection, or production work;
- accepting or executing the separate synthetic-test-run request;
- committing source/evidence or the still-Proposed planner-execution request; or
- pushing.

## Explicit authorization received

The user approved this request, directed that it be marked Accepted and committed alone, and authorized the exact static source-generation workstream subject to the limits in this document.

> I authorize only the P2-03 synthetic fixture and test-source generation under the accepted request: create exactly the eight authorized paths, use only static synthetic `example.invalid` data and accepted local source, produce the complete source manifest and static evidence, and stop for diff review. Do not invoke Go, build, test, execute the planner, read retained inputs, use a verifier or key, access the network, add dependencies, create `go.sum`, begin P2-04 or P3, commit implementation evidence, or push.

This acceptance does not approve the separate test-run request.

## Accepted authorization

The review accepted the eight-path boundary, 35-case identity set, file responsibilities, static source procedure, dependency and fixture restrictions, manifest schema, isolation, evidence, specialist reviews, stop conditions, rollback, and independent authorization gate.

Generation must stop after the uncommitted eight-path source package and static evidence are complete. No build, test, planner execution, retained-input read, dependency change, network action, implementation commit, or push is authorized.
