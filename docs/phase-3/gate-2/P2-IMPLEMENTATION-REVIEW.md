# P2-04 Complete Implementation Review Package

**Status:** Accepted
**Package date:** 2026-09-18
**Review date:** 2026-09-18
**Review readiness:** Authorized for the seven declared static specialist reviews only
**Current authority:** Perform the seven declared static reviews against this frozen scope and record the findings separately; no source edit, Go invocation, formatting, build, test, planner execution, retained-input read, verifier/key use, dependency change, network action, later-gate work, implementation commit, or push is authorized
**Governing prerequisite:** [R3-G2 planner prerequisite-resolution record](R3-G2-PLANNER-PREREQUISITE-RESOLUTION.md)
**Accepted scope artifact:** `P2-IMPLEMENTATION-REVIEW.md`; its committed identity freezes the review boundary, while specialist findings must be recorded separately

## Purpose

P2-04 is the seven-function static review of the complete P2 implementation. It determines whether the accepted planner-owned source, copied transparency-log source, synthetic fixtures, and test source are sufficiently bounded, traceable, and reviewable to close P2 as an implementation-review prerequisite.

P2-04 does not compile, format, build, test, execute, authenticate, or validate retained checksum-database data. A static `Pass` means only that the reviewed source package satisfies the accepted P2 design and governance boundary. Buildability and runtime behavior remain unresolved until separately approved P3 and P4 work.

## Accepted input anchors

| P2 item | Accepted commit | Accepted object | Current accepted identity |
|---|---|---|---|
| `P2-01` | `01a86b3c5d215ea6cdb148f070625b89f3f21f3e` | Planner-owned source baseline | Historical baseline; current planner-owned manifest includes the accepted P2-02 `sourcebundle.go` provenance update |
| `P2-02` | `2eb263dfbea3fd891c93d20fbca53f586489608c` | Copied tlog source, license, provenance classification, and manifests | `planner-owned-source-manifest.tsv` SHA-256 `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84`; `copied-tlog-manifest.tsv` SHA-256 `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d` |
| `P2-03` | `649bb5bf62529bfdc7d0e84804d00f47723cafa3` | Synthetic fixtures, test source, and self-excluding manifest | `synthetic-test-source-manifest.tsv` SHA-256 `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` |

The review baseline is commit `649bb5bf62529bfdc7d0e84804d00f47723cafa3`. The unchanged Proposed test-run and planner-execution requests are outside the P2 implementation source set and must not influence a finding.

## Complete 23-path review boundary

The complete accepted P2 repository object is exactly these 23 regular files:

```text
experiments/phase-3/r3-g2-tile-planner/LICENSES/golang.org-x-mod-BSD-3-Clause.txt
experiments/phase-3/r3-g2-tile-planner/README.md
experiments/phase-3/r3-g2-tile-planner/cmd/mneme-r3-g2-tile-plan/main.go
experiments/phase-3/r3-g2-tile-planner/copied-tlog-manifest.tsv
experiments/phase-3/r3-g2-tile-planner/go.mod
experiments/phase-3/r3-g2-tile-planner/internal/planner/model.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/output.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/output_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/parse.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/parse_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/plan.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/plan_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/run.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/run_test.go
experiments/phase-3/r3-g2-tile-planner/internal/planner/test_helpers_test.go
experiments/phase-3/r3-g2-tile-planner/internal/tlog/note.go
experiments/phase-3/r3-g2-tile-planner/internal/tlog/tile.go
experiments/phase-3/r3-g2-tile-planner/internal/tlog/tlog.go
experiments/phase-3/r3-g2-tile-planner/planner-owned-source-manifest.tsv
experiments/phase-3/r3-g2-tile-planner/sourcebundle.go
experiments/phase-3/r3-g2-tile-planner/sourcebundle_test.go
experiments/phase-3/r3-g2-tile-planner/synthetic-test-source-manifest.tsv
experiments/phase-3/r3-g2-tile-planner/testdata/synthetic/cases.json
```

No parent documentation, retained evidence root, archive, cache, generated runtime fixture, binary, output, or Proposed authorization request is part of the implementation review object.

## Manifest and byte reconciliation

| Source class | Manifest rows | Self-excluding manifest paths | Repository paths | Bytes | Manifest SHA-256 |
|---|---:|---:|---:|---:|---|
| Planner-owned | 9 | 1 | 10 | 49,515 | `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84` |
| Copied tlog and license | 4 | 1 | 5 | 39,747 | `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d` |
| Synthetic fixture/test source | 7 | 1 | 8 | 52,484 | `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` |
| **Complete P2 review object** | **20** | **3** | **23** | **141,746** | Three independently reported self-excluding manifest identities |

The synthetic class consists of seven manifested inputs totaling 51,073 bytes plus its 1,411-byte self-excluding manifest. A finding must fail if it treats that class as nine paths, includes the manifest as its own row, or reports a total other than eight paths and 52,484 bytes.

## Permitted review method

The review may use only static inspection and read-only identity checks over commit `649bb5b`, including:

- exact Git tree, commit, diff, and path inventory inspection;
- byte counts, SHA-256 calculations, and manifest-row reconciliation;
- textual inspection of imports, directives, command surfaces, caps, output schemas, error handling, provenance classification, licenses, fixtures, and tests;
- requirement-to-source and requirement-to-test traceability;
- searches for forbidden capability, unresolved token, real-data, credential, key, network, process, service, dependency, and generated-output paths; and
- documentation of uncertainty, disagreements, negative findings, and rejected expansions.

The review must not invoke Go or any formatter, compiler, linker, test runner, package manager, generator, project executable, planner, verifier, key, graph command, service, listener, container, network tool, or retained-input reader. It must not create a toolchain root, cache, fixture runtime tree, binary, `go.sum`, workspace, SBOM, license report, or generated output.

## Review record schema

Each specialist must record:

1. reviewer function;
2. finding: `Pass`, `Fail`, or `Incomplete`;
3. exact files and line-level evidence reviewed;
4. manifest/hash checks performed;
5. requirements and stop conditions covered;
6. residual uncertainty that belongs to a later gate;
7. disagreement with another finding, if any; and
8. rejected scope expansion, if any.

`Pass` is unavailable when required evidence is absent. `Incomplete` is required for an unresolved question. A disagreement remains blocking until the record contains a reviewed resolution; majority agreement is insufficient.

## Seven required specialist reviews

### P2-04-S1 — Security and privacy

Required review:

- prove that the planner has no network client, listener, external process, shell, plugin, dynamic-load, credential, token, keychain, user-home, telemetry, cloud-AI, service, database, or container path;
- inspect bounded reads, canonical relative paths, symlink rejection, directory closure, exclusive output writes, incomplete markers, caps, and plan-only sentinel behavior;
- verify that signature and tree material is parsed only as unauthenticated structure and no verifier or authentication result exists;
- verify that all fixture identities use `example.invalid`, all fixture bytes are visibly synthetic, and no retained response, real correspondence, credential, key, or production identifier appears; and
- map hostile UTF-8, malformed envelope, path traversal, symlink, oversized input, undeclared input, negative inventory, and write-failure cases to source or test evidence.

Required finding: `Pending`.

### P2-04-S2 — Quality and independent verification

Required review:

- reconcile all 35 unique ordered case IDs to a precise test or explicit static justification;
- trace parser constraints, the exact fourteen-input contract, head/operation/path caps, order closure, equal-size variants, partial/full fallback paths, sentinel behavior, output schemas, determinism, exit classes, and failure promotion;
- inspect tests for internal consistency, deterministic constants, exact expected values, bounded temporary writes, and absence of hidden external prerequisites;
- verify that no test result, compilation result, or runtime result is claimed; and
- identify any apparent syntax, API, fixture, expectation, or coverage defect for resolution before P2-04 acceptance.

Required finding: `Pending`.

### P2-04-S3 — Supply chain and maintenance

Required review:

- verify that `go.mod` contains only the accepted module identity and Go version, with no `require`, `replace`, `exclude`, `retract`, or `tool` directive;
- verify that `go.sum`, workspace files, generator directives, build tags, CGO, external test libraries, and undeclared source are absent;
- inventory every import and classify it as standard library or accepted local module source;
- reconcile copied tlog files to the accepted hashes and prove no broader x/mod package or executable content was copied; and
- verify that source embedding and provenance classification remain deterministic and bounded.

Required finding: `Pending`.

### P2-04-S4 — Preservation and provenance

Required review:

- reconcile exactly 23 regular files and 141,746 bytes against the three self-excluding manifest scopes;
- independently verify all 20 manifest rows and the three manifest SHA-256 values;
- verify P2-01 history, the accepted P2-02 `sourcebundle.go` provenance update, copied archive-member identities, license linkage, and P2-03 eight-path acceptance record;
- confirm that no accepted source byte changed after its governing commit except the explicitly accepted P2-02 update; and
- define the exact recovery boundary as restoration from commits `01a86b3`, `2eb263d`, and `649bb5b` without retained-input or external-service dependence.

Required finding: `Pending`.

### P2-04-S5 — Architecture and portability

Required review:

- verify that the source remains an isolated Phase-3 experiment and does not select or constrain the Mneme product stack;
- verify that planner behavior is deterministic, local, application-independent, and limited to structural parsing and literal tile-path planning;
- identify platform assumptions in source and proposed test behavior without executing them;
- verify that no production deployment, live archive, account, provider, database, UI, cloud model, or server configuration is introduced; and
- confirm that the planner output contract remains evidence tooling rather than product state.

Required finding: `Pending`.

### P2-04-S6 — Licensing and cost

Required review:

- verify the three copied tlog files, module pseudo-version, archive provenance, and exact BSD 3-Clause license bytes;
- verify that copied-source manifest rows consistently reference `BSD-3-Clause-x-mod` and that sourcebundle classifications preserve that status;
- confirm that planner-owned and synthetic files introduce no third-party source, dependency, service, account, hosted resource, telemetry, or paid cost; and
- record any unresolved notice or attribution question as blocking rather than searching for or acquiring another artifact.

Required finding: `Pending`.

### P2-04-S7 — Orchestrator and governance

Required review:

- reconcile the P2-01 → P2-02 → P2-03 sequence and exact accepted commits;
- verify that the P2-03 acceptance record states seven manifested inputs plus one self-excluding manifest, eight paths, 52,484 bytes, and an eight-path rollback boundary;
- confirm that the Proposed test-run and planner-execution requests remain unchanged, uncommitted, non-executable, and outside the review object;
- verify that the static review adds no source change or authority and that all disagreements and uncertainties are explicit; and
- preserve the separate gates for P3 build authorization, P3 synthetic-test authorization, P3 decision, P4 evidence, retained-input execution, R3-O1, stack selection, deployment, commit, and push.

Required finding: `Pending`.

## Consolidated finding register

| ID | Specialist function | Status | Evidence | Uncertainty | Disagreement |
|---|---|---|---|---|---|
| `P2-04-S1` | Security and privacy | `Pending` | Not yet recorded | Not yet recorded | None recorded |
| `P2-04-S2` | Quality and independent verification | `Pending` | Not yet recorded | Not yet recorded | None recorded |
| `P2-04-S3` | Supply chain and maintenance | `Pending` | Not yet recorded | Not yet recorded | None recorded |
| `P2-04-S4` | Preservation and provenance | `Pending` | Not yet recorded | Not yet recorded | None recorded |
| `P2-04-S5` | Architecture and portability | `Pending` | Not yet recorded | Not yet recorded | None recorded |
| `P2-04-S6` | Licensing and cost | `Pending` | Not yet recorded | Not yet recorded | None recorded |
| `P2-04-S7` | Orchestrator and governance | `Pending` | Not yet recorded | Not yet recorded | None recorded |

No consolidated decision exists while any row is `Pending`, `Incomplete`, or `Fail`.

## Known residual uncertainties carried beyond P2

| ID | Residual uncertainty | P2 treatment | Earliest permitted resolution |
|---|---|---|---|
| `U-P2-04-01` | Source has not been formatted, compiled, linked, or tested | Explicitly preserved; no buildability or runtime claim | Separately accepted P3 build and synthetic-test work |
| `U-P2-04-02` | Synthetic expectations have not been observed at runtime | Explicitly preserved; static traceability only | Separately accepted P3 synthetic-test run and P4 evidence review |
| `U-P2-04-03` | No retained checksum response has been read or authenticated | Required boundary, not a defect | Only after all P2–P4 and P4-E gates are accepted |
| `U-P2-04-04` | The planner does not prove checksum-database signed-tree or Merkle integrity | Required non-verifier boundary | Separately accepted offline verification work outside planner execution |

These uncertainties may remain after a static P2-04 `Pass`; they may not be silently converted into evidence or authority.

## Stop conditions

Stop the review as `Incomplete` without source repair or scope expansion if:

- the review object is not exactly 23 paths and 141,746 bytes;
- a manifest row, path, byte count, hash, provenance classification, license link, or acceptance-record total does not reconcile;
- a fourth manifest scope, undeclared source, dependency, `go.sum`, workspace, generated file, symlink, binary, cache, runtime fixture, or output appears;
- a planner or test source contains an undeclared external import or forbidden capability;
- a fixture contains retained, live, credential, key, correspondence, or production data;
- a reviewer needs a Go command, build, test, network request, retained-input read, verifier, key, service, or generated output to reach a finding;
- a finding is missing evidence, contains an unresolved uncertainty within P2 scope, or conflicts with another finding; or
- the Proposed test-run or planner-execution request changes during review.

On stop, preserve the exact repository state, record the issue and affected specialist functions, and return for a separately reviewed remediation proposal. No automatic edit, retry, test, build, cleanup, or gate advance is authorized.

## Acceptance condition and approval gate

The P2-04 findings decision becomes Accepted only when:

1. all seven specialist findings are recorded as `Pass`;
2. every required identity, row, count, hash, source boundary, requirement mapping, and rollback statement reconciles;
3. every P2-scope uncertainty and disagreement is resolved in the record;
4. later-gate uncertainties remain explicitly carried without unsupported claims;
5. the exact final record SHA-256 is reported separately as the resolution of `UNRESOLVED_P2_REVIEW_SHA256`;
6. the complete diff is presented for review; and
7. the user explicitly accepts the P2-04 decision and separately authorizes any next step.

Acceptance of P2-04 would close only the implementation-review prerequisite. It would not accept or execute the Proposed test-run request, authorize P3-01, invoke Go, build, test, read retained inputs, execute the planner, use a verifier/key, access the network, create `go.sum`, run graph commands, begin R3-O1, select a stack, deploy, commit later work, or push.

## Rollback

After this accepted scope document is committed, it remains the immutable review contract. Rejection or interruption of the specialist review must leave this scope document and the accepted P2 implementation unchanged. Any separately drafted findings package has its own exact rollback boundary.

Rollback must not alter the accepted 23-path P2 implementation, commits `01a86b3`, `2eb263d`, or `649bb5b`, the retained evidence roots, the Proposed test-run request, or the Proposed planner-execution request. No Git reset, checkout, wildcard deletion, broad cleanup, or unrelated-file change is authorized.

## Explicit non-authorization

This Accepted scope document does not authorize:

- changing any implementation, fixture, manifest, license, module, test, or authorization request;
- invoking Go, formatting, compiling, linking, building, testing, benchmarking, fuzzing, generating, installing, or executing the planner;
- creating a disposable root, toolchain copy, cache, binary, runtime fixture, output set, `go.sum`, workspace, SBOM, license report, or execution evidence;
- reading retained lookup responses, checksum tiles, correspondence, accounts, credentials, keys, user configuration, or production data;
- using a verifier, signature key, Merkle verifier, network, cloud AI, telemetry, analytics, service, listener, database, container, or package manager;
- accepting or executing the Proposed test-run or planner-execution requests;
- beginning P3, P4, P4-E, R3-O1, Checkpoint B, stack selection, deployment, production work, or real-data work;
- committing a specialist-findings package or any later artifact without separate user approval; or
- pushing.

## Accepted scope decision

The review accepted the 23-path boundary, three self-excluding manifest scopes, corrected P2-03 path and byte accounting, accepted input identities, static review method, seven specialist assignments, finding schema, residual uncertainties, stop conditions, acceptance gate, rollback, and explicit non-authorization as the frozen P2-04 review scope.

Scope acceptance authorizes only the seven static specialist reviews. All seven findings remain `Pending`, P2-04 remains unresolved, and no build, test, planner execution, retained-input access, P3, or P4 authority follows from this decision.
