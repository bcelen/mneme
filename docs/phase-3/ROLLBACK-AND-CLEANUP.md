# Rollback and Cleanup Procedure

**Status:** Accepted
**Review date:** 2026-09-17
**Scope:** Disposable Phase-3 synthetic state only. This procedure never targets the live archive, project root, home directory, production infrastructure, or unlabelled container state.

## Safety invariants

- Cleanup operates on an exact run ID recorded at preflight; no wildcard, recursive repository-root target, global prune, or unresolved environment variable is allowed.
- A filesystem target must resolve beneath `/tmp/mneme-phase3.<run-id>/`, contain a matching `MNEME_PHASE3_DISPOSABLE.json`, be owned by the current user, and not be a symlink or mount point.
- A container, volume, network, image, or Podman machine must carry the Phase-3 label/name and matching run ID. Unlabelled resources are reported and left untouched.
- Tracked fixtures, contracts, source code, lock files, SBOMs, licenses, and normalized evidence are not cleanup targets.
- Cleanup never invokes a provider revocation endpoint because all credentials are synthetic and local.
- Toolchain uninstall is not automatic. Removing installed Go, Podman, or age later requires a separate explicit instruction and the exact acquisition record.

## Run inventory

Before execution, `evidence/environment.json` and the temporary sentinel record:

- run ID and timestamps;
- exact temporary root;
- candidate/test selection;
- process IDs and loopback ports;
- Podman machine, container, volume, network, and image digests;
- SQLite/PostgreSQL state paths;
- synthetic credential/key identifiers, never secret values;
- dependency cache and build-output paths;
- expected cleanup actions.

Every created resource is appended to the run inventory immediately. Cleanup acts from this inventory rather than discovery by broad name matching.

## Normal cleanup order

1. Stop new work and mark the run `cleanup_started`.
2. Stop the loopback rendering service, network canary, candidate harnesses, parser workers, and database in reverse creation order.
3. Record final exit status and bounded diagnostics; terminate a remaining process only by the exact recorded PID after verifying its executable and run-root working directory.
4. Revoke and expire local synthetic sessions in each disposable candidate store.
5. Destroy the run-specific age identity and database password files after key-loss and restore evidence is complete.
6. Remove only the exact run-labeled Podman containers, then volumes, then internal network. Never use `podman system prune`, image prune, volume prune, or a global stop command.
7. Remove only images built by the run and carrying both `io.mneme.phase=3` and the matching run-ID label. Retain third-party cached images until acquisition/evidence reconciliation finishes; remove them later only by recorded digest.
8. Stop the named `mneme-phase3` Podman machine when no other recorded Phase-3 run uses it. Do not remove or modify a default or unrelated machine.
9. Independently verify that tracked fixture bytes still match the release manifest and that no repository file changed outside the reviewed experiment/evidence paths.
10. Copy only normalized, redacted evidence approved for retention into `experiments/phase-3/evidence/`.
11. Remove the exact sentinel-bearing temporary root using a cleanup implementation that refuses root, home, repository, empty, unresolved, symlinked, or mount-point targets.
12. Confirm no recorded process, loopback listener, container, volume, internal network, synthetic credential, key file, database state, or temporary root remains.
13. Record `cleanup_complete`, remaining tool installations/caches, and any exception requiring review.

## Failure or interruption cleanup

The same sequence is idempotent. Missing already-removed resources are recorded as absent, not recreated. If preflight, build, or a test fails before a resource class exists, later cleanup steps skip only the exact absent inventory entries.

If cleanup cannot verify a target, it stops and reports the target rather than broadening scope. A dirty repository is inspected; user or unrelated changes are preserved. No `git reset`, checkout-based overwrite, broad clean, or history rewrite is used.

## Isolation-escape or suspected compromise

If a worker, renderer, dependency, or service escapes its expected boundary:

1. stop the affected run and deny further network without executing content-controlled commands;
2. stop the exact run-labeled processes and containers;
3. preserve only process metadata, hashes, audit/network observations, and bounded logs needed for review; do not copy unsafe executable output into tracked evidence;
4. mark all derived state, build output, caches, database volumes, and synthetic credentials from the run untrusted;
5. verify tracked fixture and contract hashes from an independent process;
6. discard untrusted disposable state through the exact inventory procedure;
7. rotate synthetic credentials and keys if a later rerun is approved;
8. rebuild from verified fixture sources and reviewed dependency cache only after security/privacy review;
9. record the candidate test as `Fail` or `Blocked` and retain the Phase-2 no-selection conclusion.

No compromise drill touches real credentials, the live archive, backups, user devices, production services, or network infrastructure.

## Candidate rollback

- Candidate state is disposable. Rollback means stop services, preserve reviewed evidence, and delete the run-specific derived/database state.
- Source fixtures are never rolled back or rewritten; a fixture correction creates a new corpus release.
- A dependency update is tested in a new lock/module/image identity. Returning to the previous experiment uses its retained manifest and verified cache rather than mutating evidence.
- If one candidate is abandoned, its failure and reason remain in the evidence/rejection registers; shared contracts and the other candidate are not silently changed to hide the failure.

## Repository handoff checks

After each completed run or aborted build:

- whitespace checks pass for tracked changes;
- status lists only intended experiment/evidence files;
- no virtual environment, module cache, database, raw log, key, credential, socket, PID file, package download, container layer, or machine-specific absolute path is tracked;
- released fixture hashes match the corpus manifest;
- no evidence file contains message bodies, addresses, token-shaped values, attachment content, passwords, keys, or account identifiers;
- no commit or push occurs without a separate user instruction.

## Proof of removability

Phase 3 cannot satisfy its definition of done until one complete synthetic run is cleaned with this procedure and a fresh preflight demonstrates that no prior runtime state is required. Removing `experiments/phase-3/` from a clean checkout must affect only experimental artifacts and must not impair accepted project documentation or any live system.
