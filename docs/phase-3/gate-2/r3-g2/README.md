# R3-G2 Go Module-Graph Closure Evidence

**Evidence status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Workstream result:** Incomplete
**Stop code:** `SUMDB_CACHE_TRUST_CHAIN_AMBIGUITY`
**Authorization commit:** `ffe9359729922422952cb2c1cd95b2529f8425cf`
**Disposable root:** `/tmp/mneme-phase3-r3-g2.l4nJHn`

## Accepted conclusion

R3-G2 stopped correctly before checksum-tile acquisition and before any graph command. The fourteen `.info`, fourteen `.mod`, and fourteen checksum lookup paths were each requested exactly once and retained with complete response, byte-count, and SHA-256 evidence. The request set matched the accepted literal-path ledger, with no redirect, retry, duplicate, or byte-count mismatch.

The checksum-database integrity precondition was not proved. Manually fetched lookup responses cannot be promoted into Go's trusted checksum cache as evidence that the Go checksum client verified their signed tree heads and Merkle inclusion proofs. The retained lookup responses are therefore unverified inputs, not authenticated sumdb evidence.

Continuing would have required repeating the fourteen lookup requests through the Go client, adding an unapproved verifier, starting an unapproved local service, or weakening the accepted integrity requirement. Each route was outside the authorization. The fail-closed stop was correct, and the R3-G2 result is `Incomplete`.

## Toolchain and confinement evidence

| Control | Accepted result |
|---|---|
| Repository at execution | Clean at `ffe9359729922422952cb2c1cd95b2529f8425cf` |
| Prior matching R3-G2 root/process | None |
| Disposable root | `/tmp/mneme-phase3-r3-g2.l4nJHn` |
| Root owner/mode | UID 501; `0700` |
| Sentinel | Matching `MNEME_PHASE3_DISPOSABLE.json` present |
| R3-G1 source archive | Retained and untouched |
| Copied archive bytes | 68,100,347 |
| Copied archive SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Extraction paths | 17,353; exact match to the accepted R3-G1 inventory |
| Extracted regular files | 15,639 |
| Extracted regular-file bytes | 239,785,751 |
| Extracted links | 0 |
| Writes outside toolchain root | 0 |
| Executed identity | `go version go1.27.1 darwin/arm64` |
| Go binary SHA-256 | `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598` |

Only `go version` and the accepted `go env -json` query executed. No module-list or graph command began.

## Confined environment

| Setting | Recorded value |
|---|---|
| `GOROOT` | `/tmp/mneme-phase3-r3-g2.l4nJHn/toolchain/go` |
| `GOPATH` | `/tmp/mneme-phase3-r3-g2.l4nJHn/state/gopath` |
| `GOMODCACHE` | `/tmp/mneme-phase3-r3-g2.l4nJHn/state/gomodcache` |
| `GOCACHE` | `/tmp/mneme-phase3-r3-g2.l4nJHn/state/go-build-cache` |
| `GOTMPDIR` | `/tmp/mneme-phase3-r3-g2.l4nJHn/state/go-tmp` |
| `GOTOOLCHAIN` | `local` |
| `GOWORK` | `off` |
| `GOPROXY` | `https://proxy.golang.org` |
| `GOSUMDB` | `sum.golang.org` |
| `GONOPROXY` | `none` |
| `GOVCS` | `*:off` |
| `GOAUTH` | `off` |
| `CGO_ENABLED` | `0` |

The process environment supplied `GOENV=off`; `go env` rendered the effective `GOENV` value as empty, and no persistent Go environment file was created. `GOPRIVATE` and `GONOSUMDB` were empty. Toolchain auto-download, workspaces, VCS, authentication, CGO, and direct fallback were disabled.

## Literal request reconciliation

| Class | Planned | Completed | HTTP 200 | Redirects | Retries | Byte mismatches | Bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| Proxy `.info` | 14 | 14 | 14 | 0 | 0 | 0 | 1,859 |
| Proxy `.mod` | 14 | 14 | 14 | 0 | 0 | 0 | 2,447 |
| Sumdb lookup | 14 | 14 | 14 | 0 | 0 | 0 | 5,165 |
| **Total** | **42** | **42** | **42** | **0** | **0** | **0** | **9,471** |

The actual host/path set exactly matched the 42-row preflight ledger. Each retained object has an independent byte count, SHA-256, content type, remote address, and sanitized response metadata. No other application host was contacted. The acquisition network path was closed after the requests, and no matching acquisition or graph process, open cache file, or TCP connection remained.

## Payload and state negatives

| Prohibited state | Accepted result |
|---|---:|
| Derived checksum-tile requests | 0 |
| Module ZIPs | 0 |
| ZIP hash files | 0 |
| Extracted module source trees | 0 |
| Git/VCS requests or checkouts | 0 |
| Fifteenth-module requests | 0 |
| Alternate versions | 0 |
| `go.sum` | Not created |
| `go list` graph command | Not started |
| `go mod graph` | Not started |
| Build-cache entries | 0 |
| Go temporary entries | 0 |
| GOPATH entries | 0 |
| Builds or tests | 0 |

## Integrity stop

The accepted authorization required Go checksum-database verification of every selected module's `/go.mod` hash through signed lookup and tree evidence. The literal checksum responses were acquired by the bounded HTTPS client to satisfy the exact one-request-per-path rule. Review before the first graph command established that writing those responses to Go's expected cache paths would make them appear pretrusted; it would not prove that the client verified the note signatures and Merkle inclusion proofs.

The following continuations were rejected:

1. Repeat the fourteen lookup paths through Go, which would violate the exact request count and no-repeat rule.
2. Add a verifier or helper, which would introduce unreviewed code, dependencies, commands, and trust bootstrap.
3. Start a local interception or sumdb service, which would violate the no-service boundary and change the route.
4. Treat TLS transport and retained-object SHA-256 values as checksum-database authentication, which would weaken the accepted integrity contract.

No retry, route substitution, cache promotion, verifier execution, or service startup occurred.

## Retained evidence inventory

The owner-only temporary root retains the complete raw evidence outside Git, including:

- the 42-row predeclared request ledger and 42 completed result records;
- 42 sanitized response-metadata records and 42 retained response objects;
- exact planned/actual path reconciliation;
- a header-only derived-tile ledger recording zero tile requests;
- the 17,353-entry extraction inventory and exact R3-G1 path reconciliation;
- permitted toolchain version and environment evidence;
- normalized acquisition, network, and command event records;
- graph status recording no graph command, no `go.sum`, and no online/offline reconciliation;
- the stop register and rollback state; and
- complete path, mode, size, and checksum inventories.

Final inventory controls:

| Evidence | Accepted result |
|---|---|
| `workspace-checksums.sha256` | 106 lines; SHA-256 `d142dcea343eef409fba750c8ef425b703dceb685d39c876b297040d2353bf8b` |
| `cache-inventory.tsv` | 108 lines; SHA-256 `b1032a2c4aa1e00bd836544d9bcf8c7e4180446e21a44f4c2d79467bd0fb29c2` |
| Inventory verification | Zero checksum failures |
| Directory modes | Normalized to owner-only `0700` |
| Evidence/object file modes | Owner-only `0600` |

An evidence-permission reconciliation found that a broad local mode operation had set the `evidence/responses` directory itself to `0600`. That exact directory was restored to `0700`; its 42 files remained `0600` and byte-identical. This correction occurred after network closure and changed no request, response, or evidence content.

## Boundary confirmation

R3-G2 did not:

- download a ZIP, source payload, or alternate toolchain;
- inspect or execute project or module source;
- contact a VCS, mirror, package manager, account, telemetry, PostgreSQL/OCI, or other application host;
- acquire a fifteenth module or alternate version;
- compile, link, build, test, run a service or listener, or create a candidate or prototype;
- create a fixture, credential, key, database, container, image, or SBOM;
- begin R3-O1, R4, Checkpoint B, production work, real-data work, cloud AI, or stack selection;
- modify the repository during execution; or
- push.

## Gate effect

R3-G2 remains incomplete. It established a verified confined toolchain extraction and exact literal metadata/lookup acquisition evidence, but it did not authenticate the checksum-database trust chain, calculate the selected module graph, classify graph edges, create a metadata-only `go.sum`, or perform online/offline reconciliation.

No module payload, graph approval, R3-O1, R4, Checkpoint B, Gate-2 pass, or stack-selection authority follows from this evidence.

## Retention and rollback

The complete R3-G2 root is retained owner-only for review. The R3-G1 root remains untouched. Retention is not permission to retry, install a verifier, promote the cache, start a service, resume graph work, or use any later-stage authority.

Any later cleanup must validate the exact root, UID, mode, realpath, sentinel, non-symlink, non-mount, process/open-file state, and inventory before removing only `/tmp/mneme-phase3-r3-g2.l4nJHn`.
