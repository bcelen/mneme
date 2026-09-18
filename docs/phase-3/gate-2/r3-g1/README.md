# R3-G1 Go Archive Acquisition Evidence

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Result:** `Verified archive bytes`
**Authorization commit:** `68c409b6fab8aa189f902cb7134183974a6a1301`
**Disposable root:** `/tmp/mneme-phase3-r3-g1.UQ7udQ`

## Accepted conclusion

R3-G1 completed its single authorized request and stopped for review. The received archive's independently recorded byte count and SHA-256 match the accepted controls, and static archive inspection found no path, type, link, duplicate, or expansion anomaly that blocks retention.

The result establishes verified archive bytes only. It does not approve extraction or execution of Go, close the module graph, pass Checkpoint A or Gate 2, authorize R3-G2 or R3-O1, or select a stack.

## Preflight evidence

| Control | Result |
|---|---|
| Repository | Clean at commit `68c409b6fab8aa189f902cb7134183974a6a1301` |
| Prior matching root | None |
| Prior matching transfer process | None |
| Disposable root | `/tmp/mneme-phase3-r3-g1.UQ7udQ` |
| Root owner | UID 501 |
| Root and subdirectory mode | `0700` |
| Sentinel | Matching `MNEME_PHASE3_DISPOSABLE.json` present |
| Filesystem boundary | Root is neither a symlink nor a mount point |
| Transfer destination before request | Absent |

The archive and raw evidence remain outside the repository under the accepted owner-only temporary root.

## Request evidence

| Field | Accepted result |
|---|---|
| URL | `https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz` |
| Method | One direct `GET` |
| HTTP status | 200 |
| Effective URL | Identical to requested URL |
| Redirects | 0 |
| Retries | 0 |
| Range/resume | Not used |
| Mirror/package manager/fallback | Not used |
| Authentication/account | None |
| HTTP version | 2 |
| Content type | `application/x-gzip` |
| Response `Content-Length` | 68,100,347 bytes |
| Client body count | 68,100,347 bytes |
| Independent `wc` count | 68,100,347 bytes |
| Independent filesystem count | 68,100,347 bytes |
| TLS verification result | 0 |
| Additional application host | None |
| Network state after request | Closed; no matching process, open cache file, or TCP connection remained |

The four byte counts agree. Per accepted uncertainty `U-R2-GO-01`, they—not the publisher's rounded 65 MB description—are the authoritative size evidence.

The acquisition client reported one unsupported diagnostic-only write-out variable, `content_length_download`. This did not affect the request or integrity decision: the request exited successfully, no retry occurred, and the response header, client count, `wc`, and filesystem count independently agree. The anomaly remains visible rather than being omitted.

## Integrity evidence

| Control | Result |
|---|---|
| Expected SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Independently calculated SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Digest match | Yes |
| Gzip integrity read | Passed |
| Detached signature | None established; hash verification is not represented as publisher-signature verification |
| Archive mode | `0600` |
| Partial file | Absent |

## Static archive inspection

| Check | Accepted result |
|---|---:|
| Members | 17,353 |
| Regular files | 15,639 |
| Directories | 1,714 |
| Declared regular-file bytes | 239,785,751 |
| Largest regular file | 27,080,208 bytes |
| Declared/compressed ratio | 3.521065 |
| Top-level path | `go/` only |
| Absolute paths | 0 |
| Traversal paths | 0 |
| Duplicate paths | 0 |
| Empty paths | 0 |
| Tab or carriage-return paths | 0 |
| Symbolic links | 0 |
| Hard links | 0 |
| Device or FIFO entries | 0 |
| Privileged mode entries | 0 |

The complete temporary path inventory records 17,353 paths. The complete metadata inventory records type, mode, owner, group, declared size, timestamp, path, and link target for every member. Static inspection did not extract or execute any member.

## Retained evidence inventory

The owner-only root contains twelve files: the verified archive, sentinel, nine other evidence records, and the cache inventory itself. The inventory file excludes only its own self-hash.

| Bytes | SHA-256 | Relative path |
|---:|---|---|
| 357 | `a1d4a5fe474fb81fc5228ea8cb7daab436837d83a44b012edba81b0617115029` | `MNEME_PHASE3_DISPOSABLE.json` |
| 68,100,347 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` | `downloads/go/go1.27.1.darwin-arm64.tar.gz` |
| 3,605 | `d30fb792075b8a2addfddbe217e3a3cc3115459f11a6911d8d346a866eee362a` | `evidence/R3-G1-EVIDENCE.md` |
| 2,100 | `a35982e03397e08ec9900253281114fa223f5e509c812c05ad433014c914ebb1` | `evidence/acquisition.jsonl` |
| 1,055 | `1bfc930afdff4b670b92f10cbd8ada762a1c0d9f7096f9f3fbe502bdc8f57a8f` | `evidence/archive-inventory.json` |
| 1,562,034 | `857729eb3ad48f1b40dddcd63d1f01a70ca552c90bf86561ff5739f767d0c11e` | `evidence/archive-members.txt` |
| 729,090 | `c8200309ba95329154a04714ee661279b2e3504399f4213105decab6c8fde648` | `evidence/archive-paths.txt` |
| 296 | `2a935b830f86a9dc4ab2369b5ddc768c5e1ad619bba8012bc3f519c77a8f5008` | `evidence/checksums.sha256` |
| 656 | `146b2812a1c6252d702cf0fe1619a3813f33add6e7a0234d8a9e21cc0fa1e258` | `evidence/environment.json` |
| 757 | `fc45d3069ee5bbb3de166f762e1da60a4bdabe61a0ebeb9fab3097a61fec4600` | `evidence/network.jsonl` |
| 514 | `24052bbe34d6dcf9db4443c2af73328173dc3045a61151bae3a80b4412b8fe0` | `evidence/rollback.json` |

`evidence/cache-inventory.tsv` is 1,103 bytes with SHA-256 `f82f88db442e25ed3a333d1e8240c72f283eb696c403825d157be648a952bf38`. Its eleven recorded size/hash entries were revalidated with zero failures. The archive and full path/metadata inventories also passed the independent `checksums.sha256` reconciliation.

## Boundary confirmation

R3-G1 did not:

- extract, execute, or install Go;
- create or inspect a Go module workspace;
- contact `go.dev`, `proxy.golang.org`, `sum.golang.org`, Git/VCS, a mirror, a package manager, or any PostgreSQL/OCI host;
- create `GOROOT`, `GOPATH`, `GOBIN`, `GOCACHE`, `GOMODCACHE`, or `GOENV` state;
- create or run a build, test, service, fixture, credential, key, database, container, image, prototype, or SBOM;
- access an account, correspondence, the live archive, cloud AI, or production infrastructure;
- begin R3-G2, R3-O1, R4, Checkpoint B, prototype implementation, or stack selection; or
- commit raw cache/evidence or push.

Go remained absent from the executable path after acquisition. The repository remained clean before this normalized evidence documentation was prepared.

## Retention and rollback

The accepted result retains the verified archive and raw evidence at `/tmp/mneme-phase3-r3-g1.UQ7udQ` for review and possible later separately authorized work. Retention is not extraction, execution, or installation authority.

Any later removal must validate the exact root, UID, mode, realpath, sentinel, inventory, non-symlink, non-mount, and absence of open files/processes before removing only that root. No global cache purge, package uninstall, wildcard deletion, Git cleanup/reset, or unrelated process termination is permitted.

## Gate effect

R3-G1 closes only the archive-byte acquisition question for Go 1.27.1 macOS arm64. The following remain blocked or unproved:

- toolchain extraction and execution;
- toolchain version/environment evidence;
- checksum-database verification;
- authoritative module-graph closure and classification;
- every Go module payload;
- offline completeness;
- Podman and age routes;
- PostgreSQL OCI content;
- Checkpoint A, Gate 2, and stack selection.
