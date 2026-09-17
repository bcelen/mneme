# Phase-3 Gate-2 Checkpoint-A Decision

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Decision:** Checkpoint A is incomplete and remains open. Do not proceed to Checkpoint B.

## Finding

The acquisition controls failed closed and prevented unauthorized expansion. Exact Python prerequisites are locally complete and verified, and immutable PostgreSQL index/platform metadata is established. The full accepted prerequisite set is not locally complete or build-eligible.

Checkpoint A cannot pass because:

1. the Go archive's official redirect host was not in the accepted allowlist;
2. the Go toolchain is absent, the module checksum records were not cryptographically verified by Go, and eight graph members were undeclared;
3. the Podman package had an invalid macOS signature and disclosed unapproved destructive and privileged installer effects;
4. the age proof could not be verified with an accepted verifier and the extracted binary had only an ad-hoc signature;
5. Docker Registry blob delivery used an unallowlisted host, leaving the PostgreSQL content, package inventory, SBOM inputs, and licenses unavailable;
6. offline completeness cannot be proved from the incomplete Go and OCI caches.

These are evidence gaps, not evidence against either candidate architecture. They do not select or reject a product stack.

## Gate-2 control update

| Control | Before acquisition | Checkpoint-A evidence | Proposed status |
|---|---|---|---|
| G2-C07 exact direct pins | Verified as design input | Python pins match; all requested versions remained exact | Verified |
| G2-C08 complete transitive graph | Blocked | Python graph complete; Go graph expanded by eight undeclared modules; OCI package graph absent | Blocked |
| G2-C09 provenance and integrity | Blocked | Python verified; OCI metadata verified; Go/Podman/age/OCI content unresolved or rejected | Blocked |
| G2-C10 license/notice review | Blocked | Python and six Go license sources captured; Podman bundled and OCI image inventories incomplete | Blocked |
| G2-C11 offline build completeness | Blocked | Not run; required caches incomplete | Blocked |
| G2-C12 supply-chain failure path | Designed | Unknown hosts, undeclared modules, invalid signature, installer side effects, and unverifiable proof all caused stop/rejection | Verified for acquisition stop behavior only; build-time negative checks remain pending |
| G2-C19 acquisition-only network window | Designed | Requests and redirects logged; sensitive URLs normalized; clients ended; no persistent session remains | Verified for Checkpoint A |

Gate 2 as a whole remains open and not passed. Runtime controls C13–C30 were not exercised.

## Decisions required before a renewed Checkpoint A

Any continuation requires a revised, separately reviewed proposal that resolves all of the following without silent substitution:

- whether to add the observed official redirect hosts `dl.google.com` and `production.cloudfront.docker.com` to the allowlist, or use another reviewed primary distribution route;
- whether the eight discovered Go modules may be acquired and how the complete graph will be independently verified;
- whether to replace the Podman package/acquisition mechanism or accept a specifically justified installation route with explicit side-effect controls;
- whether to authorize acquisition of a pinned Sigsum verifier for age, adopt another independently verifiable age distribution, or remove the age probe;
- how to obtain and inventory the complete PostgreSQL arm64 image by immutable digest;
- how to demonstrate an offline-complete cache without running a build or prototype.

Approval of this evidence package alone does not resolve those questions and does not authorize new downloads.

## Prohibited next actions

Do not:

- begin Checkpoint B;
- install or execute the retained wheels or any rejected tool;
- acquire newly discovered modules, verifier tools, alternate packages, mirrors, or redirect hosts;
- initialize Podman, pull image blobs, start PostgreSQL or any service, create a listener, or create credentials or keys;
- create fixtures, candidate code, prototypes, schemas, tests, build outputs, or generated artifacts;
- access an account, inspect real correspondence, touch the live archive, use cloud AI, enable telemetry, deploy, expose a public service, send email, or mutate source data;
- select a stack, create a stack-selection ADR, commit this package, commit acquisition artifacts, or push.

## Review request

Review is requested for the accuracy and sufficiency of the normalized evidence and the decision to leave Checkpoint A open. A separate authorization is required before any renewed acquisition or Checkpoint-B activity.
