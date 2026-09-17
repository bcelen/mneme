# Gate-2 Post-Approval Sequence

**Status:** Accepted
**Review date:** 2026-09-18
**Current pause:** Before acquisition, installation, service startup, fixture creation, generated artifact creation, prototype code, or test execution.

## Principle

Gate 2 requires two evidence checkpoints because the current boundary forbids the very state needed to verify runtime controls. Approval of this document would authorize only the next checkpoint; it would not authorize candidate prototypes or acceptance tests.

## Checkpoint A — Dependency acquisition and integrity

After explicit approval, acquire only the artifacts in the accepted dependency manifest, in this order:

1. record a fresh clean Git status and exact host/toolchain identities;
2. create a download-only temporary root with a disposable sentinel and inventory;
3. acquire the exact Python wheels, Go archive/modules, Podman package, PostgreSQL image metadata/content, and age archive from the reviewed allowlist;
4. record every URL/redirect, version, filename, byte length, hash, signature/proof status, and immutable OCI index/platform digest;
5. reject any unknown host, package, module, version, mutable-only image, installer side effect, account request, telemetry, or undeclared transitive component;
6. freeze `requirements.lock`, `go.sum`, artifact checksums, module/image inventories, SBOM inputs, license/notice sources, and advisory routes;
7. disconnect the acquisition network path and prove required artifacts are locally complete;
8. present the full acquisition/integrity diff and evidence for review before build or service startup.

Allowed state at the end of Checkpoint A is limited to verified download cache, exact tool installations required by the accepted manifest, lock/module/checksum metadata, and dependency evidence. No fixture, database, Podman machine, container, candidate code, renderer, credential, key, or test result may exist.

## Checkpoint B — Empty safety-harness verification

Only after Checkpoint-A evidence is reviewed may the empty safety harness be established:

1. create a fresh sentinel-bearing runtime root and inventory with no fixture content;
2. initialize the named `mneme-phase3` Podman machine with reviewed CPU/memory/disk bounds and no automatic startup;
3. create an empty run-labeled `--internal` network and a separate no-network container context;
4. inspect namespaces, capabilities, seccomp, no-new-privileges, root filesystem, mounts, process limits, resource ceilings, socket exposure, and listener bindings using inert operating-system probes only;
5. verify that no source, repository, home, keychain, agent socket, container socket, account credential, or unrelated host path is mounted;
6. verify no-network and internal-network denial with non-sensitive fixed canaries; do not contact a provider, model, telemetry, or public application service;
7. verify loopback-only binding policy with an inert empty listener if needed, never a candidate or database service;
8. verify exact-target, label, sentinel, process, network, volume, machine-stop, and idempotent cleanup behavior;
9. return to a clean runtime state and present all normalized evidence for review.

Checkpoint B is safety-control verification, not a prototype or acceptance test. It contains no fixture bytes, parser behavior, preservation logic, database, candidate service, UI, routing stub, synthetic credential, encryption key, or product data.

## Checkpoint C — Fixture-release proposal

Only after the empty safety harness is reviewed may fixture generator and release work be proposed. Before any fixture bytes are created, present:

- exact generator file list and review ownership;
- allowed fictional-name/address/domain vocabulary;
- all 35 package recipes and expected-truth schemas;
- inert hostile-artifact construction rules;
- resource-boundary descriptor limits;
- synthetic-data and accidental-personal-data review procedure;
- release hashing, immutability, quarantine, and correction workflow.

Fixture creation is not authorized by Gate-2 approval alone.

## Evidence required to mark Gate 2 passed

Gate 2 can be proposed as passed only when:

- Checkpoint-A artifacts are exact, independently integrity-checked, fully inventoried, licensed, and locally complete;
- acquisition is demonstrably separate from offline build/test execution;
- Checkpoint-B filesystem, process, privilege, network, listener, resource, inventory, and cleanup controls are Verified;
- no account, real correspondence, live archive, cloud AI, telemetry, production resource, public listener, or source mutation occurred;
- all raw evidence is redacted and normalized without hidden generated state;
- specialists review their assigned controls and disagreements remain explicit;
- the repository contains only reviewed documentation/evidence changes and no unauthorized implementation.

Even a passed Gate 2 would authorize no stack selection and no real-data work. Gate 3 prototype implementation remains a later explicit boundary under the accepted Phase-3 plan.

## Rollback

Checkpoint A removes only the exact sentinel-bearing download cache after retaining reviewed hashes/licenses; installed tools remain unless separately authorized for uninstall. Checkpoint B stops and removes only run-labeled empty safety resources and the named experimental machine according to the accepted cleanup contract. No global prune, broad recursive removal, Git reset, or unrelated process termination is permitted.

Any mismatch or escape stops the sequence, records the control as Blocked or Fail, cleans only validated disposable state, and returns for user direction.
