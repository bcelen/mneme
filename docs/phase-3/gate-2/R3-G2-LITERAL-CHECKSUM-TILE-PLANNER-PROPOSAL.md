# R3-G2 Literal Checksum-Tile Planner Proposal

**Status:** Accepted
**Proposal date:** 2026-09-18
**Review date:** 2026-09-18
**Authority:** Accepted planning decision only; no planner implementation, build, execution, retained-input access, verifier, acquisition, graph work, or later-stage action is authorized
**Governing decision:** [Accepted R3-G2 checksum-integrity remediation](R3-G2-CHECKSUM-INTEGRITY-REMEDIATION-PROPOSAL.md)
**Selected direction:** Offline native verification using the retained lookup responses, preceded by an accepted planner result and literal tile manifest

## Purpose

This proposal defines a deterministic, offline, non-verifying planner for the fourteen retained R3-G2 checksum-database lookup responses. The planner's only purpose would be to:

1. prove that the retained response set contains every structural field needed to derive the native Go 1.27.1 client's possible checksum-tile reads;
2. account conservatively for processing order, distinct tree heads, tree-consistency checks, record checks, partial tiles, and previously unknown paths;
3. emit a complete literal checksum-tile manifest for separate review; and
4. stop before any cryptographic verifier, network request, tile acquisition, `go list`, `go mod graph`, or `go.sum` action.

The planner would not decide that a signature, tree, record, or tile is authentic. Its sufficiency result would mean only that the retained bytes are structurally adequate for exact path planning under the frozen Go 1.27.1 algorithm.

## Required ordering

The accepted direction imposes this strict sequence:

1. accept this planner design;
2. separately review the complete planner implementation diff and copied-source manifest;
3. separately authorize an isolated planner build and synthetic-only tests;
4. accept the build and test evidence;
5. separately authorize one offline planner execution against the retained lookup responses;
6. review the structural-sufficiency result and complete literal tile manifest;
7. only then prepare a tile-acquisition authorization request;
8. after separately accepted tile acquisition, prepare an offline native-verifier authorization request; and
9. keep all module-graph work behind a later gate.

No step inherits authority from an earlier step. Approval of this document would authorize planning decisions only.

## Non-verifier boundary

The planner must not:

- receive, embed, open, or use the `sum.golang.org` verifier key;
- call `note.NewVerifier`, `note.Open`, Ed25519 verification, or any equivalent signature operation;
- calculate whether a retained note signature is valid;
- read a checksum tile or calculate a Merkle root from tile bytes;
- compare a calculated record hash, tree hash, or tile hash with a retained value;
- instantiate `sumdb.Client` or execute `cmd/go`;
- read from or write to a Go checksum cache;
- make any network request or start a listener;
- classify any input or output as authenticated; or
- emit a `PASS` result for checksum integrity.

The planner may parse the signed-note envelope and tree text only as untrusted syntax. Every extracted record number, tree size, root hash, signature line, and tile coordinate remains unverified until a later native-verifier gate.

## Governing inputs

The planner design is governed by:

- the accepted [R3-G2 authorization](R3-G2-GO-MODULE-GRAPH-CLOSURE-AUTHORIZATION-REQUEST.md);
- the accepted [R3-G2 incomplete evidence](r3-g2/README.md);
- the accepted [R3-G2 stop record](r3-g2/STOP-RECORD.md); and
- the accepted [checksum-integrity remediation decision](R3-G2-CHECKSUM-INTEGRITY-REMEDIATION-PROPOSAL.md).

R3-G2 remains `Incomplete`. No stack has been selected. Gate 2 and Checkpoint A remain open.

## Exact retained-input boundary

Raw inputs remain outside Git under the owner-only root:

```text
/tmp/mneme-phase3-r3-g2.l4nJHn
```

The future planner input set would contain exactly the fourteen retained files under:

```text
state/gomodcache/cache/download/sumdb/sum.golang.org/lookup/
```

Their exact paths, sizes, and SHA-256 values are recorded in `evidence/metadata-inventory.tsv`. The governing evidence files are:

| Evidence file | Bytes | SHA-256 |
|---|---:|---|
| `evidence/metadata-inventory.tsv` | 7,211 | `f474dbc5fe97266a74f32f138af583aea9175b396f95862284a1f1e96926ff20` |
| `evidence/literal-request-results.tsv` | 9,886 | `f042983b6a1b9546e7c7e4290c2b4916a82d586fd5c75875ac4cd634f3fb06ce` |
| `evidence/request-ledger.tsv` | 4,667 | `280dce056710cbd7b521ce9853393a28cd24fb3c1717603ba99fcfedd7006731` |
| `evidence/workspace-checksums.sha256` | 106 lines | `d142dcea343eef409fba750c8ef425b703dceb685d39c876b297040d2353bf8b` |
| `evidence/cache-inventory.tsv` | 108 lines | `b1032a2c4aa1e00bd836544d9bcf8c7e4180446e21a44f4c2d79467bd0fb29c2` |

Before a future planner run, a separately authorized preflight must copy—not move or modify—only the fourteen lookup files and normalized manifest rows into a fresh owner-only root, then recheck every path, size, SHA-256, owner, mode, and regular-file type. The accepted R3-G2 root remains immutable input.

No `.info`, `.mod`, ZIP, ZIP hash, module source, VCS data, tree tile, key, credential, or live response may enter the planner input root.

## Structural input contract

For each of the fourteen exact lookup responses, the planner would require and record:

| Field | Structural requirement | Trust status |
|---|---|---|
| Lookup path | Exact match to one accepted module/version lookup path | Retained identity only |
| Response bytes | Exact size and SHA-256 match to accepted evidence | Retained identity only |
| Record identifier | Canonical non-negative base-10 integer fitting signed 64-bit range | Unverified |
| Record text | Valid UTF-8, newline-terminated, no blank line inside the record body | Unverified |
| Expected module/version line | Exactly one `/go.mod h1:` line for the path/version represented by the lookup path | Unverified |
| Note text | Structurally separable from record text without byte normalization | Unverified |
| Tree marker | Literal `go.sum database tree` first line | Unverified |
| Tree size | Canonical non-negative base-10 integer fitting signed 64-bit range | Unverified |
| Tree root | One canonical base64 value decoding to exactly 32 bytes | Unverified |
| Signature envelope | At least one structurally valid signature line; all names, key-hash prefixes, and bytes retained exactly | Unverified |
| Trailing bytes | None outside the structurally accepted note envelope | Unverified |

The planner must not repair, trim, normalize, reorder, or infer a missing field. A malformed or ambiguous response makes structural sufficiency `Incomplete` and stops the run.

## Meaning of structural sufficiency

The planner may report `Structurally sufficient for literal tile planning` only if it proves all of the following without cryptographic verification:

1. all fourteen accepted lookup paths are present exactly once;
2. all fourteen input files match their accepted sizes and SHA-256 values;
3. every response has one unambiguous record body and one unambiguous signed-note envelope;
4. every expected module/version has exactly one structurally valid `/go.mod h1:` line;
5. every record identifier and tree size is canonical, bounded, and satisfies `0 <= recordID < treeSize` for its own response;
6. every tree root is exactly 32 decoded bytes;
7. every signature line is preserved and mapped to its input response, without asserting validity;
8. every distinct tree head and every response-to-head relationship is enumerated;
9. every possible native-client tree-merge and record-check state induced by any processing order of the fourteen retained responses is represented in the operation matrix;
10. the exact Go 1.27.1 tile-planning algorithm is applied to every operation with tile height 8;
11. every primary partial tile and its deterministic full-tile fallback path is literalized;
12. the output has no wildcard, path pattern, range, unresolved placeholder, duplicate row, noncanonical path, or data-tile path;
13. two clean planner runs over independently copied inputs produce byte-identical deterministic outputs; and
14. the complete output remains under the safety caps below.

This result would not prove `SI-03`, `SI-08`, `SI-09`, or any other cryptographic integrity control. It would establish only the prerequisite for later exact tile review.

## Exact algorithm source

To avoid an independently reimplemented tile-coordinate algorithm, the proposed planner would use an exact, reviewable copy of only these three non-network x/mod transparency-log source files from the verified Go archive:

| Verified source | SHA-256 |
|---|---|
| `src/cmd/vendor/golang.org/x/mod/sumdb/tlog/note.go` | `c1d9ff098f27aab7d354385795f175a4bc0f05c46e3c37f3b3e2223f44b76236` |
| `src/cmd/vendor/golang.org/x/mod/sumdb/tlog/tile.go` | `2eb6a68b3e9f39a2926b201c0813cf2c67a1465aabc4bd88fcb310437e16bc6a` |
| `src/cmd/vendor/golang.org/x/mod/sumdb/tlog/tlog.go` | `c4bb27943a3ec8ea08ae2e0325259dc2707132ab7295d16bd3d238ba699ec628` |

The source version recorded by the verified toolchain is:

```text
golang.org/x/mod v0.36.1-0.20260813213634-8569e2639ca1
```

The exact bundled BSD 3-Clause license has SHA-256:

```text
911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad
```

No `sumdb/client.go`, cryptographic `sumdb/note` package, external module, module ZIP, or network dependency would be copied. A future implementation review must reject any copied file whose bytes differ from these accepted hashes. This copied algorithm is experimental evidence tooling and does not select a product implementation stack.

## Proposed planner implementation boundary

A later implementation proposal may add only a planner-specific tree under:

```text
experiments/phase-3/r3-g2-tile-planner/
├── README.md
├── LICENSES/
│   └── golang.org-x-mod-BSD-3-Clause.txt
├── cmd/
│   └── mneme-r3-g2-tile-plan/
│       └── main.go
├── internal/
│   └── tlog/
│       ├── note.go
│       ├── tile.go
│       └── tlog.go
├── go.mod
└── testdata/
    └── synthetic/
```

This layout is proposed, not created. It would have these limits:

- one local Go module with no `require` directive and no `go.sum`;
- standard library plus the three exact copied tlog files only;
- no network package import in planner-owned source;
- no cryptographic note-verification package or verifier key;
- no external service, listener, database, fixture from real correspondence, or candidate application code;
- no install step or write outside a fresh disposable planner root and the reviewed experiment tree; and
- no product-runtime dependency or stack-selection implication.

Any implementation diff, including copied source and license text, requires separate review before build or execution.

## Planning mechanism

### 1. Strict structural parse

Planner-owned code would parse each lookup response byte-for-byte into:

- accepted input ID and lookup path;
- record ID;
- exact record text span and SHA-256;
- exact signed-note span and SHA-256;
- unverified tree size and root bytes;
- exact signature-envelope lines; and
- expected module/version `/go.mod` line.

The parser would not expose the verifier key as an input flag. It would not contain an Ed25519 operation. Its output would label every extracted field `UNVERIFIED_STRUCTURAL_INPUT`.

### 2. Distinct-head inventory

Tree heads would be deduplicated only by the tuple `(treeSize, rootBytes)`. Every original response and exact signed-note hash would remain linked to its head. Equal-size heads with different roots would remain separate and be flagged `POSSIBLE_FORK_OR_UNVERIFIED_VARIANT`; the planner would not choose between them.

### 3. Order-complete operation matrix

The planner would model every state the native Go 1.27.1 sumdb client could reach when the fourteen retained responses are processed in any order.

It would create:

- one tree-consistency operation for every unordered pair of distinct retained heads, using the smaller tree as `older` and the larger tree as `newer`;
- one equal-size consistency operation for every equal-size/different-root head pair;
- one record-check operation for each response under its own head; and
- one additional record-check operation for each response under every retained head whose tree size is greater than or equal to that response's own tree size.

This is a conservative order-complete set. A response can be checked under its own head or a previously accepted later head; it cannot legitimately require a head smaller than the one embedded in that response after the client's merge step.

The initial empty tree adds no tile path. Identical operations are deduplicated only after their origin relationships are retained.

### 4. Exact native tile planning

For each operation, the planner would call the exact copied tlog algorithm with tile height 8 and a recording-only `TileReader`:

- a record-check operation calls `TileHashReader(head, recorder).ReadHashes` for `StoredHashIndex(0, recordID)`;
- a tree-consistency operation calls `TreeHash(olderSize, TileHashReader(newerHead, recorder))`.

The recording reader would receive the complete tile slice calculated by `TileHashReader.ReadHashes`, record every `Tile.Path()` and width, and then return the unique sentinel error:

```text
MNEME_PLAN_ONLY_TILE_CAPTURE
```

The planner would require that sentinel for every operation. It would return no tile bytes, calculate no authenticated hash, call no `SaveTiles`, and allow no operation to reach a success result. A panic, non-sentinel error, attempted save, or unexpected return is a stop.

This mechanism uses the same path-planning code as the later native client while preventing the planner from becoming a verifier.

### 5. Partial/full path closure

For every planned partial tile with width less than 256, the planner would emit:

- the exact canonical partial path as `PRIMARY`; and
- the exact corresponding width-256 path as `FULL_FALLBACK_CANDIDATE`.

Both paths would be visible for review. This accounts for the native client's deterministic full-tile fallback after a missing partial tile. The manifest would not authorize either request or define fallback behavior; the later acquisition proposal must decide which literal paths, statuses, and stop conditions to authorize.

No `/tile/8/data/...` path is expected because retained lookup responses supply record text and the later client needs hash tiles only. Any data-tile path is a planner stop.

### 6. Deterministic closure

The planner would sort normalized outputs by raw UTF-8 byte order using stable field ordering and LF line endings. Deterministic files would contain no timestamp, hostname, temporary root, process ID, random value, or environment-dependent absolute path. Run-specific metadata would be isolated in a separate non-comparison file.

Two fresh runs would be required to produce byte-identical hashes for every deterministic output. A mismatch makes the result `Incomplete`.

## Proposed future command surface

Every command below is illustrative of the exact future boundary and remains prohibited until separate approval. A later authorization must replace `<planner-root>`, `<input-root>`, and `<output-root>` with validated literal paths.

Build commands:

```text
<planner-root>/toolchain/go/bin/go version
<planner-root>/toolchain/go/bin/go env -json GOROOT GOPATH GOMODCACHE GOCACHE GOTMPDIR GOENV GOTOOLCHAIN GOWORK GOPROXY GOSUMDB GOPRIVATE GONOPROXY GONOSUMDB GOVCS GOAUTH CGO_ENABLED GOOS GOARCH GOVERSION
<planner-root>/toolchain/go/bin/go build -mod=readonly -trimpath -buildvcs=false -o <planner-root>/bin/mneme-r3-g2-tile-plan ./cmd/mneme-r3-g2-tile-plan
```

Planner command:

```text
<planner-root>/bin/mneme-r3-g2-tile-plan --mode plan --input-manifest <input-root>/lookup-inputs.tsv --input-root <input-root>/lookups --tile-height 8 --max-inputs 14 --max-heads 14 --max-operations 400 --max-literal-paths 4096 --output-root <output-root>
```

The isolated build environment would set `GOPROXY=off`, `GOSUMDB=off`, `GOVCS=*:off`, `GOAUTH=off`, `GOTOOLCHAIN=local`, `GOENV=off`, `GOWORK=off`, `CGO_ENABLED=0`, use only root-contained Go paths, and deny external networking. `GOSUMDB=off` here would apply only to a no-dependency local planner build; it would never apply to checksum verification.

No `go test`, planner build, or planner execution is authorized by this document. Exact source files, test commands, binary hash expectations, and root paths must be supplied in later gates.

## Safety caps

| Resource | Hard cap | Stop behavior |
|---|---:|---|
| Lookup inputs | 14 | Stop on any missing, duplicate, or fifteenth input |
| Bytes per lookup | Exact accepted size; never more than 1,024 | Stop before parse |
| Distinct tree heads | 14 | Stop without truncation |
| Operation rows | 400 | Stop without output promotion |
| Unique primary plus fallback paths | 4,096 | Stop without output promotion |
| Tile height | Exactly 8 | Stop on change |
| Tile level | 0 through 63 | Stop on other value |
| Tile width | 1 through 256 | Stop on other value |
| Expected bytes per tile | `width * 32`, maximum 8,192 | Stop on overflow or mismatch |
| Planner processes | 1 | Stop on child process or helper execution |
| Network requests/listeners | 0 | Stop and preserve evidence |

The caps are safety boundaries, not evidence that the expected output will approach them. Exceeding a cap is a review event, not permission to increase it during execution.

## Required planner outputs

The future planner would write only normalized planning evidence:

| Output | Required content |
|---|---|
| `planner-inputs.tsv` | Exact source IDs, relative paths, sizes, hashes, and accepted-manifest reconciliation |
| `response-structure.jsonl` | Record spans, note spans, module/version line, unverified tree fields, signature-envelope inventory, and parse result |
| `tree-heads.tsv` | Stable head IDs, sizes, root bytes, note hashes, source responses, and variant flags |
| `operation-matrix.tsv` | Every merge and record operation, its possible-order rationale, head, record, and expected sentinel result |
| `tile-origins.tsv` | Every operation-to-tile relationship before deduplication |
| `literal-tile-manifest.tsv` | One row per canonical primary or full-fallback path with tile coordinates, width, expected bytes, roles, and origin count |
| `structural-sufficiency.json` | `PASS` or `INCOMPLETE`, all condition results, counts, and no cryptographic claim |
| `planner-source-manifest.tsv` | Planner and copied-source paths, versions, sizes, hashes, and licenses |
| `determinism-checks.sha256` | Hashes from two clean runs and exact comparison result |
| `negative-inventory.json` | Zero verifier keys, signature checks, tile inputs, network actions, caches, graph commands, and `go.sum` files |
| `stop-register.md` | Every anomaly, uncertainty, cap event, and rejected continuation |

`literal-tile-manifest.tsv` must contain literal paths only. It must not contain a regular expression, glob, path prefix authorization, URL template, range, or unresolved value.

## Literal manifest schema

Each manifest row would contain, in this exact field order:

```text
manifest_id
path
role
tile_height
tile_level
tile_number
tile_width
expected_bytes
primary_path
origin_count
origin_ids_sha256
```

Rules:

- `path` begins with `/tile/8/` and exactly equals the copied tlog implementation's `Tile.Path()` with a leading slash;
- `role` is `PRIMARY` or `FULL_FALLBACK_CANDIDATE`;
- `tile_height` is `8`;
- `tile_width` is 1–256 and `expected_bytes` is exactly `tile_width * 32`;
- a primary full tile names itself in `primary_path`;
- a fallback row names the partial path that caused it;
- origins are retained in `tile-origins.tsv`; the manifest records their deterministic count and hash; and
- duplicate literal paths collapse to one row without losing origin evidence.

The later acquisition request must reproduce this table verbatim and explicitly choose which rows, if any, receive network authority.

## Synthetic-only test design

A later implementation review must provide synthetic tests that cover:

- one-record and power-of-two trees;
- partial edge tiles and deterministic full fallback paths;
- multiple records sharing tiles;
- multiple distinct tree sizes;
- equal-size/equal-root and equal-size/different-root heads;
- every input ordering for a small synthetic response set;
- malformed record identifiers and tree sizes;
- invalid UTF-8, blank lines, missing terminators, malformed base64, and wrong root length;
- missing, duplicate, unexpected, oversized, or symlinked input files;
- path canonicalization and large tile-number `xNNN/` segments;
- safety-cap exhaustion;
- the required sentinel and forbidden `SaveTiles` path;
- deterministic output across two fresh roots; and
- proof that no network, key, verifier, cache, `go.sum`, module payload, or graph command is used.

Synthetic tests must not contain a real retained lookup response, a real correspondence item, a live sumdb response, or a production credential. Test execution is not authorized by this proposal.

## Specialist reviews required before implementation approval

| Review function | Required finding |
|---|---|
| Preservation / provenance | Retained inputs remain byte-identical and immutable; copied inputs and deterministic outputs have complete manifests |
| Security / privacy | Parser limits, owner-only roots, symlink defenses, no-network enforcement, no child process, and hostile-input handling fail closed |
| Supply chain / maintenance | Only the exact three copied tlog files and standard library are used; source hashes, version, compiler, and license are complete |
| Licensing / cost | BSD 3-Clause obligations are preserved; no account, paid service, or external acquisition is introduced |
| Quality / independent verification | Operation closure, partial/full fallback logic, sentinel behavior, negative cases, and determinism are independently checked |
| Architecture / portability | Planner remains experimental evidence tooling and creates no product-stack or production-runtime dependency |
| Orchestrator / governance | Planner, manifest review, acquisition, verifier, and graph gates remain separate with exact stop conditions |

Any disagreement remains explicit and blocks implementation or execution.

## Stop conditions

A later planner stage must stop without retry, repair, substitution, or cap increase if:

- a retained root, sentinel, input path, owner, mode, type, size, or hash differs from accepted evidence;
- any input is missing, duplicated, symlinked, non-regular, oversized, or outside the validated root;
- structural parsing is ambiguous or requires byte normalization;
- a record ID, tree size, tree root, signature envelope, or expected `/go.mod` line is missing or malformed;
- the operation matrix cannot cover every possible retained-response processing order;
- copied tlog source or license bytes differ from accepted hashes;
- the planner requests or reads a key, tile, network resource, checksum cache, user configuration, or external dependency;
- a derivation does not end with `MNEME_PLAN_ONLY_TILE_CAPTURE`;
- `SaveTiles`, a hash-authentication result, a child process, or a listener occurs;
- a path is noncanonical, unresolved, outside `/tile/8/`, or is a data-tile path;
- an output or safety cap is exceeded;
- the two clean runs differ; or
- any build, test, verifier, graph, module, R3-O1, or later-stage action is attempted outside its explicit gate.

Partial outputs remain owner-only, are labeled `UNVERIFIED` and `INCOMPLETE`, and are not promoted into an acquisition manifest.

## Rollback and retention

Any future planner work would occur under a new `mktemp` owner-only root with a planner-specific sentinel. It must not modify the accepted R3-G1 or R3-G2 roots.

On interruption or rejection:

1. deny external networking and confirm zero listener or child process;
2. label every output unverified and incomplete;
3. inventory and retain only the bounded evidence needed for review;
4. do not retry, rerun, broaden a cap, or switch algorithms; and
5. wait for explicit cleanup or remediation authority.

Any later cleanup must validate the exact realpath, owner, mode, sentinel, non-symlink, non-mount, process/open-file state, and inventory before removing only that disposable planner root. No broad cache cleanup, Git reset, package uninstall, or wildcard deletion is permitted.

## Staged approval gates

| Gate | Decision | What remains prohibited after approval |
|---|---|---|
| `P1` Planner design | Accepted 2026-09-18 as a planning decision only | Source creation, build, tests, retained-input execution, network, verifier |
| `P2` Implementation diff | Review exact planner source, copied tlog files, license, manifests, and test fixtures | Build, tests, retained-input execution, network, verifier |
| `P3` Synthetic build/test | Authorize exact offline build and synthetic tests | Retained inputs, network, verifier, tiles, graph |
| `P4` Build/test evidence | Accept binary, SBOM/license, tests, and no-network evidence; authorize one retained-input planner run only | Network, tile acquisition, verifier, graph |
| `P5` Planner evidence | Accept structural sufficiency and the complete literal manifest | Network, tile acquisition, verifier, graph |
| `P6` Tile acquisition proposal | Review exact manifest rows, commands, hosts, paths, and evidence controls | Acquisition until separately authorized; verifier and graph remain blocked |

No combined approval may silently skip a gate. Native checksum verification requires a later gate not defined as execution authority here. Module-graph work remains later still.

## Explicit non-authorization

This accepted planner-design document does not authorize:

- creating planner source, copied tlog files, a Go module, synthetic fixtures, tests, dependency files, binaries, SBOMs, license reports, or generated artifacts;
- copying retained lookup responses into a new root;
- building, testing, installing, or executing the planner;
- reading or using the sumdb verifier key;
- running a signature, tree, record, tile, or Merkle verifier;
- contacting `sum.golang.org`, `proxy.golang.org`, or any other host;
- retrying the fourteen lookup requests;
- changing the allowlist, acquisition manifest, network policy, or retained cache;
- acquiring a checksum tile, lookup, module ZIP, ZIP hash, source tree, dependency, or external verifier;
- starting a service or listener;
- running any Go command, including `go version`, `go env`, `go build`, `go test`, `go list`, or `go mod graph`;
- creating or modifying `go.sum`;
- beginning R3-O1, R4, Checkpoint B, prototype work, deployment, account access, real-data work, cloud AI, or stack selection;
- committing any later implementation, authorization, evidence, or generated artifact without its own review and authorization; or
- pushing.

## Accepted planning decision

The review accepted:

1. the strict separation between structural planning and cryptographic verification;
2. the proof that the retained responses must be structurally sufficient before any verifier runs;
3. the order-complete operation matrix covering every retained-head merge and possible record-check head;
4. reuse of the exact bundled Go 1.27.1 tlog path-planning code through a recording reader that always returns the planning sentinel;
5. inclusion of deterministic full-tile fallback candidates for every partial tile;
6. the proposed experiment layout, command surface, safety caps, outputs, tests, and seven specialist reviews; and
7. the six staged gates that keep implementation, planner execution, acquisition, native verification, and graph work separate.

Acceptance closes only the `P1` planner-design gate. Until a later gate separately authorizes implementation, this document remains a planning decision only. R3-G2 remains `Incomplete`; no retained input has been read by a planner, no literal tile path has been approved or acquired, and no planner or verifier has run.
