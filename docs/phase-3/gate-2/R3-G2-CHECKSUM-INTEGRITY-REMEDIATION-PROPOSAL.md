# R3-G2 Checksum-Database Integrity Remediation Proposal

**Status:** Accepted
**Proposal date:** 2026-09-18
**Review date:** 2026-09-18
**Authority:** Accepted planning decision only. Route B—offline native verification using the retained lookup responses—is the selected design direction, subject to a separately reviewed planner and literal tile manifest. No planner, acquisition, verifier, graph, or later-stage execution is authorized.
**Predecessor result:** R3-G2 `Incomplete`
**Predecessor stop:** `SUMDB_CACHE_TRUST_CHAIN_AMBIGUITY`

## Purpose

This proposal compares bounded routes for proving both parts of Go checksum-database integrity for the fourteen retained R3-G2 lookup responses:

1. the tree head embedded in each lookup response is signed by the accepted `sum.golang.org` key; and
2. the lookup record is included in that signed tree through a valid Merkle proof reconstructed from authenticated transparency-log tiles.

This accepted planning decision selects the offline native file route as the direction for further design. It records the trust roots, verifier, network paths, commands, artifacts, uncertainties, and staged review gates that would be required before any later authorization could be considered. The planner must account for previously unknown tile paths and prove that the retained responses are structurally sufficient to derive a complete literal tile manifest before any verifier runs.

## Current state

The accepted [R3-G2 evidence](r3-g2/README.md) establishes:

- a verified and confined Go 1.27.1 macOS arm64 toolchain;
- fourteen exact `.info`, fourteen exact `.mod`, and fourteen exact sumdb lookup responses;
- complete byte-count, SHA-256, response, and request-ledger evidence for those 42 objects;
- zero checksum-tile requests;
- no `go list`, `go mod graph`, `go.sum`, build, test, or module ZIP/source acquisition; and
- a correct fail-closed stop before the unproved lookup responses could be treated as authenticated sumdb evidence.

The retained lookup responses are inputs to remediation analysis. Their HTTPS transport and recorded SHA-256 values prove retained-byte identity, not publisher identity, signed-tree validity, or Merkle inclusion.

## Governing integrity contract

A route is eligible only if it can produce reviewable evidence for all of the following:

| ID | Required proof |
|---|---|
| `SI-01` | The verifier key is the exact accepted trust root and its provenance is recorded |
| `SI-02` | Every lookup response is parsed without normalization or silent truncation |
| `SI-03` | Every embedded tree note has a valid Ed25519 signature under that trust root |
| `SI-04` | Every tree size and root hash is recorded exactly |
| `SI-05` | Every lookup record number and record body is recorded exactly |
| `SI-06` | The exact required tile coordinates are derived and frozen before external tile acquisition |
| `SI-07` | Every acquired tile is byte-counted, hashed, path-bound, and retained before use |
| `SI-08` | The verifier recomputes the relevant Merkle path and authenticates the record hash against the signed root |
| `SI-09` | Inconsistent tree heads, malformed notes, missing tiles, wrong tile lengths, hash mismatches, forks, and unexpected paths fail closed |
| `SI-10` | Authenticated and unauthenticated cache areas are separate and cannot be confused |
| `SI-11` | Network closure and an offline repeat produce the same verification result |
| `SI-12` | Verification evidence is independently reproducible from retained bytes, approved source, and exact commands |

Passing these controls would prove the retained lookup records only. It would not by itself close the module graph, create an accepted `go.sum`, authorize `go list` or `go mod graph`, acquire module ZIP/source payloads, pass Gate 2, or select a stack.

## Exact shared trust roots

All routes except the deferred route would require explicit approval of these roots:

| Trust item | Exact value | Current evidence |
|---|---|---|
| Go archive | `go1.27.1.darwin-arm64.tar.gz` | 68,100,347 bytes; SHA-256 `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Executed Go binary | `go version go1.27.1 darwin/arm64` | SHA-256 `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598` |
| Sumdb verifier key | `sum.golang.org+033de0ae+Ac4zctda0e5eza+HJyk9SxEdh+s3Ux18htTTAD8OuAn8` | Embedded in the verified toolchain at `src/cmd/go/internal/modfetch/key.go` |
| Key algorithm | Ed25519, algorithm identifier 1 | Verified toolchain `golang.org/x/mod/sumdb/note` source |
| Key name | `sum.golang.org` | Encoded in the verifier key |
| Key hash | `033de0ae` | Encoded in the verifier key and checked by `note.NewVerifier` |

The exact embedded-key source file has SHA-256 `f692a48e918dfd0647cb8b660a706dd14e44b5ad75d490a2d242b8a4b990178e`.

Approval of a route must state whether the verified Go archive is sufficient provenance for the embedded key or whether a second, independent publisher source for the key is required. That provenance choice is unresolved and may not be silently assumed.

## Verified local primary evidence

The following implementation evidence is already present inside the verified Go archive and was inspected read-only after the R3-G2 stop:

| Component | Version or SHA-256 | Relevant behavior |
|---|---|---|
| Bundled `golang.org/x/mod` | `v0.36.1-0.20260813213634-8569e2639ca1` | Exact version named in `src/cmd/vendor/modules.txt` |
| `sumdb/client.go` | `ef2e76d302bfaee7ab1dd8240600090e5fb691b0d9914e5a748c375019e07163` | Verifies tree notes, tree consistency, records, and tiles before cache promotion |
| `sumdb/note/note.go` | `5d0612c1993bff1951f782b5965490a82be4872065919963e5ce1313d12f9945` | Parses the verifier key and verifies Ed25519 note signatures |
| `sumdb/tlog/note.go` | `c1d9ff098f27aab7d354385795f175a4bc0f05c46e3c37f3b3e2223f44b76236` | Parses record identifiers, record bodies, and tree descriptions |
| `sumdb/tlog/tile.go` | `2eb6a68b3e9f39a2926b201c0813cf2c67a1465aabc4bd88fcb310437e16bc6a` | Derives tile coordinates and authenticates tile hashes against a tree root |
| `sumdb/tlog/tlog.go` | `c4bb27943a3ec8ea08ae2e0325259dc2707132ab7295d16bd3d238ba699ec628` | Transparency-log record and node hashing |
| Bundled x/mod license | SHA-256 `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad` | BSD 3-Clause text retained in the verified archive |

The native client reads lookup and tile objects through `sumdb.ClientOps`, verifies the signed tree note, checks tree consistency, obtains the stored record hash through a tile reader, compares that hash with the lookup record body, and only then writes newly fetched objects into its cache. A cached lookup is still parsed and checked. Tile data is authenticated against the signed root by the tile hash reader before newly fetched tiles are saved.

This source evidence corrects one possible overstatement in the stop rationale: manually placing a lookup response in the lookup cache does not automatically make the Go client trust its contents. The accepted stop remains correct because no verifier was actually run and no tiles existed; authentication was therefore not proved.

## Shared retained lookup paths

The fourteen retained lookup objects correspond exactly to:

```text
/lookup/github.com/jackc/pgx/v5@v5.11.0
/lookup/github.com/jackc/pgpassfile@v1.0.0
/lookup/github.com/jackc/pgservicefile@v0.0.0-20240606120523-5a60cdf6a761
/lookup/github.com/jackc/puddle/v2@v2.2.2
/lookup/golang.org/x/sync@v0.17.0
/lookup/golang.org/x/text@v0.29.0
/lookup/github.com/stretchr/testify@v1.11.1
/lookup/github.com/davecgh/go-spew@v1.1.1
/lookup/github.com/kr/pretty@v0.3.0
/lookup/github.com/pmezard/go-difflib@v1.0.0
/lookup/gopkg.in/check.v1@v1.0.0-20201130134442-10cb98267c6c
/lookup/gopkg.in/yaml.v3@v3.0.1
/lookup/golang.org/x/tools@v0.36.0
/lookup/golang.org/x/mod@v0.27.0
```

No remediation route may reinterpret these as already authenticated. Any route that repeats them over the network must identify the repeat as a new, separately approved acquisition rather than a continuation or retry under the closed R3-G2 authorization.

## Exact tile-path rule

The Go 1.27.1 client uses tile height 8 by default. Candidate tile paths have one of these canonical forms:

```text
/tile/8/<level>/<zero-padded-tile-number>
/tile/8/<level>/<zero-padded-tile-number>.p/<partial-width>
```

Large tile numbers may contain canonical `xNNN/` path segments. A native client may request a full tile after a missing partial tile. Therefore a path-pattern allowlist or a numerical cap is not an exact path manifest.

Before any future tile GET, an approved planner must emit a literal table containing every permitted path, expected relationship to a specific signed tree and record, partial/full status, and request count. That table must receive its own review. Any route that cannot freeze a literal tile table before acquisition is ineligible under this proposal.

If a later gate authorizes tile acquisition, every approved manifest row would use one direct HTTPS request with this exact argv shape after all placeholders are replaced by validated literal values:

```text
/usr/bin/curl --fail --silent --show-error --proto '=https' --tlsv1.2 --max-redirs 0 --retry 0 --noproxy '*' --connect-timeout 30 --max-time 300 --max-filesize 8192 --request GET --dump-header <root>/evidence/headers/<sequence>.txt --output <root>/downloads/tiles/<sequence>.partial --write-out '%{json}\n' https://sum.golang.org<literal-approved-tile-path> > <root>/evidence/transfers/<sequence>.json
/usr/bin/wc -c <root>/downloads/tiles/<sequence>.partial
/usr/bin/shasum -a 256 <root>/downloads/tiles/<sequence>.partial
```

The transfer would use neither range nor resume flags. The partial file would be renamed to its immutable final path only after status, effective URL, host, redirect count, byte count, and SHA-256 checks pass. The exact sequence numbers, paths, destinations, expected request count, timeouts, client version/hash, and independent post-transfer checks must be frozen in the acquisition authorization; this proposal does not do so.

## Shared future execution environment

Any later Go or helper execution would use a fresh owner-only remediation root and an empty process environment populated only with reviewed values. At minimum:

| Variable | Required future value |
|---|---|
| `PATH` | `/usr/bin:/bin` for system evidence tools; the Go binary is always invoked by absolute path |
| `GOROOT` | `<root>/toolchain/go` |
| `GOPATH` | `<root>/state/gopath` |
| `GOMODCACHE` | `<root>/state/gomodcache` |
| `GOCACHE` | `<root>/state/go-build-cache` |
| `GOTMPDIR` | `<root>/state/go-tmp` |
| `GOENV` | `off` |
| `GOTOOLCHAIN` | `local` |
| `GOWORK` | `off` |
| `GOPROXY` | Route-specific reviewed `file://` root or `off`; never `direct` or a fallback list |
| `GOSUMDB` | Exact key plus route-specific reviewed direct or `file://` URL |
| `GOPRIVATE` | Empty |
| `GONOPROXY` | `none` |
| `GONOSUMDB` | Empty |
| `GOVCS` | `*:off` |
| `GOAUTH` | `off` |
| `CGO_ENABLED` | `0` |
| Proxy variables | Unset |

No user or system Go cache, persistent Go environment file, shell profile, netrc, Git configuration, credential helper, keychain, package-manager state, or global installation may participate. Route-specific authorization must replace every `<root>` and other placeholder with a validated literal before execution.

## Route comparison

| Route | Verifier | New external requests | New code/service | Principal advantage | Principal concern | Current finding |
|---|---|---:|---|---|---|---|
| `A` Native direct | Accepted Go 1.27.1 `cmd/go` | 14 repeated lookups plus dynamically requested tiles | None, unless a path guard is needed | Smallest verifier trust base | A new lookup can carry a new tree head, so its literal tile set cannot be frozen before the client immediately requests tiles | Ineligible under the exact-path rule |
| `B` Native offline file route | Accepted Go 1.27.1 `cmd/go` | Exact approved tiles only | Tile planner required; no service required for verification | Reuses retained lookups; verification can be network-disconnected | Exact tile planning must be solved first | Selected direction for design only; execution remains gated |
| `C` Bundled-library verifier | Reviewed helper using x/mod bundled in accepted Go archive | Exact approved tiles only | New helper source and build | Strongest explicit request/proof evidence; no lookup repeat | Adds code, build, tests, and a larger review surface | Conditional |
| `D` Loopback replay | Accepted Go 1.27.1 `cmd/go` | Exact approved tiles only | Local replay service and listener | Native verifier with complete request logging | Service/listener lifecycle and replay correctness | Conditional but higher complexity |
| `E` External verifier | Separately acquired upstream x/mod-based helper | At least verifier source plus exact approved tiles | New dependency and helper | Independence from bundled implementation is possible | Integrity bootstrap is circular without an independent source trust root | Blocked |
| `F` Defer | None | 0 | None | Preserves current boundary | R3-G2 remains incomplete | Always available |

Route B is selected only as the accepted direction for further planning. No planner, tile path, acquisition, verifier command, graph command, or later-stage action is selected or authorized by that decision.

## Route A — native direct verification

### Boundary

Route A would use the accepted Go binary as the verifier, a fresh empty checksum cache, a local read-only file proxy for the retained `.info` and `.mod` objects, and a direct `sum.golang.org` URL specified explicitly in `GOSUMDB`.

It would not reuse the retained lookup files. The native client would request the fourteen lookup paths again under a new authorization, verify their signed tree notes, request only a separately approved literal tile set, authenticate each record, and then repeat the result offline.

That boundary cannot currently be implemented as written. A repeated live lookup may carry a tree head newer than the retained response, changing the required tile coordinates. The native client proceeds from lookup to tile reads within the same operation, before a new literal tile table can be reviewed. Pausing or interposing on that transition requires a path-enforcement or replay component and therefore becomes Route D, not a direct route.

### Exact trust roots and verifier

- archive, binary, and verifier key: the exact shared roots above;
- verifier: Go 1.27.1 `cmd/go`, binary SHA-256 `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598`;
- sumdb implementation: bundled x/mod `v0.36.1-0.20260813213634-8569e2639ca1`.

### Network paths

- host: `sum.golang.org` only;
- fourteen exact lookup paths: the shared list above, each at most once under the new route;
- tiles: only the literal paths in a separately approved tile manifest;
- forbidden: `/latest`, direct record-number paths, proxy sumdb support checks, query strings, all other hosts and paths.

The environment must use the explicit two-field value:

```text
GOSUMDB=sum.golang.org+033de0ae+Ac4zctda0e5eza+HJyk9SxEdh+s3Ux18htTTAD8OuAn8 https://sum.golang.org
```

The explicit URL prevents the Go client from probing `proxy.golang.org/sumdb/sum.golang.org/supported`. `GOPROXY` would point to a reviewed local `file://` tree containing only the accepted `.info` and `.mod` files.

### Required command argv

After a future authorization resolves `<root>` to a fresh validated owner-only path, the only Go verifier commands would be:

```text
<root>/toolchain/go/bin/go version
<root>/toolchain/go/bin/go env -json GOROOT GOPATH GOMODCACHE GOCACHE GOTMPDIR GOENV GOTOOLCHAIN GOWORK GOPROXY GOSUMDB GOPRIVATE GONOPROXY GONOSUMDB GOVCS GOAUTH CGO_ENABLED GOOS GOARCH GOVERSION
<root>/toolchain/go/bin/go list -mod=mod -m -json all
<root>/toolchain/go/bin/go mod graph
<root>/toolchain/go/bin/go list -mod=readonly -m -json all
<root>/toolchain/go/bin/go mod graph
```

The final two commands would run only after external network denial, with the authenticated cache retained and `GOPROXY=off`. These commands are listed for route comparison only and remain prohibited.

### Required artifacts

- fresh-root sentinel and full environment record;
- exact local proxy manifest and checksums;
- request/response ledger for fourteen lookup and every tile request;
- signed tree notes, literal tile manifest, tile bytes, sizes, and hashes;
- native client's latest-tree configuration and separated pre-/post-verification cache inventories;
- authenticated record results and failure-injection results;
- online/offline output reconciliation; and
- proof that no ZIP, source, VCS, build, test, or undeclared path was used.

### Route-specific gates

1. `A1` — approve repeating the fourteen lookup requests as a new acquisition and accept the exact trust root.
2. `A2` — approve a mechanism that freezes and enforces literal tile paths and blocks redirects, retries, credential fallback, and full-tile fallback outside the manifest.
3. `A3` — approve the final literal lookup/tile table and acquisition command.
4. `A4` — accept acquisition evidence before any graph command.
5. `A5` — authorize native verification and offline repeat.
6. `A6` — accept integrity evidence; graph closure remains separately gated.

### Unresolved concern

The native HTTP client can follow redirects and may make a second credential attempt after a 4xx response. The sumdb client may request a full tile after a missing partial tile. More fundamentally, a new tree head prevents advance approval of its literal tile set. Route A is ineligible under the current exact-path contract. A reviewed interposition design would be evaluated as Route D; merely inspecting the final cache is insufficient network evidence.

## Route B — native verification from an offline file source

### Boundary

Route B would preserve the fourteen retained lookup bytes, acquire only a precomputed exact tile set in a separately approved step, disconnect external networking, and then run the accepted Go binary against an immutable `file://` sumdb tree. Go's own sumdb client would perform signature, tree-consistency, tile, and record verification without a local service or external request.

Route B separates planning and acquisition from verification:

1. structurally parse the retained responses as explicitly untrusted planner inputs, without checking a signature or running a verifier;
2. prove that every response contains the complete record, note envelope, tree-size, tree-root, and signature fields needed to derive all possible native-client tile reads;
3. derive and review a conservative exact tile manifest that accounts for every retained record/tree-head ordering and any previously unknown path;
4. acquire only those literal tile paths under a later authorization;
5. close networking and assemble a read-only file tree;
6. run native signature, tree-consistency, tile, and record verification with a fresh cache; and
7. rerun from retained authenticated state offline.

### Exact trust roots and verifier

The exact shared Go archive, Go binary, embedded key, and bundled x/mod version apply to the later verifier stage. The planner does not use the key or make a cryptographic trust decision. The verifier is the accepted Go 1.27.1 binary, not the planner. Planner output is untrusted until the native client independently completes verification.

### Network paths

- lookup requests: none; use the fourteen retained lookup bytes by exact recorded SHA-256;
- tile host: `sum.golang.org` only;
- tile requests: only the literal paths in the separately reviewed planner output;
- all proxy, lookup, `/latest`, record-number, query-string, redirect, retry, and other-host requests: forbidden.

The exact verification source would be:

```text
GOSUMDB=sum.golang.org+033de0ae+Ac4zctda0e5eza+HJyk9SxEdh+s3Ux18htTTAD8OuAn8 file://<root>/sumdb-source
```

The Go 1.27.1 web reader supports `file://` reads directly. External networking must be denied while this value is active.

### Required command argv

The future native verification command set would be the same five Go argv forms listed under Route A. The networked acquisition command would not be a Go command; it would be a separately reviewed single-purpose HTTPS client invocation for each literal tile URL, with redirects, retries, range, resume, credentials, mirrors, and fallback disabled.

The exact planner command is unresolved. Route B cannot be authorized until the following planner subroute is accepted and its literal command is frozen:

- `B-P1`: the reviewed bundled-library helper described in Route C, in `plan` mode only.

An alternative `B-P2` native-client dry run against a read-only `file://` tree was considered and rejected as an exact planner. Without tile bytes, the client can reveal a missing path but cannot complete that proof branch and reliably enumerate all later paths. Interleaving planning and tile acquisition would violate the literal-manifest-before-acquisition requirement.

### Required artifacts

- structural parse and sufficiency results for all retained lookup responses, explicitly labeled unverified;
- exact tree sizes, root hashes, record numbers, and lookup-object hashes;
- deterministic literal tile manifest with derivation links to records and trees;
- separately accepted tile acquisition evidence;
- immutable `file://` source-tree manifest;
- fresh unauthenticated and authenticated cache inventories kept in separate paths;
- native verification transcript and explicit result for each of fourteen records;
- negative tests for altered note, lookup body, record number, tree hash, tile byte, tile truncation, and missing tile; and
- network-denied repeat evidence.

### Route-specific gates

1. `B1` — select and review the planner subroute; accept the shared trust root.
2. `B2` — authorize planner code/build or native local planning only; no acquisition or graph work.
3. `B3` — accept the exact literal tile manifest.
4. `B4` — authorize exact tile acquisition only.
5. `B5` — accept acquired tile bytes and the immutable file-tree manifest.
6. `B6` — authorize native offline verification and negative tests only.
7. `B7` — accept integrity evidence; any graph command remains separately gated.

### Preliminary fit

Route B avoids repeated lookup network requests, does not require a listener, and keeps the proof replayable from retained bytes. It is the accepted design direction. Its unresolved prerequisite is a trustworthy, separately reviewed planner that derives a complete exact tile table, accounts for paths not previously known, and demonstrates the structural sufficiency of all retained responses before any verifier runs. Route B cannot proceed until that prerequisite is explicitly approved and completed without silently expanding trust.

## Route C — purpose-built verifier from bundled x/mod source

### Boundary

Route C would copy only the required x/mod packages from the verified Go archive into a fresh review workspace, add a small Mneme-specific command implementing `sumdb.ClientOps`, and build a deterministic offline verifier with the accepted Go binary.

The helper would have two strictly separated modes:

- `plan`: structurally parse retained lookup notes without using the verifier key or checking signatures, prove that all fields required for complete path derivation are present, calculate the conservative literal tiles required for every record/tree-head ordering, and emit a manifest without external networking; and
- `verify`: read only retained lookup and acquired tile files, run the x/mod sumdb verification path, emit per-record proof results, and refuse every missing or undeclared path.

It would not calculate the module graph, write `go.sum`, import candidate code, or access a module ZIP/source tree.

### Exact trust roots and verifier

- shared archive and embedded sumdb key;
- accepted Go compiler binary SHA-256 `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598`;
- bundled x/mod version `v0.36.1-0.20260813213634-8569e2639ca1`;
- exact copied-source manifest and the source hashes listed above;
- helper source reviewed line by line and frozen by SHA-256 before build;
- built verifier accepted only after two clean builds produce the same binary hash or a documented reason explains platform nondeterminism.

### Network paths

- helper planning and verification: no network;
- separate tile acquisition: `https://sum.golang.org` plus only the approved literal tile paths;
- lookup requests: none;
- every other host and path: forbidden.

### Required command argv

The exact future command surface would be frozen in a separate helper-design record. Its proposed shape is:

```text
<root>/toolchain/go/bin/go version
<root>/toolchain/go/bin/go env -json GOROOT GOPATH GOMODCACHE GOCACHE GOTMPDIR GOENV GOTOOLCHAIN GOWORK GOPROXY GOSUMDB GOPRIVATE GONOPROXY GONOSUMDB GOVCS GOAUTH CGO_ENABLED GOOS GOARCH GOVERSION
<root>/toolchain/go/bin/go build -trimpath -buildvcs=false -o <root>/bin/mneme-sumdb-verify ./cmd/mneme-sumdb-verify
<root>/bin/mneme-sumdb-verify plan --key-file <root>/inputs/sumdb.key --lookup-manifest <root>/inputs/lookups.tsv --lookup-root <root>/inputs/lookups --output <root>/evidence/tile-plan.tsv
<root>/bin/mneme-sumdb-verify verify --key-file <root>/inputs/sumdb.key --lookup-manifest <root>/inputs/lookups.tsv --lookup-root <root>/inputs/lookups --tile-manifest <root>/inputs/tiles.tsv --tile-root <root>/inputs/tiles --output <root>/evidence/verification.jsonl
```

These command names and flags are interface requirements, not existing code. Route C would require a separate reviewed source diff, dependency manifest, build plan, and test plan before any of them could run.

### Required artifacts

- copied-source inventory with origin paths, versions, licenses, sizes, and hashes;
- helper specification, source, review record, and threat analysis;
- build environment, transcript, compiler identity, binary hash, SBOM, and license report;
- deterministic plan output with exact tile derivations;
- tile acquisition evidence from a later gate;
- per-note signature and per-record Merkle verification evidence;
- positive and mutation-based negative-test results; and
- independent comparison against the native Go client before the helper can be relied upon.

### Route-specific gates

1. `C1` — approve copying the exact bundled packages and the helper specification.
2. `C2` — accept source review, dependency closure, license report, test vectors, and exact build commands.
3. `C3` — authorize the isolated build and tests only.
4. `C4` — accept binary reproducibility and authorize offline `plan` mode.
5. `C5` — accept the exact literal tile manifest.
6. `C6` — authorize exact tile acquisition only.
7. `C7` — accept acquired tiles and authorize offline `verify` plus negative tests.
8. `C8` — accept integrity evidence after independent native-client comparison.

### Unresolved concern

This route adds experimental code, a build, tests, a binary, and an SBOM. None is currently authorized. The helper must not become a new permanent trust root merely because it uses the same library as `cmd/go`; independent native-client comparison remains mandatory.

## Route D — loopback replay into the native client

### Boundary

Route D would use the accepted Go binary as the verifier and a purpose-built read-only loopback service as a transport recorder. The service would expose only the retained lookup bytes and separately acquired approved tiles, reject every other path, emit a complete access ledger, and have no external-network capability.

The native client would use:

```text
GOSUMDB=sum.golang.org+033de0ae+Ac4zctda0e5eza+HJyk9SxEdh+s3Ux18htTTAD8OuAn8 http://127.0.0.1:<approved-port>
```

### Exact trust roots and verifier

The accepted Go binary and embedded key are the proof verifier. The replay service is not trusted for integrity, but its path mapping and byte fidelity must still be tested because omission or misrouting can affect coverage and evidence.

### Network paths

- external acquisition before replay: only exact approved `https://sum.golang.org/tile/...` URLs;
- verification: loopback host `127.0.0.1` and a single frozen port;
- replay paths: the fourteen exact lookup paths plus the approved literal tile table;
- no wildcard bind, IPv6 bind, external route, proxy, redirect, retry, `/latest`, or other path.

### Required command argv

The route would require exact future commands to:

1. build or otherwise establish the reviewed replay service;
2. start it with explicit `--bind 127.0.0.1:<approved-port>`, immutable source root, literal route manifest, and append-only log;
3. run the same native Go verifier argv as Route A;
4. stop the exact recorded service process; and
5. prove listener closure.

No command can be finalized until service source, binary hash, port, source root, and log path are frozen. Those unresolved values make Route D non-executable at this stage.

### Required artifacts

- service source/dependency/build/test package;
- route-to-file table and immutable source manifest;
- bind/listener preflight and postflight evidence;
- complete local request/response ledger;
- native verification and negative-test results; and
- proof of service termination and zero external connectivity.

### Route-specific gates

1. `D1` — approve service design, source, dependencies, exact bind, and threat model.
2. `D2` — authorize isolated build and service tests without retained R3-G2 inputs.
3. `D3` — accept service evidence and exact tile plan.
4. `D4` — authorize exact tile acquisition only.
5. `D5` — accept tiles and authorize one loopback replay session.
6. `D6` — accept native verification, listener closure, and rollback evidence.

### Preliminary fit

Route D gives excellent path observability but adds a service, listener, code, build, and lifecycle risk that Route B avoids. It should remain a fallback unless file-based verification proves inadequate.

## Route E — separately acquired external verifier

### Boundary

Route E would acquire a specific upstream `golang.org/x/mod` source release and build a separately reviewed verifier rather than copy the version bundled with Go 1.27.1.

The only version already present in the accepted fourteen-module envelope is `golang.org/x/mod@v0.27.0`. Its possible proxy objects are:

```text
https://proxy.golang.org/golang.org/x/mod/@v/v0.27.0.info
https://proxy.golang.org/golang.org/x/mod/@v/v0.27.0.mod
https://proxy.golang.org/golang.org/x/mod/@v/v0.27.0.zip
https://sum.golang.org/lookup/golang.org/x/mod@v0.27.0
```

The `.info`, `.mod`, and lookup bytes are already retained, but the ZIP/source payload is not. No request above is authorized by this proposal.

### Integrity bootstrap problem

The normal authenticity route for the module ZIP is the same sumdb trust chain that remediation is intended to establish. Using the unproved lookup response to trust the verifier source would be circular. HTTPS plus a ZIP SHA-256 calculated after download would establish retained-byte identity, not an independent publisher trust root.

Route E remains blocked unless a separate primary publisher channel supplies an exact source artifact and independently authenticated digest or signature whose trust chain does not depend on the unresolved sumdb proof. That channel, signature format, key, artifact, path, and verification command are not currently established.

### Required command and artifacts if unblocked

Before any acquisition, a later proposal would have to freeze:

- exact upstream version and artifact URL;
- exact publisher signing key or independently authenticated digest source;
- signature/digest verification command and verifier provenance;
- complete dependency graph, license set, build commands, tests, and SBOM;
- helper command interface equivalent to Route C; and
- exact tile paths and acquisition commands.

### Route-specific gates

1. `E1` — establish and accept a non-circular publisher trust root.
2. `E2` — approve exact source artifact, hosts, paths, redirects, hashes, signatures, dependencies, and licenses.
3. `E3` — authorize source acquisition only.
4. `E4` — accept source integrity and authorize isolated build/tests.
5. `E5` — accept verifier evidence before any retained lookup or tile is processed.
6. Later tile and proof gates would then mirror Route C.

Until `E1` is satisfied, Route E is rejected as an executable remediation route.

## Route F — defer and preserve the incomplete result

Route F makes no request, executes no verifier, starts no service, and creates no build or graph artifact. R3-G2 remains `Incomplete`; the retained lookup responses remain unverified; the owner-only evidence roots remain preserved under their accepted retention controls.

Deferral is the default if no other route passes review. It creates no later-stage authority.

## Rejected shortcuts

The following are not remediation routes:

- treating HTTPS transport or local SHA-256 values as signed-tree or Merkle proof;
- setting `GOSUMDB=off` or adding `GONOSUMDB` exclusions;
- trusting lookup or tile files because they occupy Go's conventional cache path;
- running `go list`, `go mod graph`, or a verifier under the closed R3-G2 authorization;
- repeating a request and labeling it a retry under the old authorization;
- allowing an unreviewed redirect, mirror, proxy fallback, credential helper, VCS route, or package manager;
- acquiring a verifier whose own integrity depends on the unresolved proof;
- accepting planner output as final proof; or
- accepting a successful command exit without retained per-record and per-tile evidence.

## Required specialist reviews

Every non-deferred route requires all seven Phase-3 review functions:

| Review function | Required finding |
|---|---|
| Preservation / provenance | Inputs remain byte-identical, immutable, path-bound, exportable, and reproducible; authenticated and unverified states cannot be confused |
| Security / privacy | No accounts, credentials, telemetry, public exposure, undeclared network path, unsafe listener, cache escape, or secret-bearing log; failures close the route |
| Supply chain / maintenance | Trust roots, source versions, dependencies, toolchain, hashes, signatures, build steps, and update implications are complete |
| Licensing / cost | Source and binary licenses are recorded; no paid service, account, or distribution assumption is introduced |
| Quality / independent verification | Test vectors include valid proofs and mutations of keys, notes, records, tree heads, paths, tiles, lengths, and hashes; results are independently reproducible |
| Architecture / portability | The route does not become a hidden production dependency or imply stack selection; platform-specific controls are explicit |
| Orchestrator / governance | Every gate, command, host, path, artifact, stop condition, rollback action, and downstream boundary is explicit |

Any unresolved disagreement blocks route authorization and is recorded rather than averaged away.

## Cross-route staged approval model

No single approval may authorize the entire remediation. The minimum gate sequence is:

1. **Route gate:** select one route for further design, not execution.
2. **Trust gate:** accept exact keys, binaries, source versions, licenses, and provenance assumptions.
3. **Planner gate:** approve exact planner source/command or native planning mechanism.
4. **Tile-manifest gate:** review the complete literal tile table; patterns and caps are insufficient.
5. **Acquisition gate:** authorize only the exact tile GETs and evidence controls.
6. **Acquisition-evidence gate:** accept bytes, hashes, paths, response metadata, network closure, and cache state.
7. **Verifier gate:** authorize only the exact offline or confined verifier commands and negative tests.
8. **Integrity-evidence gate:** accept or reject signed-tree and Merkle-proof results for every record.
9. **Graph proposal gate:** only after integrity acceptance, prepare a new proposal for any `go list`, `go mod graph`, `go.sum`, or online/offline graph reconciliation.

The user may stop or defer at every gate. Approval of this proposal satisfies none of them.

## Stop conditions for any future route

A later authorized route must stop without retry or substitution if:

- the archive, binary, key, source, helper, service, manifest, or retained input differs from its approved hash;
- a trust root or publisher provenance assumption is missing or changes;
- a command, argument, environment variable, root, host, method, path, query, redirect, retry, credential, or cache differs from the approved table;
- a tile path is absent from the literal approved manifest;
- a response has the wrong status, size, hash, type, or route;
- a note signature, tree parse, tree consistency check, record hash, Merkle path, tile length, or root comparison fails;
- an authenticated cache receives data before proof succeeds;
- any external network remains available during an offline stage;
- a ZIP, ZIP hash, source payload, VCS route, fifteenth module, alternate version, build outside an approved helper build, graph command, or `go.sum` is attempted; or
- a service binds beyond an exact approved loopback endpoint or remains active after its stage.

Partial evidence is retained owner-only and labeled unverified. No automatic fallback or alternate route is permitted.

## Required evidence package

The selected route—and any later approved replacement—must return, at minimum:

1. route and gate identifiers;
2. exact trust-root table and provenance decisions;
3. source, dependency, license, command, environment, and binary inventories;
4. retained lookup manifest with byte counts and hashes;
5. distinct signed tree notes with exact signatures, tree sizes, and root hashes;
6. exact record identifiers and record-body hashes;
7. approved literal tile manifest and derivation record;
8. tile request/response evidence and immutable tile inventory;
9. per-record signature, tree, Merkle-path, and final authentication result;
10. authenticated-versus-unverified cache reconciliation;
11. negative-test matrix and results;
12. network, process, listener, open-file, and path closure evidence;
13. offline reproducibility result;
14. complete anomaly, disagreement, uncertainty, and stop registers; and
15. explicit confirmation that no graph command, `go.sum`, module payload, R3-O1, later phase, stack selection, account, real data, cloud AI, production action, commit of raw artifacts, or push occurred.

## Uncertainties and decisions required

| ID | Uncertainty | Required disposition |
|---|---|---|
| `U-G2R-01` | Whether the verified Go archive alone is sufficient provenance for the embedded `sum.golang.org` key | Accept explicitly or require an independent publisher key source before route selection |
| `U-G2R-02` | Exact literal tile coordinates have not been derived | Approve a planner route, then review its complete literal output before acquisition |
| `U-G2R-03` | Native direct HTTP behavior may exceed strict redirect/retry/path controls | Prove an enforcement mechanism or reject Route A |
| `U-G2R-04` | A purpose-built helper adds code and build trust | Require source review, dependency closure, reproducible build, mutation tests, and native-client comparison |
| `U-G2R-05` | A loopback service adds listener and lifecycle risk | Require exact bind, zero external capability, route manifest, logs, and closure proof |
| `U-G2R-06` | External x/mod source acquisition has a circular integrity bootstrap | Establish a non-sumdb publisher trust root or keep Route E blocked |
| `U-G2R-07` | Multiple lookup responses may carry different valid tree heads | Record all heads and prove consistency on one accepted timeline, not merely individual signatures |
| `U-G2R-08` | Proof success does not establish graph completeness | Keep all graph commands and graph conclusions behind a later gate |

## Explicit non-authorization

This accepted planning document does not authorize:

- executing Route B or beginning Route A, C, D, or E;
- contacting any host or making any lookup, tile, proxy, source, or verifier request;
- retrying or repeating any R3-G2 request;
- changing the allowlist, manifest, network controls, or retained cache;
- acquiring, copying, generating, compiling, installing, executing, or testing a verifier or helper;
- starting a local service or listener;
- creating a fresh Go workspace or running any Go command, including `go version`, `go env`, `go list`, `go mod graph`, `go build`, or `go test`;
- creating or modifying `go.sum`;
- acquiring a module ZIP, ZIP hash, source tree, VCS checkout, fifteenth module, or alternate version;
- beginning R3-O1, R4, Checkpoint B, a prototype, deployment, account access, real-data work, cloud AI, or stack selection;
- deleting or altering the retained R3-G1 or R3-G2 roots;
- committing any later planner, implementation, evidence, or generated artifact without its own review and authorization; or
- pushing.

## Accepted planning decision

The review accepted the following planning decisions:

1. Route B—offline native verification using the retained lookup responses—is the selected direction for design only.
2. A separately reviewed planner and complete literal checksum-tile manifest are mandatory predecessors to acquisition or verifier execution.
3. The planner must account for previously unknown tile paths and prove that the retained lookup responses contain all structural inputs needed to derive the complete manifest before any verifier runs.
4. Route A remains ineligible under the exact-path rule; Route D remains a higher-complexity fallback; Route E remains blocked by circular bootstrap.
5. The shared trust-root provenance question remains explicit and must be resolved before verifier authorization.
6. The nine-stage approval sequence continues to separate planner design, manifest review, acquisition, integrity verification, and later module-graph work.

Until a later instruction explicitly accepts and authorizes the planner's next gate, R3-G2 remains `Incomplete`; all network, planner-execution, verifier, graph, and later-stage paths remain closed. Acceptance of Route B as a planning direction is not execution authority.
