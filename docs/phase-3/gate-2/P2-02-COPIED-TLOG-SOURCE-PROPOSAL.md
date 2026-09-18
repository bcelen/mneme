# P2-02 Copied Transparency-Log Source Proposal

**Status:** Accepted
**Proposal date:** 2026-09-18
**Review date:** 2026-09-18
**Authority:** Accepted planning decision only; this document does not authorize reading the retained archive, copying a source or license file, modifying planner source, invoking Go, building, testing, executing, or committing P2-02 implementation evidence
**Predecessor:** P2-01 accepted 2026-09-18 at commit `01a86b3`
**Governing prerequisite:** [R3-G2 planner prerequisite-resolution record](R3-G2-PLANNER-PREREQUISITE-RESOLUTION.md)
**Governing design:** [R3-G2 literal checksum-tile planner](R3-G2-LITERAL-CHECKSUM-TILE-PLANNER-PROPOSAL.md)

## Purpose

P2-02 would supply only the exact non-network transparency-log source needed by the accepted planner-owned code, together with its governing BSD 3-Clause license bytes and deterministic provenance evidence. It would not add an external module dependency or authorize a build, test, planner run, retained lookup read, verifier, key, network action, or later gate.

This proposal freezes the proposed source-to-destination mapping and review controls. No source or license bytes have been copied by preparing it.

## Accepted provenance anchor

The sole proposed source object is the already accepted R3-G1 archive retained outside Git:

| Field | Exact value |
|---|---|
| Archive | `go1.27.1.darwin-arm64.tar.gz` |
| Retained path | `/tmp/mneme-phase3-r3-g1.UQ7udQ/downloads/go/go1.27.1.darwin-arm64.tar.gz` |
| Accepted result | `Verified archive bytes` |
| Bytes | `68,100,347` |
| SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| Publisher route | `https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz` |
| Source acquisition | One accepted direct GET; zero redirects and retries |
| Archive state | Owner-only retained archive; statically inspected, not a current execution authority |
| Bundled module identity | `golang.org/x/mod v0.36.1-0.20260813213634-8569e2639ca1` |

The archive path is a provenance locator, not current permission to open it. A later P2-02 authorization must revalidate the exact archive identity, owner-only root, sentinel, regular-file type, size, and SHA-256 before reading any member.

## Exact proposed copy set

Only these four archive members may be materialized, and only at the corresponding repository destinations:

| ID | Exact archive member | Exact repository destination | Required SHA-256 | Classification |
|---|---|---|---|---|
| `TLOG-01` | `go/src/cmd/vendor/golang.org/x/mod/sumdb/tlog/note.go` | `experiments/phase-3/r3-g2-tile-planner/internal/tlog/note.go` | `c1d9ff098f27aab7d354385795f175a4bc0f05c46e3c37f3b3e2223f44b76236` | Copied upstream source |
| `TLOG-02` | `go/src/cmd/vendor/golang.org/x/mod/sumdb/tlog/tile.go` | `experiments/phase-3/r3-g2-tile-planner/internal/tlog/tile.go` | `2eb6a68b3e9f39a2926b201c0813cf2c67a1465aabc4bd88fcb310437e16bc6a` | Copied upstream source |
| `TLOG-03` | `go/src/cmd/vendor/golang.org/x/mod/sumdb/tlog/tlog.go` | `experiments/phase-3/r3-g2-tile-planner/internal/tlog/tlog.go` | `c4bb27943a3ec8ea08ae2e0325259dc2707132ab7295d16bd3d238ba699ec628` | Copied upstream source |
| `TLOG-LICENSE-01` | `go/src/cmd/vendor/golang.org/x/mod/LICENSE` | `experiments/phase-3/r3-g2-tile-planner/LICENSES/golang.org-x-mod-BSD-3-Clause.txt` | `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad` | Verbatim BSD 3-Clause license bytes |

The license-member path is the exact proposed x/mod module-root location. A later authorized static member check must stop if that literal member is absent, not a regular file, duplicated, linked, or does not have the accepted hash. It may not search for or substitute a different license path.

## Source boundary

The proposed copied-source boundary is exactly the three `package tlog` files above. It excludes:

- `sumdb/client.go` and every other sumdb client file;
- the cryptographic `sumdb/note` package;
- verifier keys, Ed25519 or signature-verification helpers;
- HTTP, network, cache, service, command, and telemetry code;
- every other x/mod package or file;
- module ZIPs, module source acquisitions, VCS content, and generated code;
- synthetic fixtures and tests, which remain P2-03;
- retained R3-G2 lookup responses and checksum tiles; and
- application or product-runtime source.

The copied files must remain byte-for-byte identical to the accepted archive members. No package rename, import rewrite, formatting, comment edit, generated header, line-ending conversion, or source repair is permitted.

## Exact permitted repository delta after later approval

A later P2-02 implementation authorization may propose only:

1. the three copied files under `internal/tlog/`;
2. the one copied license file under `LICENSES/`;
3. a new `copied-tlog-manifest.tsv` containing the exact provenance rows;
4. the minimum literal `go:embed` pattern expansion in `sourcebundle.go` needed to include the three copied files, license, and copied-source manifest in future deterministic source evidence; and
5. the corresponding refresh of `planner-owned-source-manifest.tsv` for the changed `sourcebundle.go` only, preserving all other accepted P2-01 rows exactly.

No other path, source edit, dependency, module directive, `go.sum`, fixture, test, binary, SBOM, license report, generated output, or configuration file may appear. The accepted P2-01 commit remains the immutable historical baseline; any permitted metadata delta must be independently visible in the P2-02 review diff.

## Proposed copied-source manifest

The future `copied-tlog-manifest.tsv` must use this exact schema:

```text
copy_id	archive_sha256	archive_member	module_identity	destination	bytes	sha256	license_id	copy_status
```

Requirements:

- rows are ordered `TLOG-01`, `TLOG-02`, `TLOG-03`, `TLOG-LICENSE-01`;
- `archive_sha256`, archive member, module identity, destination, and required SHA-256 exactly match this proposal;
- `bytes` is the independently counted exact member byte length, recorded only after a later authorized static copy;
- source and destination byte counts and SHA-256 values must match independently;
- source files use license ID `BSD-3-Clause-x-mod`; the license row uses `BSD-3-Clause-x-mod-text`;
- `copy_status` is `BYTE_IDENTICAL` only after both source and destination checks pass;
- LF line endings and deterministic row ordering are required;
- no timestamp, hostname, absolute disposable path, user identifier, or unresolved field is permitted; and
- the manifest's SHA-256 is recorded as `UNRESOLVED_P2_TLOG_MANIFEST_SHA256` until the complete future diff is reviewed.

The manifest is evidence of byte identity and provenance. It is not build, execution, dependency, or stack-selection evidence.

## Proposed later copy procedure

If and only if P2-02 receives separate implementation authorization, the bounded procedure would:

1. verify the repository baseline and confirm no unrelated staged content;
2. revalidate the exact R3-G1 root, sentinel, archive path, type, owner, mode, byte count, and SHA-256 without network access;
3. create one fresh owner-only disposable P2-02 staging root outside Git;
4. inspect only the four literal archive-member metadata entries and require each to be unique, regular, non-linked, and bounded;
5. stream only those four member byte sequences into literal staging files without broad extraction;
6. independently hash and count each staging file and require the values in this proposal;
7. copy the verified bytes once to the four literal repository destinations;
8. independently compare source-stage and repository-destination bytes, sizes, and hashes;
9. create the deterministic copied-source manifest and make only the two permitted provenance-embedding metadata edits;
10. confirm that the complete diff contains exactly the authorized paths; and
11. stop for review without invoking Go, building, testing, executing, committing, or deleting the retained archive.

No archive-member search, wildcard extraction, recursive extraction, path fallback, alternate source, network request, or retry is permitted.

## Stop conditions

P2-02 must stop without substitution, repair, retry, or partial promotion if:

- the retained root, sentinel, archive path, type, owner, mode, size, or hash differs;
- any exact member is absent, duplicated, linked, non-regular, unexpectedly large, or differently named;
- an archive member or destination hash differs from this proposal;
- a source and destination byte count or byte comparison differs;
- a fourth source file, second license file, external dependency, `go.sum`, generated file, fixture, or test appears;
- copied source is reformatted, normalized, patched, or renamed;
- the embed-pattern change includes a wildcard broader than the literal accepted directories/files;
- the accepted P2-01 rows drift except for the one explicitly permitted `sourcebundle.go` refresh;
- a command attempts to invoke Go, build, test, execute copied or project code, read a retained lookup, use a verifier or key, contact a host, start a service or listener, or enter P2-03; or
- the exact bounded diff and manifest cannot be reconciled.

On a stop, retain bounded owner-only evidence, leave every result `Incomplete`, do not commit, and return for review.

## Required specialist review

| Review function | Required finding |
|---|---|
| Preservation / provenance | The accepted archive identity is revalidated; all four source-to-destination mappings and byte identities are complete and deterministic |
| Supply chain / maintenance | Exactly three non-network tlog files are copied; no external module, undeclared package, generated source, or broader Go toolchain content is introduced |
| Licensing / cost | The exact BSD 3-Clause license bytes accompany the source; attribution and redistribution obligations are preserved; no account, service, or cost is introduced |
| Quality / independent verification | Independent byte counts, SHA-256 checks, comparisons, manifest reconciliation, path inventory, and no-extra-file checks all pass |
| Orchestrator / governance | P2-02 remains separate from P2-03, build/test authority, retained-input execution, acquisition, graph work, R3-O1, and stack selection |

Any missing evidence, disagreement, source-boundary ambiguity, or license uncertainty blocks P2-02 acceptance.

## Acceptance condition

P2-02 may become `Accepted` only after the user reviews the complete future diff and confirms that:

1. all four destination files are byte-identical to the accepted source hashes;
2. provenance from the accepted R3-G1 archive through each destination is complete;
3. the copied-source manifest has an exact recorded SHA-256 and no unresolved field;
4. the license bytes and obligations are accepted;
5. no copied package, dependency, source modification, fixture, test, build, execution, retained input, network action, or generated artifact exists outside this proposal's exact boundary; and
6. the specialist findings are all `Pass` with no unresolved disagreement.

Acceptance would close only P2-02 as an implementation-review prerequisite. It would not authorize P2-03, P2-04, P3, P4, planner execution, checksum verification, module-graph work, or any later action.

## Rollback boundary

Before P2-02 acceptance, rejection or interruption permits removal only of the exact uncommitted P2-02 destination files and an exact validated disposable staging root under a separate cleanup instruction. The accepted P2-01 commit and retained R3-G1 archive must not be altered. No wildcard deletion, Git reset, broad cache cleanup, package uninstall, or unrelated file removal is permitted.

## Explicit non-authorization

This Accepted planning document does not authorize:

- opening or extracting the retained Go archive;
- creating any `internal/tlog`, `LICENSES`, or copied-source manifest file;
- modifying `sourcebundle.go`, the accepted P2-01 manifest, `go.mod`, or any planner source;
- adding a dependency or creating `go.sum`;
- invoking Go or another verifier, compiler, linker, build, test, or project executable;
- reading retained lookup responses, tiles, credentials, keys, correspondence, accounts, or user configuration;
- making a network request, changing an allowlist, starting a service/listener, or using cloud AI;
- beginning P2-03, P2-04, P3, P4, P4-E, R3-O1, Checkpoint B, deployment, stack selection, or production work;
- committing P2-02 or the still-Proposed planner-execution request; or
- pushing.

## Accepted planning decision

The review accepted the four literal source mappings, accepted provenance anchor, byte-preserving copy boundary, license treatment, deterministic manifest schema, two narrowly permitted provenance-metadata edits, stop conditions, specialist findings, acceptance condition, and rollback boundary as the P2-02 planning framework.

P2-02 implementation remains unresolved. Until a separate execution package is reviewed and explicitly approved, no archive member or repository destination may be read or created under this planning decision.
