# P2-02 Copied Transparency-Log Source Execution Authorization Request

**Status:** Accepted
**Request date:** 2026-09-18
**Review date:** 2026-09-18
**Execution readiness:** Authorized only for the exact bounded P2-02 workstream after this document is committed; P2-02 evidence remains unaccepted until later review
**Current authority:** One offline archive revalidation, four literal member reads and copies, exactly seven repository-path changes, required integrity evidence, and stop for review; no Go invocation, build, test, planner execution, retained-input read, verifier, key, network action, P2-03 work, implementation commit, or push is authorized
**Accepted planning decision:** [P2-02 copied transparency-log source proposal](P2-02-COPIED-TLOG-SOURCE-PROPOSAL.md), commit `48c4fbf`
**Accepted predecessor:** P2-01 planner-owned source, commit `01a86b3`

## Authorized decision

The accepted decision authorizes one offline, byte-preserving P2-02 workstream that:

1. revalidates the already accepted Go 1.27.1 archive without contacting a host;
2. reads exactly four literal archive members;
3. copies exactly three transparency-log source files and one BSD 3-Clause license file into the accepted experiment tree;
4. proves source-to-destination byte identity with independent byte counts, SHA-256 values, and byte comparisons;
5. creates one deterministic copied-source manifest;
6. makes only the minimum source-embedding and manifest-classification changes needed to report the copied files with correct provenance and licensing; and
7. stops for complete diff and evidence review before build, test, execution, or commit.

This authority covers only that bounded copy-and-document operation. It does not accept P2-02 evidence, authorize P2-03, invoke Go, or make the planner buildable evidence acceptable.

## Exact source object

| Field | Required value |
|---|---|
| Retained archive | `/tmp/mneme-phase3-r3-g1.UQ7udQ/downloads/go/go1.27.1.darwin-arm64.tar.gz` |
| Filename | `go1.27.1.darwin-arm64.tar.gz` |
| Platform | macOS arm64 |
| Accepted bytes | `68,100,347` |
| Accepted SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Accepted acquisition result | `Verified archive bytes` |
| Accepted acquisition evidence | [R3-G1 evidence](r3-g1/README.md) |
| Bundled source identity | `golang.org/x/mod v0.36.1-0.20260813213634-8569e2639ca1` |
| Network requests permitted | `0` |

The accepted archive is a source artifact, not a tool to execute. No `go` binary or other archive member may be extracted, installed, or invoked.

## Exact source and destination set

| ID | Literal archive member | Literal repository destination | Required SHA-256 | Required provenance | License ID |
|---|---|---|---|---|---|
| `TLOG-01` | `go/src/cmd/vendor/golang.org/x/mod/sumdb/tlog/note.go` | `experiments/phase-3/r3-g2-tile-planner/internal/tlog/note.go` | `c1d9ff098f27aab7d354385795f175a4bc0f05c46e3c37f3b3e2223f44b76236` | Go 1.27.1 bundled `golang.org/x/mod v0.36.1-0.20260813213634-8569e2639ca1` | `BSD-3-Clause-x-mod` |
| `TLOG-02` | `go/src/cmd/vendor/golang.org/x/mod/sumdb/tlog/tile.go` | `experiments/phase-3/r3-g2-tile-planner/internal/tlog/tile.go` | `2eb6a68b3e9f39a2926b201c0813cf2c67a1465aabc4bd88fcb310437e16bc6a` | Go 1.27.1 bundled `golang.org/x/mod v0.36.1-0.20260813213634-8569e2639ca1` | `BSD-3-Clause-x-mod` |
| `TLOG-03` | `go/src/cmd/vendor/golang.org/x/mod/sumdb/tlog/tlog.go` | `experiments/phase-3/r3-g2-tile-planner/internal/tlog/tlog.go` | `c4bb27943a3ec8ea08ae2e0325259dc2707132ab7295d16bd3d238ba699ec628` | Go 1.27.1 bundled `golang.org/x/mod v0.36.1-0.20260813213634-8569e2639ca1` | `BSD-3-Clause-x-mod` |
| `TLOG-LICENSE-01` | `go/src/cmd/vendor/golang.org/x/mod/LICENSE` | `experiments/phase-3/r3-g2-tile-planner/LICENSES/golang.org-x-mod-BSD-3-Clause.txt` | `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad` | License bytes bundled beside the accepted x/mod source | `BSD-3-Clause-x-mod-text` |

No archive-member search is authorized. An absent literal path or hash mismatch is a stop, not permission to search for or substitute another source or license.

## Provenance proof available before execution

| Link | Accepted evidence | Proven fact |
|---|---|---|
| Publisher route | Accepted R1/R2 route records | The exact Go 1.27.1 macOS arm64 publisher object and expected archive SHA-256 were fixed before acquisition |
| Acquired object | [Accepted R3-G1 evidence](r3-g1/README.md) | One direct response produced exactly 68,100,347 bytes with the accepted SHA-256; redirects and retries were zero |
| Archive structure | Accepted R3-G1 static inventory | The archive has one `go/` top-level path and no absolute, traversal, duplicate, symbolic-link, hard-link, device, FIFO, or privileged-mode anomaly |
| Source identity | [Accepted planner design](R3-G2-LITERAL-CHECKSUM-TILE-PLANNER-PROPOSAL.md) | The three exact tlog member hashes and bundled x/mod pseudo-version are frozen |
| License identity | Accepted remediation and planner-design records | The bundled BSD 3-Clause license hash is frozen as `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad` |
| Destination boundary | Accepted P2-02 planning decision | The four member-to-destination mappings and no-substitution rule are frozen |

This chain proves the accepted source route and expected identities. The later bounded copy must add direct member-byte and destination-byte evidence before P2-02 itself can be accepted.

## License proof requirement

The copied source may be classified `BSD-3-Clause-x-mod` only if all of the following hold after an authorized copy:

1. the literal license member exists exactly once and is a regular, non-linked archive member;
2. its bytes hash to `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad`;
3. the repository license destination is byte-identical to those member bytes;
4. the copied-source manifest links all three source files to that exact license ID and module identity;
5. no second license, patent notice, attribution file, or contrary term is inferred, copied, or silently omitted from the declared boundary; and
6. the licensing/cost reviewer confirms that the accepted BSD 3-Clause treatment is complete for this bounded source copy.

If the reviewer determines that another notice is legally required, P2-02 stops as `Incomplete`; this request does not authorize searching for or copying it.

## Exact implementation delta permitted after approval

The future uncommitted diff may touch exactly these seven paths:

```text
experiments/phase-3/r3-g2-tile-planner/LICENSES/golang.org-x-mod-BSD-3-Clause.txt
experiments/phase-3/r3-g2-tile-planner/copied-tlog-manifest.tsv
experiments/phase-3/r3-g2-tile-planner/internal/tlog/note.go
experiments/phase-3/r3-g2-tile-planner/internal/tlog/tile.go
experiments/phase-3/r3-g2-tile-planner/internal/tlog/tlog.go
experiments/phase-3/r3-g2-tile-planner/planner-owned-source-manifest.tsv
experiments/phase-3/r3-g2-tile-planner/sourcebundle.go
```

The first five paths are additions. The final two are narrowly bounded modifications. No README, `go.mod`, planner logic, command, parser, output writer, test, fixture, or documentation file may change during execution.

### Exact source-embedding change

The accepted `go:embed` pattern must change from:

```go
//go:embed README.md go.mod sourcebundle.go planner-owned-source-manifest.tsv cmd/mneme-r3-g2-tile-plan/main.go internal/planner/*.go
```

to:

```go
//go:embed README.md go.mod sourcebundle.go planner-owned-source-manifest.tsv copied-tlog-manifest.tsv LICENSES/golang.org-x-mod-BSD-3-Clause.txt cmd/mneme-r3-g2-tile-plan/main.go internal/planner/*.go internal/tlog/*.go
```

The pattern may not be broadened to `**`, a parent directory, all of `internal/`, or any unlisted file.

### Minimal manifest-classification correction

The accepted P2-01 manifest generator currently emits `planner-owned` and `project-internal-no-redistribution-grant` for every embedded path. Applying only the pattern change would misstate copied-source provenance. The same `sourcebundle.go` edit must therefore make the smallest deterministic path-based classification necessary to emit:

| Embedded path class | `origin` | `license_status` |
|---|---|---|
| `internal/tlog/*.go` | `copied-go1.27.1-x-mod@v0.36.1-0.20260813213634-8569e2639ca1` | `BSD-3-Clause-x-mod` |
| `LICENSES/golang.org-x-mod-BSD-3-Clause.txt` | `copied-go1.27.1-x-mod-license` | `BSD-3-Clause-x-mod-text` |
| `copied-tlog-manifest.tsv` | `p2-02-provenance-evidence` | `project-internal-no-redistribution-grant` |
| Every accepted P2-01 path | Existing `planner-owned` value | Existing `project-internal-no-redistribution-grant` value |

This is a provenance correction within the accepted source-embedding function, not planner behavior. It may add no import, network capability, parser behavior, command option, output file, or dependency. Any broader code change stops P2-02.

### Accepted-manifest refresh

`planner-owned-source-manifest.tsv` may change only its `sourcebundle.go` row to the post-edit byte count and SHA-256. Every other accepted row must remain byte-for-byte identical to commit `01a86b3`. The manifest file's new SHA-256 must be recorded in the P2-02 evidence.

## Exact copied-source manifest contract

The new `copied-tlog-manifest.tsv` must have exactly this header:

```text
copy_id	archive_sha256	archive_member	module_identity	destination	bytes	sha256	license_id	copy_status
```

It must contain exactly four LF-terminated rows ordered `TLOG-01`, `TLOG-02`, `TLOG-03`, `TLOG-LICENSE-01`. All fixed values must match this request. The independently observed byte count fills `bytes`; `copy_status` may be `BYTE_IDENTICAL` only after source-stage and repository-destination size, SHA-256, and byte comparison all agree.

No absolute temporary path, timestamp, hostname, user ID, unresolved value, extra column, extra row, or normalized source content is permitted. The complete manifest SHA-256 must be recorded as the resolution of `UNRESOLVED_P2_TLOG_MANIFEST_SHA256` for review, not inserted retroactively into the manifest itself.

## Disposable staging boundary

After approval, create one owner-only root using:

```text
/tmp/mneme-phase3-p2-02.XXXXXX
```

The validated expanded root must be mode `0700`, owned by UID 501, a non-symlink, not a mount point, and contain a matching `MNEME_PHASE3_DISPOSABLE.json` sentinel. Its only permitted content is:

```text
<root>/
├── MNEME_PHASE3_DISPOSABLE.json
├── source/
│   ├── note.go
│   ├── tile.go
│   ├── tlog.go
│   └── LICENSE
└── evidence/
    ├── archive-preflight.tsv
    ├── member-metadata.tsv
    ├── source-stage-manifest.tsv
    ├── destination-comparison.tsv
    ├── command-ledger.tsv
    ├── rollback.json
    └── stop-register.md
```

Directories are mode `0700`; staged files and evidence are mode `0600`. Raw evidence stays outside Git. The accepted R3-G1 archive and root remain read-only and unchanged.

## Exact command and tool boundary

Only these system utilities may be used for the approved copy workstream:

```text
/usr/bin/mktemp
/usr/bin/id
/usr/bin/stat
/usr/bin/realpath
/usr/bin/find
/usr/bin/shasum
/usr/bin/wc
/usr/bin/cmp
/usr/bin/tar
/bin/chmod
/bin/cp
/bin/ls
/bin/mkdir
/sbin/mount
/usr/sbin/lsof
```

`/usr/bin/tar` may receive only the exact archive path and one literal member path from this request at a time. Wildcards, member listing without a literal path, recursive extraction, extraction of directories, and archive writes are forbidden. Each member is streamed once to its literal staging destination; no broad archive extraction is permitted.

Repository metadata edits must use the reviewed patch mechanism. No shell-generated rewrite, formatter, generator, package manager, compiler, linker, Go command, or project executable is permitted.

## Authorized sequence if separately approved

1. Record the current repository commit and confirm only the previously Proposed planner-execution request is unrelated uncommitted content.
2. Validate the R3-G1 root and archive identity against the exact accepted path, owner, mode, sentinel, type, byte count, and SHA-256.
3. Create and validate the disposable P2-02 root and sentinel.
4. Query metadata for each of the four literal members only; require one regular, non-linked result per path.
5. Stream each literal member once to its fixed staging filename without extracting anything else.
6. Record independent byte counts and SHA-256 values; require all four accepted hashes.
7. Create the four literal repository destinations and copy the staged bytes without normalization.
8. Compare each staging file and destination by byte count, SHA-256, and exact byte comparison.
9. Create `copied-tlog-manifest.tsv` with exactly four reconciled rows.
10. Apply only the accepted embed-pattern and path-classification edit to `sourcebundle.go`.
11. Refresh only the `sourcebundle.go` row in `planner-owned-source-manifest.tsv` and verify all other rows against commit `01a86b3`.
12. Verify the Git diff contains exactly the seven authorized paths, run whitespace and status checks, preserve the owner-only evidence root, and stop for review.

No step may invoke Go, build, test, execute copied source, read retained R3-G2 lookups, use a verifier or key, or contact a network host.

## Required evidence at the stop

The review package must provide:

1. exact archive preflight identity and comparison with accepted R3-G1 evidence;
2. literal member metadata proving unique regular non-linked entries;
3. source-stage and destination path, byte-count, SHA-256, and byte-comparison results for all four files;
4. complete `copied-tlog-manifest.tsv` and its SHA-256;
5. pre/post SHA-256 and complete diff for `sourcebundle.go`;
6. proof that only the `sourcebundle.go` row changed in `planner-owned-source-manifest.tsv`, plus its new SHA-256;
7. complete seven-path Git diff and zero extra repository paths;
8. exact sanitized command ledger and zero network, Go, build, test, execution, service, listener, key, verifier, lookup, or generated-output counts;
9. specialist findings, disagreements, uncertainties, and stop record; and
10. disposable-root inventory and rollback/retention state.

Raw archive bytes and staging evidence remain outside Git. Only the four accepted copied files and three narrowly permitted repository evidence/embedding paths may appear in the P2-02 implementation diff.

## Specialist reviews required before P2-02 acceptance

| Review function | Required finding |
|---|---|
| Preservation / provenance | Archive-to-member-to-staging-to-destination identity is byte-preserving and fully manifested |
| Supply chain / maintenance | Exactly the three accepted non-network tlog files are present, with no dependency, broader x/mod package, generated source, or executable content added |
| Licensing / cost | The exact accepted BSD 3-Clause license bytes and source linkage are complete; no unresolved notice, account, service, or cost exists |
| Quality / independent verification | All independent hashes, counts, comparisons, row constraints, sourcebundle classifications, and no-extra-path checks pass |
| Orchestrator / governance | The seven-path boundary is exact; P2-03 and every build, test, retained-input, verifier, graph, and later gate remain blocked |

Any non-`Pass` finding or unresolved disagreement keeps P2-02 `Incomplete`.

## Stop conditions

Stop without retry, substitution, source repair, or partial promotion if:

- the accepted archive root, sentinel, path, type, owner, mode, byte count, or hash differs;
- a literal member is missing, duplicated, linked, non-regular, differently named, or hashes differently;
- another archive member is queried, listed, extracted, or copied;
- source-stage and destination bytes, counts, hashes, or comparisons differ;
- copied bytes are normalized, formatted, patched, renamed, or combined;
- another source, dependency, package, license, notice, fixture, test, generated file, or repository path appears;
- `sourcebundle.go` changes beyond the exact embed list and minimum provenance classification;
- any accepted P2-01 manifest row other than `sourcebundle.go` changes;
- the copied-source manifest contains an unresolved, extra, reordered, or inconsistent value;
- a network request, Go command, build, test, project execution, service, listener, retained lookup read, verifier, key, or later-stage action occurs; or
- the evidence root, Git diff, or rollback state cannot be reconciled.

A stop leaves P2-02 `Incomplete`, preserves bounded owner-only evidence, and returns for review. No automatic cleanup or retry is authorized.

## Rollback and retention

The accepted R3-G1 root and P2-01 commit must remain unchanged. On a stop, preserve the disposable P2-02 root owner-only and do not alter the repository further.

Cleanup requires a later explicit instruction and must validate the exact root, UID, mode, sentinel, realpath, non-symlink, non-mount, process, open-file, and inventory state before removing only that root. Removing uncommitted repository destinations also requires an exact later instruction. No wildcard deletion, Git reset, checkout, broad cache cleanup, package uninstall, archive removal, or unrelated-file change is permitted.

## Explicit non-authorization

This Accepted request does not authorize:

- opening, listing, or extracting any archive or member outside the one exact archive preflight and four literal member operations authorized here;
- creating any disposable root outside the one exact owner-only P2-02 staging boundary;
- creating or modifying any repository path outside the seven-path boundary;
- adding a dependency, changing `go.mod`, or creating `go.sum`;
- invoking Go, a compiler, linker, formatter, verifier, key, build, test, or project executable;
- reading retained R3-G2 lookups, tiles, credentials, correspondence, accounts, or user configuration;
- accessing the network, changing an allowlist, or starting a service/listener;
- beginning P2-03, P2-04, P3, P4, P4-E, R3-O1, Checkpoint B, deployment, stack selection, or production work;
- committing this request, the copied source, evidence, or the still-Proposed planner-execution request; or
- pushing.

## Accepted explicit authorization

On 2026-09-18, the user supplied the required explicit authorization, limited to this exact request. The accepted authorization is substantively equivalent to:

> I authorize P2-02 execution only under the accepted `P2-02-COPIED-TLOG-SOURCE-EXECUTION-AUTHORIZATION-REQUEST.md`: revalidate the exact retained Go archive offline, read and copy only the four literal members, make only the seven authorized repository-path changes, produce the specified byte-identity and provenance evidence, and stop for review. Do not invoke Go, build, test, execute code, read retained lookups, use a verifier or key, access the network, begin P2-03, commit implementation evidence, or push.

The authorization becomes executable only after this Accepted document is committed. Approval of the planning proposal, document preparation, or a general instruction to continue would have remained insufficient.

## Accepted authorization decision

The review accepted the exact archive and member identities, provenance and license proof chain, seven-path repository boundary, minimal source-embedding and manifest-classification edits, command and staging limits, evidence requirements, specialist reviews, stop conditions, rollback, and explicit execution boundary.

Acceptance authorizes execution only after this document's commit. It does not accept the resulting files or evidence. The workstream must stop after producing the seven-path diff and complete evidence package; P2-03 and all later work remain closed.
