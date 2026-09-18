# R3-G2 Planner Prerequisite-Resolution Record

**Status:** Accepted
**Record date:** 2026-09-18
**Review date:** 2026-09-18
**Authority:** Accepted governance document only; no prerequisite is resolved and no implementation, build, test, retained-input, execution, or later-stage authority follows from acceptance
**Execution request:** [Proposed and uncommitted](R3-G2-PLANNER-EXECUTION-AUTHORIZATION-REQUEST.md)

## Purpose

This record makes the unresolved P2–P4 prerequisites explicit before the planner-execution request can be accepted or executed. Every row identifies the missing fact or artifact, why it is required, the only permitted way to establish it, the expected evidence and hash, the required specialist review, and its acceptance condition.

No new artifact hash is invented. A hash shown as `UNRESOLVED_*` must be replaced by the SHA-256 of the exact reviewed artifact after a separately authorized action produces it.

## P2 — implementation-review prerequisites

| ID | Exact missing fact or artifact | Why required | Permitted way to establish | Expected evidence and hash | Specialist review | Becomes Accepted when |
|---|---|---|---|---|---|---|
| `P2-01` | Complete planner-owned source diff: `README.md`, `go.mod`, `cmd/mneme-r3-g2-tile-plan/main.go`, and any planner-owned support files | Freezes parser behavior, non-verifier boundary, output schemas, caps, sentinel handling, and command interface before build | Create only the accepted experiment layout under a separate implementation authorization; no build or execution | `planner-owned-source-manifest.tsv`; SHA-256 `UNRESOLVED_P2_PLANNER_SOURCE_MANIFEST_SHA256` | Security/privacy; supply chain; quality; architecture; orchestrator | Every source line and manifest row is reviewed; no network, verifier, key, service, graph, or product-runtime behavior exists; exact hash is recorded |
| `P2-02` | Exact copied tlog source and BSD license bytes | Ensures tile paths come from the same algorithm as the accepted Go 1.27.1 client without adding an external dependency | Copy only the four accepted files from the verified Go archive under a separate implementation authorization; compare bytes before review | `note.go` `c1d9ff098f27aab7d354385795f175a4bc0f05c46e3c37f3b3e2223f44b76236`; `tile.go` `2eb6a68b3e9f39a2926b201c0813cf2c67a1465aabc4bd88fcb310437e16bc6a`; `tlog.go` `c4bb27943a3ec8ea08ae2e0325259dc2707132ab7295d16bd3d238ba699ec628`; license `911f8f5782931320f5b8d1160a76365b83aea6447ee6c04fa6d5591467db9dad`; `copied-tlog-manifest.tsv` SHA-256 `UNRESOLVED_P2_TLOG_MANIFEST_SHA256` | Preservation/provenance; supply chain; licensing/cost; quality | All four destination files are byte-identical to accepted source hashes, the manifest hash is recorded, provenance is complete, and no other copied package exists |
| `P2-03` | Complete synthetic fixtures and planner tests | Demonstrates parsing limits, operation closure, partial/full fallback planning, sentinel behavior, determinism, and failure handling without retained inputs | Create synthetic-only fixtures and tests under the same separately reviewed implementation diff; do not run them yet | `synthetic-test-source-manifest.tsv`; SHA-256 `UNRESOLVED_P2_TEST_SOURCE_MANIFEST_SHA256` | Security/privacy; quality; orchestrator | Coverage maps to every accepted planner requirement and stop condition; fixtures contain no retained response, real correspondence, key, credential, or live response; exact hash is recorded |
| `P2-04` | Complete P2 implementation review decision | Prevents code creation from being treated as build or execution authority | Seven specialists review the exact diff and record findings without running the planner | `P2-IMPLEMENTATION-REVIEW.md`; SHA-256 `UNRESOLVED_P2_REVIEW_SHA256` | All seven specialist functions | All findings are `Pass` or explicitly resolved; no disagreement remains; the record says build, tests, and retained-input access remain unauthorized |

## P3 — synthetic build/test authorization prerequisites

| ID | Exact missing fact or artifact | Why required | Permitted way to establish | Expected evidence and hash | Specialist review | Becomes Accepted when |
|---|---|---|---|---|---|---|
| `P3-01` | Exact offline build command, environment, disposable layout, timeout, and rollback procedure | Prevents dependency resolution, global installation, user-state access, or undeclared tool execution during build | Derive a literal command ledger from accepted P2 source; use the accepted Go 1.27.1 binary only, `GOPROXY=off`, no external modules, owner-only root, and denied network | `P3-BUILD-AUTHORIZATION.md`; SHA-256 `UNRESOLVED_P3_BUILD_AUTH_SHA256`; compiler binary must remain `132b69336a1f809932a8a20b0201dbbb980e86e3a323ae32e893639d83d71598` | Security/privacy; supply chain; quality; orchestrator | Command ledger has no placeholder, dependency fetch, install, `go.sum`, service, or retained-input path; rollback and evidence are complete; user explicitly accepts it |
| `P3-02` | Exact synthetic-test command and test-to-requirement matrix | Limits testing to accepted synthetic cases and proves every control has a test or justified static review | Derive literal test commands and matrix from accepted P2 tests; no retained input or network | `P3-SYNTHETIC-TEST-AUTHORIZATION.md` and `test-to-requirement.tsv`; combined-manifest SHA-256 `UNRESOLVED_P3_TEST_AUTH_MANIFEST_SHA256` | Security/privacy; quality; orchestrator | Every command, fixture, expected result, cap, and stop condition is frozen; no retained input, verifier, key, network, graph, or later-stage action is included; user explicitly accepts it |
| `P3-03` | P3 authorization decision | Build and tests may not begin merely because their plans exist | Record explicit user approval limited to the exact P3-01/P3-02 artifacts | `P3-DECISION.md`; SHA-256 `UNRESOLVED_P3_DECISION_SHA256` | Orchestrator/governance with confirmation from security and quality | Decision names accepted hashes, authorizes only isolated build and synthetic tests, and preserves every retained-input and later-stage prohibition |

## P4 — build/test evidence prerequisites

| ID | Exact missing fact or artifact | Why required | Permitted way to establish | Expected evidence and hash | Specialist review | Becomes Accepted when |
|---|---|---|---|---|---|---|
| `P4-01` | Planner binary identity and reproducibility result | Execution must use one reviewed binary whose origin and repeatability are known | Under accepted P3 only, perform two clean offline builds and compare outputs; do not install or run against retained inputs | `planner-binary-evidence.json`; binary SHA-256 `UNRESOLVED_P4_BINARY_SHA256`; evidence SHA-256 `UNRESOLVED_P4_BINARY_EVIDENCE_SHA256` | Supply chain; quality; security/privacy | Both builds are explained and accepted, binary identity is frozen, no undeclared output exists, and exact hashes are recorded |
| `P4-02` | Final source manifest tying binary to reviewed source | Prevents source drift between P2 review and P3 build | Hash every accepted planner, copied tlog, license, module, fixture, and test file after build; compare with P2 | `planner-source-manifest.tsv`; SHA-256 `UNRESOLVED_P4_SOURCE_MANIFEST_SHA256` | Preservation/provenance; supply chain; quality | Manifest exactly matches accepted P2 content and the built binary's source inputs; no extra file or drift exists |
| `P4-03` | Synthetic-test execution report | Establishes parser, path planning, caps, sentinel, determinism, and failure controls before retained inputs | Run only accepted P3 synthetic commands in denied-network disposable roots | `synthetic-test-report.json`; SHA-256 `UNRESOLVED_P4_TEST_REPORT_SHA256` | Quality; security/privacy; orchestrator | Every required test passes or an accepted explanation resolves it; no retry, retained input, network, verifier, key, or later-stage action occurred |
| `P4-04` | Planner SBOM | Makes compiler, standard-library, copied-source, and binary composition reviewable | Generate from accepted source/build records using only the approved offline evidence path | `planner-sbom.spdx.json`; SHA-256 `UNRESOLVED_P4_SBOM_SHA256` | Supply chain; licensing/cost | SBOM is complete, names no undeclared dependency, and reconciles exactly to the source and binary manifests |
| `P4-05` | License report | Confirms obligations for copied x/mod source and produced binary | Review accepted license bytes and SBOM; produce documentation only | `planner-license-report.md`; SHA-256 `UNRESOLVED_P4_LICENSE_REPORT_SHA256` | Licensing/cost; supply chain | BSD 3-Clause provenance and obligations are complete; no unknown or incompatible license remains |
| `P4-06` | No-network and isolation evidence | Retained-input execution cannot be authorized without proof that the planner build/test boundary is enforceable | During accepted P3, record process, environment, listener, connection, root, cache, and postflight evidence without contacting a host | `planner-no-network-evidence.json`; SHA-256 `UNRESOLVED_P4_NETWORK_EVIDENCE_SHA256` | Security/privacy; quality | Evidence proves zero request/listener, owner-only confinement, no user state, no key/verifier path, and clean closure; exact hash is recorded |
| `P4-07` | Complete P4 specialist review and acceptance decision | Converts raw build/test artifacts into governed evidence suitable for an execution decision | All seven specialists review P4-01 through P4-06 and record disagreements and residual uncertainty | `P4-EVIDENCE-DECISION.md`; SHA-256 `UNRESOLVED_P4_DECISION_SHA256` | All seven specialist functions | Every required finding passes, every artifact hash is accepted, no unresolved disagreement remains, and retained-input execution is still explicitly unauthorized |

## Execution-request resolution prerequisite

| ID | Exact missing fact or artifact | Why required | Permitted way to establish | Expected evidence and hash | Specialist review | Becomes Accepted when |
|---|---|---|---|---|---|---|
| `P4-E-01` | Fully resolved revision of `R3-G2-PLANNER-EXECUTION-AUTHORIZATION-REQUEST.md` | The current request contains `UNRESOLVED_P4_*` blockers and cannot identify the executable binary or accepted evidence | After P4-07 only, replace every unresolved token with the exact accepted hash; make no other scope expansion; present the complete revised diff | Revised request SHA-256 `UNRESOLVED_P4E_REQUEST_SHA256` plus a zero-placeholder check | Orchestrator/governance; preservation/provenance; security/privacy; quality | Every placeholder is replaced by an accepted P4 value, all cross-references reconcile, the diff introduces no new authority, the request remains uncommitted until user review, and the user explicitly authorizes P4-E execution |

## Resolution order

The only permitted order is:

```text
P2-01 → P2-02 → P2-03 → P2-04
      → P3-01 → P3-02 → P3-03
      → P4-01 → P4-02 → P4-03 → P4-04 → P4-05 → P4-06 → P4-07
      → P4-E-01
```

Items within a gate may be prepared together for review, but no action in the next gate may execute before the prior gate's decision is Accepted. A failed or incomplete item blocks all downstream items.

## Current disposition

- P1 is Accepted.
- P2–P4 and P4-E are unresolved.
- The planner-execution request remains `Proposed` and uncommitted.
- No retained input has been read by a planner.
- No planner source, build, test, binary, SBOM, license report, or execution evidence has been authorized or created by this record.

## Explicit non-authorization

This accepted governance record does not by itself authorize creating an implementation artifact, copying accepted tlog source, building or testing anything, reading retained inputs, executing the planner, invoking Go or a verifier, using a key, accessing the network, retrying a lookup, changing the allowlist, acquiring a tile, creating `go.sum`, running a graph command, beginning R3-O1, committing the proposed execution request or later artifacts, or pushing.

## Accepted governance decision

The review accepted the completeness of the P2–P4 inventory, the permitted resolution route and hash requirement for each item, the assigned specialist reviews, each acceptance condition, and the strict resolution order. Acceptance resolves governance structure only. Every P2–P4 item remains individually unresolved until its own evidence is reviewed and accepted. The execution request remains unchanged, `Proposed`, uncommitted, and non-executable.
