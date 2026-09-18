# P2-04 Static Specialist Review Findings

**Status:** Accepted
**Review execution date:** 2026-09-18
**Review date:** 2026-09-19
**Frozen scope:** `P2-IMPLEMENTATION-REVIEW.md`, commit `213728e3497ab227146f7dd733061329f9fb1de6`, SHA-256 `9cd1789a50cd6b66541e66e8dc20e4cee3a601842007dfcee7443b025537b0af`
**Reviewed implementation baseline:** commit `649bb5bf62529bfdc7d0e84804d00f47723cafa3`
**Review result:** All seven static specialist findings are accepted as `Pass`; this acceptance does not authorize a build, test, planner execution, retained-input read, or later gate
**Current authority:** Preserve the accepted static review boundary; no source change, Go invocation, build, test, planner execution, retained-input read, verifier/key use, dependency change, network action, later-gate work, or push is authorized

## Purpose and review limit

This record reports the seven static specialist reviews authorized by the accepted P2-04 scope. The reviews cover exactly the accepted 23-path, 141,746-byte P2 implementation object. They establish static source completeness, traceability, provenance, and boundary compliance only.

No Go command, formatter, compiler, linker, test runner, planner, verifier, key, retained input, network tool, package manager, service, or generated runtime fixture was used. A `Pass` in this record is not evidence that the source compiles or that a test or planner behavior succeeds at runtime.

The final SHA-256 of this findings document is intentionally reported outside the document with the acceptance record. Embedding the digest in the hashed file would create a self-referential identity. That separately reported digest records the accepted identity and resolves `UNRESOLVED_P2_REVIEW_SHA256`.

## Review method and zero-action ledger

Permitted static methods used:

- Git tree, commit, history, and diff inspection;
- regular-file, symlink, executable-bit, path-count, and byte-count inspection;
- independent SHA-256 calculation for all 23 paths and the accepted scope document;
- row-by-row comparison of all three self-excluding manifests;
- textual inspection of all planner-owned, copied tlog, fixture, and test source;
- import, directive, capability, unresolved-token, generated-artifact, and domain scans; and
- requirement-to-source and case-to-test mapping.

Explicit action counts during these seven reviews:

| Action | Count |
|---|---:|
| Go invocations | 0 |
| Formatter, compiler, linker, build, test, benchmark, fuzz, or generator runs | 0 |
| Planner or project-code executions | 0 |
| Retained-input or retained-evidence reads | 0 |
| Verifier or key uses | 0 |
| Network requests | 0 |
| Dependencies added or installed | 0 |
| `go.sum` or workspace files created | 0 |
| Graph commands | 0 |
| Services, listeners, containers, databases, or credentials created | 0 |
| Implementation paths changed | 0 |
| Pushes | 0 |

## Frozen review-object reconciliation

### Scope totals

| Source class | Manifest rows | Self-excluding manifest | Paths | Bytes | Manifest SHA-256 | Result |
|---|---:|---:|---:|---:|---|---|
| Planner-owned | 9 | 1 | 10 | 49,515 | `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84` | Match |
| Copied tlog and license | 4 | 1 | 5 | 39,747 | `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d` | Match |
| Synthetic fixture/test source | 7 | 1 | 8 | 52,484 | `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` | Match |
| **Complete object** | **20** | **3** | **23** | **141,746** | Three independent scopes | **Match** |

The synthetic class is seven manifested paths totaling 51,073 bytes plus the 1,411-byte self-excluding manifest. It is eight paths and 52,484 bytes, not nine paths.

All 23 entries are regular non-executable files. No symlink, binary, cache, runtime fixture, generated output, `go.sum`, `go.work`, or `go.work.sum` exists in the review object.

### Exact path identities

| Class | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Copied | `LICENSES/golang.org-x-mod-BSD-3-Clause.txt` | 1,453 | `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad` |
| Planner | `README.md` | 3,466 | `96a65ee7f6cbaa971a9d74b7568b0509fea6e0d7fbed6a5e7e918f01b2a69292` |
| Planner | `cmd/mneme-r3-g2-tile-plan/main.go` | 157 | `877e86645cc8c6409d8da52e118ef25e0643b9e3cad15283b85d4abe555152b9` |
| Copied manifest | `copied-tlog-manifest.tsv` | 1,515 | `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d` |
| Planner | `go.mod` | 59 | `611f1b084ded3e5c0014d7f420d05c58b88e2bb727fb1fa792feccd29541e742` |
| Planner | `internal/planner/model.go` | 3,101 | `d8013d415fb6a5ebaa97fbf941d8d052939293082d7bfc316f6f480b168766c4` |
| Planner | `internal/planner/output.go` | 11,080 | `fbf2f12b6b0ff23ddcb572c3d0977c62084a497d60ef9aca08942520215cd66b` |
| Synthetic test | `internal/planner/output_test.go` | 6,641 | `d1bc78ae8b7d36c41889e33600eb13e6da789d5ccad4665e9394c1c857169093` |
| Planner | `internal/planner/parse.go` | 12,141 | `53f26895106925427dee249c7c1185c9ce5ca48966a06a0b31266989a6d46c31` |
| Synthetic test | `internal/planner/parse_test.go` | 7,061 | `24baf24350457f4ca335e9de63b54969ddd8dc2122186834a46d11661be9f359` |
| Planner | `internal/planner/plan.go` | 12,659 | `8fe2ffb4d72cc093df0182db5a6493867490630ebe0a963657ea37a275bb1d72` |
| Synthetic test | `internal/planner/plan_test.go` | 9,297 | `a72e685c4befae19992c683ce70cee47b4270118ddbc545c96e4d5da1b3c6de5` |
| Planner | `internal/planner/run.go` | 3,131 | `52f28b368995b6389231e407196f6c9998bde869d6da2b76a94f6eabb7fd094c` |
| Synthetic test | `internal/planner/run_test.go` | 5,012 | `e8d3e93cfedda7a1717b6328ee05ffbf7c1ff2538c0b9915efd2bfded557a30e` |
| Synthetic test | `internal/planner/test_helpers_test.go` | 9,575 | `0cbbb75834f9124a94fe76fe6eb4085b320ed73fe8d5a99d860af9367828a085` |
| Copied | `internal/tlog/note.go` | 3,931 | `c1d9ff098f27aab7d354385795f175a4bc0f05c46e3c37f3b3e2223f44b76236` |
| Copied | `internal/tlog/tile.go` | 14,296 | `2eb6a68b3e9f39a2926b201c0813cf2c67a1465aabc4bd88fcb310437e16bc6a` |
| Copied | `internal/tlog/tlog.go` | 18,552 | `c4bb27943a3ec8ea08ae2e0325259dc2707132ab7295d16bd3d238ba699ec628` |
| Planner manifest | `planner-owned-source-manifest.tsv` | 1,265 | `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84` |
| Planner | `sourcebundle.go` | 2,456 | `5dc8a7636a42b2361c77010537cc5dd8d35f2a63d609c5b68154506d768eb76a` |
| Synthetic test | `sourcebundle_test.go` | 3,449 | `a368dfd289b8e182b9a73666a41897231dc8c386280cde5e22d0f86b0b5b6619` |
| Synthetic manifest | `synthetic-test-source-manifest.tsv` | 1,411 | `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05` |
| Synthetic fixture | `testdata/synthetic/cases.json` | 10,038 | `b162f0d1cf8e00ec3b44b3bb3562076eb10c6918591e9b4c2750298c8fd06412` |

Every one of the 20 manifest rows matched its repository path, byte count, and SHA-256. The three manifest files independently matched their accepted SHA-256 values.

## P2-04-S1 — Security and privacy

**Finding:** `Pass`

**Evidence identity:** planner manifest SHA-256 `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84`; synthetic manifest SHA-256 `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05`.

Evidence reviewed:

- The complete import and capability scan found no network client/listener, HTTP/URL package, process execution, shell, plugin, dynamic load, `unsafe`, CGO, credential, token, keychain, telemetry, cloud-AI, database, container, user-home lookup, or environment-read path in planner or test source.
- `internal/planner/run.go:10-38` states and implements the bounded local path from flags to manifest read, declared-input read, structural plan, and output write. Exit class 2 is configuration-only; later stops return 1.
- `internal/planner/parse.go:20-86` bounds and validates the exact fourteen-row manifest; lines 89-150 reject a symlink root, require directory closure, reject symlink/non-regular entries, bound every read, and reconcile bytes and SHA-256.
- `internal/planner/parse.go:153-261` parses UTF-8, record, expected `/go.mod` line, tree, and signature envelope as structure only. No verifier key or authentication result is present.
- `internal/planner/parse.go:264-294` checks file identity before reading and limits reads; lines 315-325 reject noncanonical relative paths and malformed hashes.
- `internal/planner/plan.go:15-34` defines the plan-only sentinel reader; lines 202-237 require that sentinel, zero `SaveTiles`, and at least one captured tile; lines 269-281 reject data-tile, wildcard, escape, and noncanonical paths.
- `internal/planner/output.go:66-177` refuses incomplete plans, requires an empty non-symlink output directory, writes an incomplete marker first, creates outputs exclusively at mode `0600`, and promotes the complete stop register only after all other writes.
- `internal/planner/output.go:50-64` and lines 257-277 make checksum integrity false and all forbidden-capability counters zero.
- `internal/planner/test_helpers_test.go:21`, `143-165`, `168-190`, and `234-259` use deterministic `MNEME_SYNTHETIC_*` constants and `example.invalid` identities. The only URL-shaped test values are `synthetic.example.invalid` environment strings in `run_test.go:94-96`; no client reads them.
- Hostile UTF-8, malformed envelope, path traversal, symlink, oversized input, undeclared input, negative inventory, and output/write-failure cases map to the tests recorded in the case matrix below.

Requirements and stop conditions covered: zero external capability, bounded hostile-input handling, exact input closure, path confinement, no authentication claim, fail-closed output promotion, synthetic-only fixture identity, and no retained or real-data path.

Residual uncertainty: runtime process and network isolation remain unobserved under `U-P2-04-01` and `U-P2-04-02`; cryptographic authenticity remains intentionally unproved under `U-P2-04-03` and `U-P2-04-04`.

Disagreement status: None.

Rejected expansion: invoking Go, executing hostile fixtures, using a verifier/key, reading retained inputs, or probing the network.

Acceptance condition: this finding may be accepted only as a static source-boundary finding with all four residual uncertainties preserved and with no claim of runtime sandbox enforcement or checksum integrity.

## P2-04-S2 — Quality and independent verification

**Finding:** `Pass`

**Evidence identity:** synthetic case inventory SHA-256 `b162f0d1cf8e00ec3b44b3bb3562076eb10c6918591e9b4c2750298c8fd06412`; synthetic manifest SHA-256 `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05`.

Evidence reviewed:

- `cases.json` contains exactly 35 unique case IDs in strict lexical order. `test_helpers_test.go:47-83` freezes the same ordered ID set; lines 85-140 validate schema, trust label, order, uniqueness, required fields, and PASS/STOP expectations.
- The complete 35-case mapping below identifies a precise test or explicit static justification for every ID.
- `run_test.go:36-85` covers the exact command surface and caps; lines 87-104 cover independence from HOME and fake proxy/checksum environment values; lines 106-145 cover normalized configuration, input, and output exit classes.
- `parse_test.go:24-49` covers exact fourteen-input structural parsing; lines 51-135 cover hostile parser structure; lines 138-208 cover manifest, size, directory-closure, symlink, and path controls.
- `plan_test.go:11-27` covers complete fourteen-input planning; lines 29-118 cover head variants, operation closure, and all six order permutations; lines 120-200 cover canonical paths, sentinel, `SaveTiles`, fallback, and deduplication; lines 202-236 cover all three caps.
- `output_test.go:22-70` covers exact names, schemas, normalized text, path uniqueness, and provenance fields; lines 72-123 cover byte determinism and fail-closed incomplete markers; lines 125-179 cover the structural-only trust label, negative inventory, and incomplete-plan refusal.
- `sourcebundle_test.go:11-103` covers deterministic embedded-source output, schema, ordering, hashes, and copied-source/license classification.
- Static inspection found no unresolved token, apparent undeclared API, external prerequisite, nondeterministic time/random source, or path outside test-owned temporary roots.
- No compilation, test, or runtime result is claimed.

### Complete 35-case traceability

| Case ID | Static test or justification |
|---|---|
| `ERR-BLANK-RECORD-LINE` | `TestParseResponseRejectsHostileSyntheticStructure`; added envelope section is rejected as an ambiguous separator before promotion |
| `ERR-DUPLICATE-ID` | `TestInputManifestAndFilesystemBoundaries/ERR-DUPLICATE-ID` |
| `ERR-HEAD-CAP` | `TestPlannerCapsFailClosed/ERR-HEAD-CAP` |
| `ERR-INPUT-CAP` | `TestInputManifestAndFilesystemBoundaries/ERR-INPUT-CAP` |
| `ERR-MALFORMED-ROOT-BASE64` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `ERR-MALFORMED-SIGNATURE` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `ERR-MISSING-INPUT` | `TestInputManifestAndFilesystemBoundaries/ERR-MISSING-INPUT` |
| `ERR-MISSING-TERMINATOR` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `ERR-OPERATION-CAP` | `TestPlannerCapsFailClosed/ERR-OPERATION-CAP` |
| `ERR-OVERSIZED-INPUT` | `TestInputManifestAndFilesystemBoundaries/ERR-OVERSIZED-INPUT` |
| `ERR-PATH-CAP` | `TestPlannerCapsFailClosed/ERR-PATH-CAP` |
| `ERR-PATH-TRAVERSAL` | `TestInputManifestAndFilesystemBoundaries/ERR-PATH-TRAVERSAL` |
| `ERR-RECORD-NEGATIVE` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `ERR-RECORD-NONCANONICAL` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `ERR-SAVE-TILES` | `TestTilePathFallbackSentinelAndDeduplication/ERR-SAVE-TILES`; production stop at `plan.go:233-235` |
| `ERR-SYMLINK-INPUT` | `TestInputManifestAndFilesystemBoundaries/ERR-SYMLINK-INPUT` |
| `ERR-TREE-NONCANONICAL` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `ERR-UNEXPECTED-INPUT` | `TestInputManifestAndFilesystemBoundaries/ERR-UNEXPECTED-INPUT` |
| `ERR-UTF8` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `ERR-WRONG-ROOT-LENGTH` | `TestParseResponseRejectsHostileSyntheticStructure` |
| `SYN-EQUAL-DIFFERENT-ROOT` | `TestSingleRecordAndHeadVariants/SYN-EQUAL-DIFFERENT-ROOT` |
| `SYN-EQUAL-SAME-ROOT` | `TestSingleRecordAndHeadVariants/SYN-EQUAL-SAME-ROOT` |
| `SYN-INCOMPLETE-MARKER` | `TestIncompleteMarkerFailsClosed` |
| `SYN-LARGE-TILE-NUMBER` | `TestTilePathFallbackSentinelAndDeduplication/SYN-LARGE-TILE-NUMBER` |
| `SYN-MULTI-SIZE-HEADS` | `TestOperationClosureAndOrderIndependence` |
| `SYN-NEGATIVE-INVENTORY` | `TestNormalizedSufficiencyAndNegativeInventory` |
| `SYN-ORDER-PERMUTATIONS` | `TestOperationClosureAndOrderIndependence`; six permutations are enumerated |
| `SYN-OUTPUT-DETERMINISM` | `TestSyntheticOutputsAreByteDeterministic` |
| `SYN-PARTIAL-FALLBACK` | `TestTilePathFallbackSentinelAndDeduplication/SYN-PARTIAL-FALLBACK` |
| `SYN-POWER-OF-TWO` | `TestTilePathFallbackSentinelAndDeduplication/SYN-POWER-OF-TWO` |
| `SYN-SENTINEL-REQUIRED` | `TestTilePathFallbackSentinelAndDeduplication/SYN-SENTINEL-REQUIRED` |
| `SYN-SHARED-TILES` | `TestTilePathFallbackSentinelAndDeduplication/SYN-SHARED-TILES` |
| `SYN-SINGLE-RECORD` | `TestSingleRecordAndHeadVariants/SYN-SINGLE-RECORD` |
| `SYN-SOURCE-PROVENANCE` | `TestEmbeddedSourceManifestIsDeterministic` and `TestEmbeddedSourceProvenanceClassifications`; explicit cross-package static mapping |
| `SYN-VALID-14` | `TestParseValidSyntheticResponses` and `TestSyntheticValid14Plan` |

Requirements and stop conditions covered: exact case inventory, parser and cap behavior, operation closure, fallback/sentinel boundary, deterministic schemas and outputs, fail-closed promotion, provenance classification, and absence of hidden prerequisites.

Residual uncertainty: the source has not been parsed by a Go compiler and none of the test expectations has been observed at runtime. These are exactly `U-P2-04-01` and `U-P2-04-02`.

Disagreement status: None.

Rejected expansion: using a compiler, formatter, test runner, standalone parser, generated golden file, or runtime fixture to strengthen the static finding.

Acceptance condition: accept only the completeness and internal consistency of the static test design. Test success remains blocked on the independent build and test gates.

## P2-04-S3 — Supply chain and maintenance

**Finding:** `Pass`

**Evidence identity:** `go.mod` SHA-256 `611f1b084ded3e5c0014d7f420d05c58b88e2bb727fb1fa792feccd29541e742`; copied manifest SHA-256 `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d`; planner manifest SHA-256 `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84`.

Evidence reviewed:

- `go.mod` contains only `module example.invalid/mneme-r3-g2-tile-planner` and `go 1.27.1`. It contains no `require`, `replace`, `exclude`, `retract`, or `tool` directive.
- No `go.sum`, workspace file, vendor tree, generator directive, build tag, CGO directive, external test library, compiled artifact, or undeclared source appears.
- Standard-library imports are limited to `bufio`, `bytes`, `crypto/sha256`, `embed`, `encoding/base64`, `encoding/hex`, `encoding/json`, `errors`, `flag`, `fmt`, `io`, `io/fs`, `math/bits`, `os`, `path/filepath`, `sort`, `strconv`, `strings`, `testing`, and `unicode/utf8`.
- Local imports are limited to the accepted module root, `internal/planner`, and `internal/tlog`. No third-party import path is compiled as an external module.
- The copied scope is exactly `note.go`, `tile.go`, `tlog.go`, and the BSD 3-Clause license. Their byte counts and hashes match all four copied-manifest rows; no broader x/mod package or executable content exists.
- `sourcebundle.go:20` embeds a literal bounded set plus `internal/planner/*.go` and `internal/tlog/*.go`; `ManifestTSV` sorts every embedded path and hashes its bytes. The accepted test-source expansion is visible through the planner glob rather than acquired as a dependency.

Requirements and stop conditions covered: no module graph expansion, no external dependency, exact copied-source scope, deterministic source embedding, no generator/build variation, and no undeclared artifact.

Residual uncertainty: actual compiler compatibility and transitive toolchain behavior remain unproved under `U-P2-04-01`. No dependency acquisition or graph closure is inferred from this finding.

Disagreement status: None.

Rejected expansion: running `go list`, `go mod graph`, `go env`, a compiler, a package manager, or any dependency lookup.

Acceptance condition: the source set must remain byte-identical to the three manifests. Any later dependency, directive, source expansion, or toolchain change requires a separate reviewed gate.

## P2-04-S4 — Preservation and provenance

**Finding:** `Pass`

**Evidence identity:** planner manifest SHA-256 `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84`; copied manifest SHA-256 `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d`; synthetic manifest SHA-256 `64a00de1d8e29c157baa8e2955e82496e602143f507f74d0ef1f6083b77e0f05`.

Evidence reviewed:

- All 20 manifest rows and three self-excluding manifest hashes independently reconcile to 23 regular files and 141,746 bytes.
- P2-01 is anchored by commit `01a86b3c5d215ea6cdb148f070625b89f3f21f3e`; P2-02 by `2eb263dfbea3fd891c93d20fbca53f586489608c`; P2-03 by `649bb5bf62529bfdc7d0e84804d00f47723cafa3`.
- The P2-01 to P2-02 diff added the four copied paths and copied manifest, and changed only `sourcebundle.go` plus its single planner-manifest row. That accepted provenance update is recorded at SHA-256 `5dc8a7636a42b2361c77010537cc5dd8d35f2a63d609c5b68154506d768eb76a`.
- The P2-02 acceptance record preserves the copied archive SHA-256 `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12`, exact archive members, module pseudo-version `v0.36.1-0.20260813213634-8569e2639ca1`, license linkage, and accepted `realpath` anomaly/substitute checks.
- The P2-02 to P2-03 diff added exactly the eight synthetic paths and changed no prior path.
- The P2-03 commit record states seven manifested inputs totaling 51,073 bytes plus one 1,411-byte self-excluding manifest, eight paths, 52,484 bytes, and an exact eight-path rollback boundary.
- The accepted implementation tree is unchanged from `649bb5b` through the current scope commit.

Recovery boundary:

1. restore P2-01 planner-owned history from `01a86b3`;
2. restore and audit the accepted copied-source/provenance delta from `2eb263d`; and
3. restore the complete accepted P2 review object from `649bb5b`.

The repository commits and three manifests are sufficient to reconstruct and independently recheck the static review object. No retained lookup, external service, account, network path, or generated output is required for this recovery boundary.

Requirements and stop conditions covered: exact path/byte/hash closure, accepted mutation history, copied-member provenance, license linkage, corrected P2-03 accounting, and application-independent recovery from Git objects.

Residual uncertainty: the retained Go archive and owner-only external evidence roots were not read during this review. Their previously accepted identities are historical provenance anchors, not reverified payloads in P2-04.

Disagreement status: None.

Rejected expansion: reading the retained archive/evidence roots, re-extracting members, or producing a new aggregate manifest.

Acceptance condition: accept the repository-contained preservation chain only. Reverification against retained external artifacts requires a separately authorized operation.

## P2-04-S5 — Architecture and portability

**Finding:** `Pass`

**Evidence identity:** README SHA-256 `96a65ee7f6cbaa971a9d74b7568b0509fea6e0d7fbed6a5e7e918f01b2a69292`; planner manifest SHA-256 `31e9f4e9dd729fb8f67796ee901662a3a2a4e5e742860a103ee0e48bb19d0e84`.

Evidence reviewed:

- `README.md:15-31` defines an isolated Phase-3 evidence tool that derives literal checksum-tile paths from unverified structure and explicitly does not authenticate a response, signature, tree, record, module hash, or tile.
- The command surface is local files in, ten application-independent text/JSON files out. Inputs are exact bytes and hashes; outputs use deterministic ordering, normalized LF text, fixed schemas, and no database or service state.
- Planner behavior is limited to structural parsing and path planning through the copied tlog algorithm. The plan-only reader returns before tile data, Merkle proof, signature, or network behavior.
- Source contains no Gmail, Outlook, Apple, archive, correspondence, account, provider, UI, database, production server, cloud model, Docker, Podman, ZFS, or Tailscale integration.
- The experiment does not select or constrain Mneme's product stack. The `go 1.27.1` declaration applies only to this isolated evidence tool.
- Static platform assumptions are explicit: filesystem semantics use Go `os`/`filepath`; tests propose temporary directories and symlinks; output promotion uses rename replacement behavior. These assumptions require observation at the later approved build/test gate and are not presented as product portability evidence.

Requirements and stop conditions covered: experimental isolation, deterministic local evidence contract, no product-state coupling, no production integration, and no stack selection.

Residual uncertainty: compiler/OS behavior, symlink-test availability, and rename semantics remain runtime questions under `U-P2-04-01` and `U-P2-04-02`.

Disagreement status: None.

Rejected expansion: treating Go, macOS, copied tlog code, or the ten-output contract as a selected product architecture.

Acceptance condition: accept only the experiment architecture. Any reuse in Mneme product architecture requires the separate Phase-2 stack-selection process, which remains without a selected stack.

## P2-04-S6 — Licensing and cost

**Finding:** `Pass`

**Evidence identity:** license SHA-256 `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad`; copied manifest SHA-256 `4e75011ceafa397b0bdf670c1867cfcc18aab5c25d3207ea0c74cabea501062d`.

Evidence reviewed:

- The three copied Go files retain the Go Authors copyright and BSD-style license header.
- The exact 1,453-byte BSD 3-Clause text is present under `LICENSES/` and matches its copied-manifest row.
- All three copied source rows identify module `golang.org/x/mod v0.36.1-0.20260813213634-8569e2639ca1`, the accepted Go 1.27.1 archive SHA-256, exact archive-member path, `BSD-3-Clause-x-mod`, and `BYTE_IDENTICAL` status.
- `sourcebundle.go:64-74` classifies the three copied sources, license, and provenance manifest distinctly; `sourcebundle_test.go:38-103` statically checks those classifications.
- Planner-owned and synthetic files introduce no third-party dependency, service, account, hosted resource, telemetry, subscription, or paid cost.

Requirements and stop conditions covered: exact license bytes, copied-file attribution, module/version/archive provenance, deterministic classification, and zero service/account cost.

Residual uncertainty: binary-distribution notice placement is outside P2 because no binary has been built or distributed. A later distribution gate must preserve the license terms.

Disagreement status: None.

Rejected expansion: searching for a substitute notice, querying a license service, or acquiring any additional package/license artifact.

Acceptance condition: the copied files and license must remain byte-identical and linked in provenance output. Any binary distribution or source expansion requires a later license review.

## P2-04-S7 — Orchestrator and governance

**Finding:** `Pass`

**Evidence identity:** frozen scope SHA-256 `9cd1789a50cd6b66541e66e8dc20e4cee3a601842007dfcee7443b025537b0af`; review-time Proposed test-run request SHA-256 `9f0cafd4980ecd62d31f565d9af5d44bf686cdb6fcaf6b49e3047734bd8319e6`; review-time Proposed planner-execution request SHA-256 `6a6dac7c0f3fe90f1f9f43559275015887c67d5e36e6465d793cf50d3a7997ad`.

Evidence reviewed:

- Accepted P2 sequence: P2-01 commit `01a86b3`; P2-02 commit `2eb263d`; P2-03 commit `649bb5b`; frozen P2-04 scope commit `213728e`.
- P2-03 accounting is preserved as seven manifested inputs plus one self-excluding manifest, eight paths, 52,484 bytes, and an eight-path rollback boundary.
- The test-run and planner-execution requests both remain `Proposed`, unchanged during review, uncommitted, and outside the 23-path implementation object.
- The review introduced no implementation change and no execution authority. The user accepted this separate findings record on 2026-09-19 as a completed static review only.
- No disagreement is open. All later uncertainties are explicit below.
- Separate gates remain for P3 build authorization, P3 synthetic-test authorization, P3 decision, P4 evidence, retained-input execution, R3-O1, stack selection, deployment, implementation/evidence commit, and push.

Requirements and stop conditions covered: staged acceptance history, immutable review scope, proposal separation, no authority leakage, explicit uncertainty, and independent future gates.

Residual uncertainty: all four accepted P2 residual uncertainties remain open; no later gate is pre-approved.

Disagreement status: None.

Rejected expansion: modifying or accepting either Proposed request during the frozen review, starting P3/P4, interpreting static `Pass` as test approval, committing any file beyond the separately authorized findings document, or pushing.

Acceptance condition: Satisfied on 2026-09-19 by the user's explicit acceptance of the seven findings as a completed static review. This closes only P2-04 as an implementation-review prerequisite.

## Judgment-call register

### J-P2-04-01 — Embedded test-source provenance labels

`sourcebundle.go` embeds `internal/planner/*.go`, so later P2-03 `_test.go` files are included in the runtime source manifest and receive origin `planner-owned`. The accepted P2-03 source manifest uses owner `planner-test-owned`.

Resolution: no conflict. `origin` answers whether bytes are project-created or externally copied and determines license classification; `owner` identifies the P2 governance class. Both labels correctly describe the same test files. The runtime source manifest is an embedded-source provenance output, not a fourth manifest for the complete 23-path P2 review object. `sourcebundle_test.go:85-96` intentionally checks the origin/license dimension.

Status: Resolved; no disagreement.

### J-P2-04-02 — `ERR-BLANK-RECORD-LINE` stop wording

The case inventory describes an inserted blank line in record text. The test mutation creates an additional section between the formatted record and tree note, and the parser stops at the multiple-envelope-separator check. The specific diagnostic is therefore `unambiguous envelope separator`, not the case inventory's higher-level phrase `record structure is malformed`.

Resolution: the case's required property is fail-closed rejection before structural promotion, and that property is directly asserted. Independently, `tlog.ParseRecord` and `parse.go:168-170` reject malformed record text. No runtime result is claimed. Exact error-message equality was not an accepted requirement.

Status: Resolved; no disagreement.

## Residual-uncertainty register

| ID | State after review | Treatment |
|---|---|---|
| `U-P2-04-01` | Open | Source has not been formatted, compiled, linked, or tested; only a separately accepted P3 build/test action may address it |
| `U-P2-04-02` | Open | Synthetic expectations have not been observed at runtime; only a separately accepted synthetic test run and P4 review may address it |
| `U-P2-04-03` | Open by design | No retained checksum response was read or authenticated; retained-input work remains separately gated |
| `U-P2-04-04` | Open by design | The planner is not a checksum signed-tree or Merkle verifier; later offline verification remains separate |

No unresolved uncertainty remains inside the authorized static P2 review scope. The four listed uncertainties belong to later gates and are not converted into evidence by this review.

## Disagreement register

| ID | Specialists | Status | Resolution |
|---|---|---|---|
| None | All seven | No disagreement | No conflicting finding, interpretation, or acceptance condition was identified |

## Consolidated finding register

| ID | Specialist function | Finding | Evidence/hash status | Disagreement | Acceptance condition |
|---|---|---|---|---|---|
| `P2-04-S1` | Security and privacy | `Pass` | Capability, hostile-input, synthetic-only, and boundary evidence reconciled to planner and synthetic manifests | None | Static boundary only; runtime isolation and integrity remain unproved |
| `P2-04-S2` | Quality and independent verification | `Pass` | All 35 cases mapped; source/test identities match synthetic manifest | None | No compile/test claim; later test authorization remains required |
| `P2-04-S3` | Supply chain and maintenance | `Pass` | Module, import, copied-source, and no-artifact checks reconcile | None | Any dependency or source expansion requires separate review |
| `P2-04-S4` | Preservation and provenance | `Pass` | 23 paths, 141,746 bytes, 20 rows, 3 manifests, and commit history reconcile | None | Repository-contained chain only; retained artifacts not reread |
| `P2-04-S5` | Architecture and portability | `Pass` | Experimental local evidence boundary preserved | None | No product-stack selection or runtime portability claim |
| `P2-04-S6` | Licensing and cost | `Pass` | Copied files, BSD license, provenance, and zero-service-cost boundary reconcile | None | Later binary distribution requires a new license review |
| `P2-04-S7` | Orchestrator and governance | `Pass` | Accepted sequence and review-time Proposed-request hashes preserved | None | Satisfied 2026-09-19; no later authority follows |

## Consolidated decision

The seven specialist reviews find the frozen P2 implementation object statically complete and consistent with the accepted P2-04 scope. The proposed consolidated decision is:

> **P2-04 static implementation review: Pass, Accepted.**

This P2-04 decision became Accepted on 2026-09-19 after:

1. the complete findings diff is reviewed;
2. the separately reported final findings-document SHA-256 is reviewed as the resolution of `UNRESOLVED_P2_REVIEW_SHA256`;
3. the seven `Pass` findings, two resolved judgment calls, four carried uncertainties, and no-disagreement register are accepted; and
4. the user explicitly accepted the seven findings as a completed static review.

Acceptance closes only P2-04 as an implementation-review prerequisite. It does not authorize or accept the Proposed test-run request, P3-01, a Go invocation, formatting, compilation, build, test, planner execution, retained-input read, verifier/key use, network access, dependency change, `go.sum`, graph work, P4, R3-O1, stack selection, deployment, commit of later work, or push.

## Rollback and review boundary

This findings document is the only path authorized for its acceptance commit. After that commit, it is the immutable accepted P2-04 findings record. Any future amendment requires separate review and must not alter:

- the accepted 23-path P2 implementation;
- commits `01a86b3`, `2eb263d`, `649bb5b`, or `213728e`;
- either independently governed Proposed authorization request;
- retained roots or evidence; or
- any unrelated repository path.

No Git reset, checkout, wildcard deletion, broad cleanup, test, build, planner execution, commit, or push is authorized by this record.
