# Exact Experiment Layout

**Status:** Accepted
**Review date:** 2026-09-17
**Creation state:** Layout specification only; none of the paths below exists yet.

## Root boundary

All future Phase-3 implementation and generated review evidence must be under `experiments/phase-3/` or a run-specific operating-system temporary root. Nothing is added to a production application tree. No path may point to the live archive.

```text
experiments/phase-3/
├── README.md
├── SYNTHETIC_ONLY
├── contracts/
│   ├── preservation-profile-v0.1.md
│   ├── preservation-manifest-v0.1.schema.json
│   ├── provenance-event-v0.1.schema.json
│   ├── export-profile-v0.1.md
│   ├── export-record-v0.1.schema.json
│   ├── worker-protocol-v0.1.md
│   ├── worker-request-v0.1.schema.json
│   ├── worker-result-v0.1.schema.json
│   ├── citation-profile-v0.1.md
│   ├── search-cases-v0.1.json
│   ├── privacy-boundary-v0.1.md
│   └── backup-profile-v0.1.md
├── fixtures/
│   ├── README.md
│   ├── releases/
│   │   └── phase3-corpus-v0.1/
│   │       ├── SYNTHETIC_ONLY.json
│   │       ├── manifest.json
│   │       ├── expected-truth.jsonl
│   │       └── packages/
│   │           └── CORP-001-... through CORP-035-.../
│   └── generators/
│       ├── README.md
│       └── resource-boundary-descriptors/
├── shared/
│   ├── verifier-python/
│   ├── verifier-go/
│   ├── parser-worker/
│   ├── model-router-stub/
│   ├── network-canary/
│   ├── semantic-export-comparator/
│   └── evidence-normalizer/
├── cand-001/
│   ├── README.md
│   ├── requirements.in
│   ├── requirements.lock
│   ├── harness/
│   └── tests/
├── cand-003/
│   ├── README.md
│   ├── go.mod
│   ├── go.sum
│   ├── harness/
│   ├── swift-safe-render/
│   └── tests/
├── isolation/
│   ├── README.md
│   ├── Containerfile.worker
│   ├── seccomp.worker.json
│   └── podman-profiles/
├── dependency-evidence/
│   ├── acquisition-log.jsonl
│   ├── artifacts.sha256
│   ├── sbom/
│   ├── licenses/
│   ├── notices/
│   └── advisories/
├── evidence/
│   ├── README.md
│   ├── environment.json
│   ├── test-results.jsonl
│   ├── preservation/
│   ├── migration/
│   ├── rebuild/
│   ├── isolation/
│   ├── privacy/
│   ├── recovery/
│   ├── search-citations/
│   └── supply-chain/
└── scripts/
    ├── preflight
    ├── acquire
    ├── run
    ├── collect-evidence
    └── cleanup
```

Names under `shared/`, `cand-001/`, and `cand-003/` describe future experimental implementation boundaries, not language package or production module names.

## Runtime roots

Every run receives an unpredictable identifier and a fresh root created from the fixed template `/tmp/mneme-phase3.<run-id>/`. The root must contain a generated `MNEME_PHASE3_DISPOSABLE.json` sentinel before any service or write-capable process starts.

```text
/tmp/mneme-phase3.<run-id>/
├── MNEME_PHASE3_DISPOSABLE.json
├── input/          # fixture copy or read-only bind target
├── work/           # disposable candidate and parser state
├── output/         # bounded worker output
├── db/             # disposable SQLite/PostgreSQL state
├── backup-a/       # simulated failure domain A
├── backup-b/       # simulated failure domain B
├── credentials/    # disposable synthetic secrets and keys
├── logs/           # redacted local logs
└── raw-evidence/   # reviewed before any canonical evidence is copied
```

No virtual environment, module cache, database volume, key, credential, raw log, or temporary output is stored in the repository. Canonical evidence copied into `experiments/phase-3/evidence/` must be redacted, deterministic where possible, and contain no source bodies, addresses, token-shaped fixture values, attachment contents, or secrets.

## Process and network topology

```text
fixture release (read-only)
        |
        +--> independent verifier A (no network)
        +--> independent verifier B (no network)
        +--> parser worker (read-only input, scratch output, network none)
        |
        +--> candidate harness ---- private internal test network ---- ephemeral DB
                  |
                  +--> deterministic router/citation stub (local only)
                  +--> safe-render probe ---- loopback canary only
```

- The parser worker always uses `--network none` and never joins the database network.
- Candidate-to-database traffic uses a run-specific internal network with no public port and no default external route.
- A browser or WebKit probe may reach only a run-specific loopback listener. Remote-looking fixture URLs use reserved domains and must be blocked before resolution or connection.
- Dependency acquisition is a separate, logged step. No candidate process, fixture generator, test, renderer, or worker runs during the acquisition window.
- No listener binds to `0.0.0.0`, `::`, a LAN address, or a public interface.

## Candidate boundary

### `EXP-C001`

- One Python virtual environment inside the temporary run root.
- One SQLite database and FTS5 index inside `db/cand-001/`.
- A minimal Django test service bound to an operating-system-assigned loopback port only when a rendering test requires HTTP.
- Python standard-library test execution; no separate test framework.
- The shared parser worker remains outside the Django process and has no database or archive write path.

### `EXP-C003`

- One Go module cache inside the temporary run root and one built test harness.
- One ephemeral PostgreSQL 18.6 service on the private internal test network, with a run-specific data volume.
- One minimal Go command/API bound only inside the internal network or to an operating-system-assigned loopback port for the Swift probe.
- One Xcode test bundle for a minimal SwiftUI/WebKit rendering probe; no Swift package dependencies and no distributable app.
- The shared parser worker remains a separate process/container with no database or archive write path.

## Tracked and disposable material

| Class | Location | Git policy | Cleanup policy |
|---|---|---|---|
| Contracts, fixture generators, source code, test definitions | `experiments/phase-3/` | Tracked after review | Retained as experiment evidence |
| Released fixture bytes and expected truth | `fixtures/releases/phase3-corpus-v0.1/` | Tracked and immutable after release | Never changed in place |
| Lock files, SBOMs, licenses, notices | `dependency-evidence/` and candidate roots | Tracked | Retained with evidence |
| Sanitized test results and reports | `evidence/` | Tracked after review | Retained with evidence |
| Environments, caches, DBs, raw logs, keys, credentials, containers, volumes | `/tmp/mneme-phase3.<run-id>/` and run-labeled Podman state | Never tracked | Removed by the approved cleanup procedure |
| Download cache | Run-specific temporary root | Never tracked | Removed after hashes/SBOM evidence is retained |

No broad `.gitignore` pattern is proposed. Disposable files are kept outside the repository, so useful fixtures, tests, lock files, and evidence cannot be hidden accidentally.

## Gate-1 acceptance conditions

- Every future path has a single stated purpose and retention class.
- The experiment root remains visibly separate from product code and production configuration.
- Runtime writes are limited to a sentinel-bearing temporary root and explicitly labeled ephemeral container state.
- The topology has no route to an account, live archive, cloud AI, telemetry service, public listener, or production host.
- Any implementation change to this layout is reviewed before use.
