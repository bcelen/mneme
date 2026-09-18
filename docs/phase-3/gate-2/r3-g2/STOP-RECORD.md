# R3-G2 Stop Record

**Status:** Accepted
**Review date:** 2026-09-18
**Workstream result:** Incomplete
**Stop code:** `SUMDB_CACHE_TRUST_CHAIN_AMBIGUITY`

## Stop decision

R3-G2 stopped before checksum-tile acquisition and before any graph command because the checksum-database integrity precondition was not proved.

The fourteen authorized checksum lookup paths had been fetched exactly once over HTTPS and retained with response, byte-count, and SHA-256 evidence. Manually placing those responses in Go's checksum cache would not prove that the Go checksum client authenticated their signed tree heads and Merkle inclusion proofs. The responses therefore remain unverified inputs.

## Rejected continuations

No continuation was authorized that could close the proof gap without changing an accepted boundary:

- repeating the fourteen lookup requests through the Go client would violate the exact request count and no-repeat rule;
- introducing and executing a verifier or helper would add unreviewed code, dependencies, commands, and trust bootstrap;
- starting a local interception or sumdb service would violate the no-service boundary and alter the route; and
- treating HTTPS transport and retained-object hashes as sumdb authentication would weaken the accepted integrity requirement.

R3-G2 therefore stopped without retry, substitution, cache promotion, verifier execution, service startup, `go list`, `go mod graph`, `go.sum` creation, build, or test.

## Preserved partial evidence

- verified and confined Go 1.27.1 toolchain extraction;
- exact toolchain identity and environment output;
- fourteen `.info`, fourteen `.mod`, and fourteen checksum lookup responses;
- 42 HTTP 200 results with zero redirects, retries, duplicates, or byte-count mismatches;
- zero derived checksum tiles, ZIPs, ZIP hashes, source trees, VCS requests, builds, or tests; and
- owner-only raw evidence retained at `/tmp/mneme-phase3-r3-g2.l4nJHn`.

## Evidence-packaging anomaly

A permission reconciliation found that a broad local mode operation had set the `evidence/responses` directory itself to `0600`, preventing traversal. The exact directory was restored to `0700`; its 42 response files remained `0600` and byte-identical. The correction occurred after network closure and caused no request, retry, integrity change, or scope expansion.

## Effect

The module graph remains open and unproved. The fetched checksum records are not authenticated sumdb evidence. No R3-G2 completion, graph closure, offline reconciliation, module-payload authority, R3-O1 authority, later-stage authority, Gate-2 pass, or stack selection is claimed.

Any remediation route requires a separate proposed document, specialist review, and explicit user approval before execution. This accepted stop record provides no such authorization.
