# Gate-2 Baseline Evidence

**Status:** Accepted
**Review date:** 2026-09-18
**Observed:** 2026-09-17 on the local Phase-3 evaluation host
**Method:** Read-only repository and tool inventory; no package acquisition, installation, service start, fixture creation, or test execution.

## Evidence records

### G2-E001 — Accepted Gate-1 commit boundary

- Commit: `689448f Accept Phase-3 Gate-1 experiment design`
- Commit content: exactly eight files under `docs/phase-3/`
- Diff: 1,026 insertions, zero deletions
- Immediate post-commit state: clean index and working tree
- Whitespace: staged and unstaged checks passed
- Branch state immediately after commit: `main` six commits ahead of `origin/main`
- Remote action: no push

The committed files are documentation only. The commit contains no fixture, prototype, dependency, service configuration, credential, key, generated artifact, or executable entry point.

### G2-E002 — Repository scope

The physical working path and Git top level both resolve to:

```text
/Users/bogac/dev/forgejo/mneme
```

The repository and `.git` directory are ordinary directories owned by the current user. This establishes the reviewed project boundary; it does not grant any experiment permission outside it.

### G2-E003 — Tracked-content scan

At observation time Git reports 43 tracked files. A tracked-path scan found none matching:

- `experiments/`, `fixtures/`, `src/`, `app/`, `vendor/`, `node_modules/`, or `.venv/` trees;
- `go.mod`, `go.sum`, requirement/lock manifests, `package-lock.json`, `Cargo.lock`, `Dockerfile`, `Containerfile`, or Compose files;
- `.env` files, PEM/private-key/certificate files, `.credentials/`, or `.mneme-secrets/`.

The `experiments/` directory and proposed `experiments/phase-3/` root do not exist.

This is path-level absence evidence. It does not claim that arbitrary document prose is a secret scanner or that the host outside the repository was searched.

### G2-E004 — Ignore-policy review

The current `.gitignore` excludes named local/secret and generated-state locations, virtual environments, caches, logs, SQLite transient files, editor swaps, and OS metadata. Its comments explicitly preserve visibility of project and test fixtures unless they are deliberately placed in a named local directory.

Git reported no ignore match for these proposed useful paths:

```text
experiments/phase-3/fixtures/releases/phase3-corpus-v0.1/manifest.json
experiments/phase-3/cand-001/requirements.lock
experiments/phase-3/cand-003/go.sum
experiments/phase-3/dependency-evidence/sbom/cand-001.spdx.json
experiments/phase-3/evidence/test-results.jsonl
```

No `.gitignore` change is needed for Gate 2. Disposable environments, databases, keys, raw logs, caches, containers, and downloads remain outside the repository under a validated temporary root.

### G2-E005 — Installed host/toolchain baseline

| Component | Observed identity | Gate-2 posture |
|---|---|---|
| Host architecture | Apple Silicon `arm64` | Recorded |
| macOS | 26.6.2 | Recorded |
| Git | Apple Git 2.54.0 | Recorded |
| Python | CPython 3.14.6 | Installed; no Phase-3 environment created |
| SQLite | 3.53.3, FTS5 enabled through Python | Installed; no Phase-3 database created |
| Python-reported OpenSSL | 3.6.3 | Recorded only |
| Xcode | 27.0, build 27A266a | Installed; no Phase-3 project/test bundle created |
| Swift | Apple Swift 6.4, `swiftlang-6.4.0.34.1` | Installed; no build run |
| macOS SDK | 27.0 | Installed |
| SafariDriver | Included with Safari 26.6.2, build 21624.5.1.11.3 | Installed; not started |

The baseline matches the accepted Gate-1 dependency document. A version change before use requires evidence refresh and review.

### G2-E006 — Absent proposed components

Command discovery found these absent:

| Component | Why absence matters |
|---|---|
| Go | EXP-C003 and the independent Go verifier cannot build or run |
| Podman | Linux isolation, internal network, ephemeral PostgreSQL, and resource-limit evidence cannot be produced |
| Docker | Confirms no Docker runtime is being used as an undeclared substitute |
| PostgreSQL commands/service | No database or dump/restore activity can occur |
| age | No backup-encryption key or artifact can exist |

Absence is the expected safe baseline, not a failure. It means dependency integrity and runtime isolation remain Blocked until separately approved acquisition and verification.

### G2-E007 — Available safety-observation primitives

The host currently provides `shasum`, `openssl`, `tar`, `mktemp`, `stat`, `realpath`, `lsof`, `netstat`, and `/usr/bin/sandbox-exec`.

- Hash, path, metadata, temporary-root, process-listener, and archive observations can be made without adding a package.
- `sandbox-exec` presence is not accepted as the sole parser-isolation proof; its behavior would be supplemental evidence only.
- The inventory does not execute untrusted content or assert that a tool is secure merely because it is present.

### G2-E008 — External-state boundary

No external account was authenticated, enumerated, or accessed. No real correspondence or live archive path was inspected, statted, searched, hashed, or imported. No cloud AI, hosted model, telemetry endpoint, analytics service, external embedding service, production host, or public listener was used. No email was sent and no source system was mutated.

Primary release/package pages used during Gate-1 research did not receive project data and did not download or install an artifact. Gate-2 shell evidence was local and read-only.

## Evidence limitations

This baseline cannot yet prove:

- fixture synthetics or allowlists, because no fixture exists;
- source read-only enforcement, because no fixture or worker exists;
- network denial, because the proposed isolation runtime is absent;
- resource limits, because no worker process exists;
- dependency integrity, SBOMs, or licenses beyond the reviewed proposal, because no artifact was acquired;
- log, cache, temporary-file, key, credential, service, restore, or cleanup behavior, because no experimental runtime state exists.

Those limitations are recorded as blockers in the control matrix rather than inferred away.
