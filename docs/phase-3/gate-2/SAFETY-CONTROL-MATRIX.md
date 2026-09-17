# Gate-2 Safety-Control Matrix

**Status:** Accepted
**Review date:** 2026-09-18
**Rule:** Every execution-critical control must be Verified before fixture creation, candidate implementation, service startup, or test execution. Designed and Blocked are not pass.

## Repository and data boundary

| ID | Control | Current evidence | Status | Required proof before use | Failure action |
|---|---|---|---|---|---|
| G2-C01 | Correct repository boundary | G2-E002 resolves Git and physical roots to the Mneme repository | Verified | Recheck at every entry point | Stop on mismatch |
| G2-C02 | Documentation-only starting state | G2-E001/E003: accepted docs commit; no experiment/code/dependency paths | Verified | Recheck tracked and untracked state before acquisition and execution | Stop and review unexpected file |
| G2-C03 | No accidentally hidden useful artifacts | G2-E004: fixture, lock, module, SBOM, and result paths are not ignored | Verified | Repeat after any ignore-file change | Stop until useful path is visible |
| G2-C04 | No real-data path or arbitrary input | Accepted safeguards prohibit path arguments and environment overrides; no enforcing entry point exists | Designed | Review preflight implementation; negative path-resolution checks against outside, symlink, mount, and unknown package cases | Stop before any read |
| G2-C05 | Synthetic fixture identity | Exact marker/manifest contract accepted; no release exists | Blocked | Independent review of all 35 generated package markers, reserved domains, expected truth, and release hashes | Quarantine release; no downstream work |
| G2-C06 | Live archive and account exclusion | G2-E008; no account or real/live path touched | Verified for work so far | Maintain no-auth/no-real-path policy; preflight must have no general source path or provider option | Stop and request new authority |

## Dependency and build boundary

| ID | Control | Current evidence | Status | Required proof before use | Failure action |
|---|---|---|---|---|---|
| G2-C07 | Exact direct dependency pins | Accepted dependency manifest names exact proposed versions and known artifact hashes | Verified as design input | Acquisition log must match every version/artifact exactly | Reject drift |
| G2-C08 | Complete transitive dependency graph | Published Python and pgx requirements documented; nothing acquired | Blocked | Frozen `requirements.lock`, `go.sum`, Go module graph, OCI package inventory, and reconciled counts | No build |
| G2-C09 | Artifact provenance and integrity | Official sources and known hashes documented; missing Podman/PostgreSQL immutable digests remain explicit | Blocked | Record URL, size, SHA-256/ecosystem checksum, signature/proof, OCI index and arm64 digests before unpack/install | Quarantine artifact |
| G2-C10 | License/notice review | Proposed license postures documented; no acquired license set or image inventory | Blocked | SPDX inventory, notices, unresolved-license report, and reviewer signoff | No build/use |
| G2-C11 | Offline build completeness | Acquisition/execution separation designed; no cache or build exists | Blocked | Disable network and prove both candidate dependency checks/build prerequisites resolve from verified local cache | No build |
| G2-C12 | Supply-chain failure path | AT-S09 and stop conditions mapped; no executable gate exists | Designed | Demonstrate wrong hash, graph drift, unsigned/unverifiable artifact, and missing-cache failures before candidate build | Quarantine and record Fail/Blocked |

## Filesystem and process boundary

| ID | Control | Current evidence | Status | Required proof before use | Failure action |
|---|---|---|---|---|---|
| G2-C13 | Fresh disposable root | Exact `/tmp/mneme-phase3.<run-id>/` and sentinel contract accepted; no root exists | Designed | Create one empty unpredictable root; validate owner, type, permissions, sentinel, realpath, non-mount, non-symlink, and cleanup inventory | Stop before state creation |
| G2-C14 | Source read-only | Read-only mount/open contract accepted; no fixture/runtime exists | Blocked | Expected-failure write probe from candidate and worker contexts plus before/after independent hashes | Stop before parsing/indexing |
| G2-C15 | Output confinement | Exact work/output/database/evidence paths accepted; no process exists | Designed | Attempt outside, absolute, traversal, symlink, hard-link, and undeclared-output writes using inert safety probes | Stop and treat escape as security failure |
| G2-C16 | Worker privilege isolation | Non-root/capability/seccomp/namespace profile accepted; Podman absent | Blocked | Inspect effective UID, capabilities, mounts, namespaces, seccomp, no-new-privileges, and absence of host sockets/secrets | No worker execution |
| G2-C17 | Resource ceilings | Fixed experimental CPU/memory/PID/time/output/temp/nesting/expansion limits accepted; runtime absent | Blocked | Inspect runtime configuration and execute only dedicated bounded safety probes after approval | No untrusted worker input |
| G2-C18 | Process ownership and cleanup | Inventory-first cleanup accepted; no runtime state exists | Designed | Demonstrate exact PID/executable/run-root matching and idempotent cleanup without global prune or broad deletion | Stop cleanup on ambiguity |

## Network, service, and rendering boundary

| ID | Control | Current evidence | Status | Required proof before use | Failure action |
|---|---|---|---|---|---|
| G2-C19 | Acquisition-only network window | Host allowlist and separation policy accepted; nothing acquired | Designed | Record allowlisted destinations, redirects, artifact-only traffic, start/end, and network-disabled transition | Stop on unknown host/account/telemetry |
| G2-C20 | Worker has no network | `--network none` contract accepted; Podman absent | Blocked | Namespace inspection plus denied DNS, loopback, LAN, and external attempts using non-sensitive canaries | No worker input |
| G2-C21 | Candidate/database internal network | Run-specific `--internal` topology accepted; Podman/PostgreSQL absent | Blocked | Prove no published port/default external route; only named candidate-to-DB path works | Stop services |
| G2-C22 | Loopback-only listeners | Policy names OS-assigned loopback ports; no listener has been started | Designed | Observe exact process/socket binding and reject `0.0.0.0`, `::`, LAN, or public bindings | Stop service immediately |
| G2-C23 | Safe-render network and active-content denial | Web/WebKit controls accepted; no probe exists | Blocked | Inspect configuration and show zero prohibited canary requests, navigation, storage, bridge, script, form, plugin, worker, or download activity | Stop rendering; record failure |
| G2-C24 | No cloud/telemetry fallback | Router vocabulary has no cloud route; no stub exists | Designed | Static review plus denied unrecognized-route and telemetry/update endpoint attempts | Stop and request authority |

## Credentials, logging, and evidence boundary

| ID | Control | Current evidence | Status | Required proof before use | Failure action |
|---|---|---|---|---|---|
| G2-C25 | Synthetic credentials only | Prefix, local authority, expiry, file delivery, and cleanup rules accepted; no credential exists | Designed | Generate only after runtime boundary passes; inspect scope/expiry without logging value; revoke and confirm denial | Stop on any external authority |
| G2-C26 | Disposable encryption keys only | age version and key handling designed; age absent and no key exists | Blocked | Generate in sentinel root after approval; verify backup-only scope, key-loss failure, and deletion | Stop on external keychain/account use |
| G2-C27 | Log minimization/redaction | Allowed fields and forbidden content accepted; no logger exists | Designed | Static format review and synthetic token/body/address redaction checks before retaining evidence | Quarantine raw evidence |
| G2-C28 | Cache/temp inventory | Exact runtime classes and temporary root accepted; no caches exist | Designed | Inventory every created path and reconcile against cleanup record | Stop on undeclared path |
| G2-C29 | Evidence integrity and separation | Evidence IDs/contracts accepted; no generated evidence exists | Designed | Hash raw-to-normalized evidence, record redaction, dependency/environment identities, and reviewer state | Do not publish unsupported result |
| G2-C30 | Complete cleanup | Accepted exact-target, label, sentinel, and no-prune procedure; nothing exists to clean | Designed | Perform one safety-state cleanup and prove no process/listener/container/volume/network/key/cache/temp root remains | Gate stays Blocked |

## Gate-2 readiness summary

| Status | Controls | Count |
|---|---|---:|
| Verified | C01, C02, C03, C06, C07 | 5 |
| Designed | C04, C12, C13, C15, C18, C19, C22, C24, C25, C27, C28, C29, C30 | 13 |
| Blocked | C05, C08, C09, C10, C11, C14, C16, C17, C20, C21, C23, C26 | 12 |

Gate 2 is not passed. The current evidence proves a controlled starting point and a closed scope, while preserving twelve genuine blockers. No blocker may be converted to Verified by document review alone.

## Mandatory review ownership

- Preservation/corpus: C04–C06, C14, C29.
- Security/privacy: C04, C06, C13–C30.
- Maintenance/supply chain: C07–C12.
- Licensing/cost: C09–C10 and acquisition cost/terms.
- Quality/review: evidence sufficiency and status calibration for all controls.
- Orchestrator: sequence enforcement, complete inventory, stop conditions, and unresolved disagreement.

Research/AI and product/UX review remain informed observers at Gate 2; their mandatory execution review begins when routing/citation and rendering behavior exists. No specialist may mark an unexecuted control Verified.
