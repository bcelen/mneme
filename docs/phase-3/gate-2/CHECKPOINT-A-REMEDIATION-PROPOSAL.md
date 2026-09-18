# Checkpoint-A Remediation Proposal

**Status:** Accepted
**Review date:** 2026-09-18
**Proposal date:** 2026-09-18
**Current authority:** Design and review only. No renewed acquisition is authorized.

## Purpose

This proposal defines how to resolve the five blockers accepted in the Checkpoint-A evidence package:

1. Podman package signature and installer route;
2. Go toolchain provenance and complete dependency graph;
3. age proof verification;
4. PostgreSQL image-content acquisition by immutable digest;
5. offline-completeness evidence.

It does not resolve those blockers by assertion. It defines the evidence, alternatives, stop conditions, specialist reviews, and approval gates required before any network acquisition resumes.

## Accepted baseline

The following conclusions remain governing inputs:

- Checkpoint A is incomplete and remains open.
- Gate 2 is not passed.
- G2-C12 is Verified only for the observed acquisition-stop behavior. Build-time negative checks and the full supply-chain control are not Verified.
- No stack has been selected; `EXP-C001` and `EXP-C003` remain comparison references only.
- The retained Python wheel set is verified but not installed.
- The Go, Podman, age, and PostgreSQL executable/content prerequisites are not approved for use.
- Checkpoint B, fixtures, prototypes, services, builds, and tests remain outside current authority.

## Remediation principles

Every proposed route must satisfy these rules before acquisition:

1. **Primary-source route:** identify the publisher-controlled release record, exact artifact, expected redirects, integrity mechanism, signature/proof trust root, license source, and update policy.
2. **Exact scope:** name every host, component, version, artifact, transitive dependency, verifier, helper, installer action, and expected output. No wildcard component or floating version is permitted.
3. **Independent integrity:** verify bytes independently of the tool being acquired. A checksum copied from the same unverified artifact channel is not sufficient by itself.
4. **No signature downgrade:** an invalid, absent, or unverifiable signature is recorded as such. A matching hash cannot silently replace a signature requirement already accepted for that component.
5. **No side-effect surprise:** inspect and approve installation paths, privileged operations, removals, helpers, services, login/startup behavior, network behavior, and uninstall/rollback before execution.
6. **Graph before payload:** review the complete dependency graph before acquiring newly discovered executable payloads.
7. **One bounded network window:** use only a newly approved host/artifact list, log redirects, stop on deviation, and close the acquisition clients before offline verification.
8. **No substitution by convenience:** package managers, mirrors, source builds, alternate runtimes, and new verification tools are new routes requiring explicit review.

No existing allowlist entry is changed by this proposal.

## Workstream P — Podman signature and installer route

### Accepted problem

The Podman 6.1.2 package matched the publisher's checksum, but macOS reported `Status: invalid signature`. Static inspection also found a root-authorized installer that recursively removes `/opt/podman`, writes system path/manpath files, and invokes `podman-mac-helper install`. Checkpoint A did not authorize those effects.

### Candidate remediation routes

| Route | Boundary | Evidence required before selection | Current disposition |
|---|---|---|---|
| P1 — Correctly signed publisher package | Same product/version family and publisher release channel, but only a package whose Apple signature and team identity validate | Publisher release record; exact package URL and hash; expected Apple identity; independent signature result; scripts, payload, install/uninstall paths, helper behavior, and rollback | Preferred evidence target if the publisher provides a valid replacement; not currently established |
| P2 — Publisher-documented package-manager route | Exact formula/cask and immutable bottle/artifact graph from a publisher-endorsed route | Formula revision; all bottle hosts/digests; complete transitive graph and licenses; install scripts; analytics/update behavior; paths, services, helpers, rollback, and proof that unrelated packages are untouched | Alternative for comparison only; not authorized |
| P3 — Rootless alternative harness | Replace Podman only as the Phase-3 isolation harness, without changing candidate architecture | Capability mapping for rootless containers, internal/no-network modes, resource limits, arm64 OCI support, socket/mount isolation, deterministic cleanup, license/cost, exact artifacts and signatures | Architecture-impacting alternative; requires specialist and user review |
| P4 — Defer container-backed evidence | Run only evidence that needs no container harness and leave container-dependent gates Unproved | Explicit test/gate impact and proof that no weaker substitute is presented as equivalent | Valid scope reduction; cannot pass the affected Gate-2 controls |

### Rejected shortcuts

- Do not accept the invalidly signed package because its checksum matches.
- Do not run the installer merely to observe its behavior.
- Do not pre-delete, overwrite, or adopt an existing `/opt/podman` tree.
- Do not use Homebrew, another package manager, a source build, Docker Desktop, or an alternate container runtime without a reviewed exact route.
- Do not authorize `podman-mac-helper`, a privileged helper, startup item, login item, background service, or telemetry implicitly.

### Required review

- Supply-chain specialist: provenance, signature, complete graph, and update path.
- Security/privacy specialist: privilege, helper, socket, network, mount, and side effects.
- Licensing/cost specialist: bundled components, terms, and distribution obligations.
- Quality specialist: rollback evidence and claim calibration.
- Orchestrator: exact-target installation boundary and no unrelated-state mutation.

No Podman route is recommended for execution until P1–P4 are compared with primary evidence.

## Workstream G — Go toolchain and dependency graph

### Accepted problem

The official Go URL redirected to `dl.google.com`, which was not in the accepted allowlist. The toolchain was therefore not acquired. Metadata for the six reviewed modules exposed eight additional graph members; they were correctly left unacquired. Without the exact toolchain, checksum-database verification and an authoritative minimal-version-selected graph were unavailable.

### Proposed staged resolution

#### G1 — Toolchain route record

Before any archive transfer, produce a proposed route record containing:

- exact Go version, platform archive, expected size, and SHA-256;
- publisher documentation connecting the public download page to every redirect host;
- redirect chain with query material removed from durable evidence;
- toolchain license and release/security policy;
- archive layout, installation destination, and zero-privilege/no-installer execution plan;
- independent verification method that does not require executing the new toolchain;
- exact cleanup and rollback procedure.

Adding `dl.google.com` is one possible future decision, not an action authorized here. If publisher-controlled evidence cannot establish the route, the toolchain remains blocked.

#### G2 — Metadata-only graph closure

After a separately approved and verified toolchain exists, create an isolated module workspace containing no candidate code and no source data. Use only reviewed module metadata to calculate the selected graph. The result must classify every module as:

- imported runtime/build dependency;
- test-only dependency of the experimental harness;
- dependency present only in another module's tests or tooling;
- module-graph input not linked into the artifact;
- unresolved.

The current discovery set requiring explicit disposition is:

- `github.com/stretchr/testify@v1.11.1`;
- `github.com/davecgh/go-spew@v1.1.1`;
- `github.com/kr/pretty@v0.3.0`;
- `github.com/pmezard/go-difflib@v1.0.0`;
- `gopkg.in/check.v1@v1.0.0-20201130134442-10cb98267c6c`;
- `gopkg.in/yaml.v3@v3.0.1`;
- `golang.org/x/tools@v0.36.0`;
- `golang.org/x/mod@v0.27.0`.

Graph computation may identify further modules. Any new member stops the metadata pass and returns for review before payload acquisition.

#### G3 — Graph approval before ZIP acquisition

Present the authoritative graph, selection reasons, exact proxy and checksum URLs, content hashes, licenses, security routes, and expected cache files. Only an explicitly approved graph may be acquired. The final offline `go.sum`, module inventory, and cache count must reconcile exactly.

### Required review

Supply chain owns toolchain/module provenance and checksums; licensing owns the complete graph; security reviews environment variables, proxy/sumdb boundaries, and absence of credential/private-module fallback; quality independently reconciles graph and cache counts; the orchestrator enforces the stop between G2 and G3.

## Workstream A — age verification

### Accepted problem

The age 1.3.2 archive matched the accepted SHA-256 and had a separate Sigsum proof. The proof was not verified because no reviewed verifier existed. The extracted macOS binary carried only an ad-hoc linker signature and no publisher identity.

### Candidate remediation routes

| Route | Boundary | Required evidence | Current disposition |
|---|---|---|---|
| A1 — Verify the Sigsum proof | Add one exact, independently bootstrapped verifier and the publisher's documented trust policy solely to validate the already identified age archive | Verifier source/artifact/version/hash/signature; complete dependencies; Sigsum policy/key/log identity; reproducible verification command and expected result; license; offline operation | Preferred proof route if its own trust chain is smaller and reviewable; not authorized |
| A2 — Publisher-authenticated alternate distribution | Use another official artifact whose publisher identity can be independently validated on this host | Exact route, signature identity, hash, archive layout, license, and no-installer/no-network execution behavior | Alternative only; not established |
| A3 — Remove the age probe from Phase 3 | Preserve backup/restore testing without this encryption implementation, or leave encryption-specific evidence Unproved | Traceability impact, replacement contract if any, and explicit list of gates that remain Unproved | Scope decision requiring review; not a stack decision |

### Bootstrap rule

The verifier cannot be trusted merely because it verifies age. Its own origin, integrity, signature/proof, dependencies, and license must be established independently. Acquiring a verifier is a manifest change and requires a separate approval.

No archive execution, key generation, keychain use, or synthetic backup creation occurs during remediation acquisition.

## Workstream O — PostgreSQL image-content route

### Accepted problem

The OCI index and `linux/arm64/v8` manifest are immutably identified and independently hashed. Blob retrieval redirected from the accepted registry host to `production.cloudfront.docker.com`; the accepted allowlist instead named `production.cloudflare.docker.com`. The redirect was correctly rejected. No config or layer content was acquired.

### Candidate remediation routes

| Route | Boundary | Evidence required before selection | Current disposition |
|---|---|---|---|
| O1 — Approve the observed registry CDN route | Continue Docker Registry content retrieval only for the already frozen index/platform manifest and descriptor digests | Publisher-controlled evidence tying the registry service to the exact CDN host; redirect/credential behavior; no account requirement; TLS/host review; exact blob inventory; cost/terms; stop on any further host | Most direct route; host addition is not authorized by this proposal |
| O2 — Registry endpoint without external redirect | Obtain the same immutable blobs through a publisher-supported endpoint that stays within a newly reviewed host set | Primary documentation, exact API behavior, digest identity with accepted descriptors, and no mutable-tag fallback | Alternative only; not established |
| O3 — Reviewed content-addressed mirror | Use a separately trusted mirror only if it provides byte-identical blobs for the accepted descriptors | Mirror ownership, synchronization/provenance, immutable addressing, independent digest verification, license/terms, account/cost, and complete host list | Higher trust burden; not preferred without strong evidence |
| O4 — Defer PostgreSQL-backed evidence | Keep the database-backed candidate and affected tests Unproved | Explicit impact on gates and scorecard | Valid scope reduction; cannot be represented as equivalent evidence |

### Content acceptance conditions

Any future route must request only the accepted arm64 config digest and thirteen recorded layer digests. Every blob must match its descriptor before decompression. The cache inventory must reconcile one config plus thirteen layers, and the image must be addressed by platform-manifest digest rather than tag. Package/license inventory occurs offline and cannot silently pull vulnerability databases or helper images.

No image import, Podman initialization, container creation, database startup, or service listener is part of content acquisition.

## Workstream C — Offline-completeness evidence

### Objective

Prove that the exact reviewed prerequisites can be installed or consumed from the verified local cache with all external network paths unavailable, without yet building candidate code, starting a service, or running a prototype.

### Preconditions

Offline-completeness work cannot begin until P, G, A, and O each have an approved disposition. A deferred component must be explicitly removed from the claimed completeness scope. All retained inputs must have reconciled hashes, signatures/proofs, licenses, and dependency inventories.

### Proposed evidence sequence

1. Create a fresh owner-only sentinel-bearing disposable root outside the repository.
2. Copy only reviewed cache files and manifests into the root; verify every copy against the accepted checksum inventory.
3. Disable external network access with a separately reviewed mechanism and prove denial using fixed non-sensitive canaries.
4. Resolve Python requirements from the local wheel cache using exact hashes and no index or dependency discovery.
5. Verify the complete Go module cache and selected graph with network lookup disabled; no compile or test command is permitted.
6. Verify every OCI config/layer digest and prove the platform manifest is locally complete without importing or starting the image.
7. Verify standalone-tool archives and signatures/proofs without executing their product functionality.
8. Reconcile file count, component count, lock/module/image inventory, licenses, and SBOM inputs.
9. Attempt controlled negative cases: one missing cache item, one wrong hash, one undeclared component, and one network request. Each must stop without fallback.
10. Remove only the exact disposable verification root after retaining normalized evidence, then prove no process, listener, credential, key, service, or generated product state remains.

If proving local resolution would necessarily install a tool, that installation must be separately described and approved first. This proposal itself authorizes neither installation nor execution.

### Pass criteria

Offline completeness passes only if:

- the declared scope is exact and contains no deferred-but-required component;
- all cache files verify independently and all ecosystem inventories reconcile;
- resolution succeeds without DNS, HTTP, registry, proxy, update, telemetry, credential-helper, or account access;
- every negative case fails closed with no alternate source or mutable fallback;
- no candidate code is built and no service, image, database, fixture, credential, key, or listener is created;
- cleanup returns to the pre-verification state.

This would close only the acquisition/offline-cache portion of Gate 2. It would not verify runtime isolation, parser safety, rendering, source immutability, or cleanup under candidate execution.

## Proposed remediation stages

| Stage | Permitted work | Required stop |
|---|---|---|
| R0 — Proposal review | Review this document only | Current stage; no network acquisition |
| R1 — Primary-evidence route dossiers | Collect and present publisher-controlled documentation for P, G, A, and O; propose exact manifest/allowlist changes without applying them | User reviews routes and rejects or approves each independently |
| R2 — Revised acquisition manifest | Produce a complete proposed diff naming exact hosts, artifacts, verifiers, graphs, signatures, side effects, licenses, cache inventory, and rollback | User explicitly approves before any artifact request |
| R3 — Bounded reacquisition | Acquire only the approved route, one workstream at a time; stop after each workstream's evidence | User reviews evidence before the next workstream |
| R4 — Offline-completeness demonstration | Run only the approved cache-verification sequence with no candidate build/test/service | User reviews result and decides whether Checkpoint A can close |

Approval of one stage does not imply approval of the next. A host, component, redirect, verifier, side effect, license issue, account request, cost, telemetry path, or mutable fallback not named in the approved stage causes an immediate stop.

## Records and review ownership

Each workstream must update the acquisition, redirect, integrity/signature, dependency, license, uncertainty, gap, disagreement, and rejection records. Rejected alternatives remain visible with reasons; absence of evidence remains `Unproved`, not zero risk.

Mandatory reviewers are:

- security/privacy;
- maintenance/supply chain;
- licensing/cost;
- quality/review;
- orchestrator.

Preservation/corpus review is required for any route that could write to source-like paths, alter backup semantics, or blur raw and derived state. Product/UX and research/AI remain informed observers because this remediation does not exercise product behavior.

## Explicit non-authorization

This proposal does not authorize:

- retrying an artifact request or contacting a new host;
- editing the accepted allowlist or dependency manifest;
- installing, importing, or executing a retained or rejected artifact;
- acquiring the eight discovered Go modules or a Sigsum verifier;
- initializing Podman or another container runtime;
- pulling/importing an OCI image, creating a container/network/volume, or starting PostgreSQL;
- creating a fixture, credential, key, listener, service, database, candidate file, prototype, build, test, or generated SBOM;
- accessing an account, real correspondence, live archive, cloud AI, telemetry, or production infrastructure;
- beginning Checkpoint B, selecting a stack, creating a stack-selection ADR, committing this proposal, or pushing.

## Review request

Review is requested on:

1. the P1–P4, A1–A3, and O1–O4 alternative boundaries;
2. the staged G1–G3 graph-closure method;
3. the offline-completeness definition and negative cases;
4. the R0–R4 approval sequence;
5. whether the next authorized action should be limited to R1 primary-evidence route dossiers.

Until that review is explicit, Checkpoint A remains open and no remediation activity begins.
