# Synthetic-Only Safeguards

**Status:** Accepted
**Review date:** 2026-09-17
**Policy:** Fail closed. A blocked safeguard is a blocked experiment, never a warning-only pass.

## Preflight sequence

Every executable entry point must complete these checks in order before reading fixture payloads or creating candidate state:

1. Resolve the repository root from Git and require the experiment path to equal `<repo>/experiments/phase-3`.
2. Resolve every input with operating-system realpath semantics and require it to be beneath `fixtures/releases/phase3-corpus-v0.1/`.
3. Reject symlinks, hard-link count greater than one for regular payload files, device files, sockets, FIFOs, mount points, absolute paths, `.`/`..` components, and case-colliding paths.
4. Verify the release and package `SYNTHETIC_ONLY.json` markers and require `synthetic: true`, `contains_real_data: false`, and `external_authority: false`.
5. Match the requested fixture IDs against the frozen release manifest; reject unknown, duplicate, extra, missing, or unsupported-version entries.
6. Independently verify package membership, byte lengths, source hashes, evidence hashes, and expected-truth hashes.
7. Create a fresh `/tmp/mneme-phase3.<run-id>/` root and its `MNEME_PHASE3_DISPOSABLE.json` sentinel; reject an existing or nonempty root.
8. Record the environment, dependency-lock identity, image digests, network profile, limits, and selected acceptance tests.
9. Prove source input is read-only from the worker and candidate execution contexts by an expected-failure write probe.
10. Prove the required network boundary and resource controls are active. If they cannot be established, stop before parsing, rendering, indexing, or restoring.

The preflight command accepts no arbitrary input path, URL, account name, provider credential, archive path, or database connection string. Fixture release, candidate, and test selection are enumerated values.

## Real-data exclusion

- No command accepts a home-directory mail path, browser profile, provider export location, cloud drive, removable archive, user-selected folder, or environment-provided source path.
- Environment variables cannot override input, output, credential, network, or archive roots.
- The string forms of the live-project path, home mail locations, and common provider-export names are denied as resolved inputs even when a symlink or mount attempts to disguise them.
- A fixture content review allows only reserved domains and a reviewed fictional-name list. Unexpected addresses, account IDs, phone-like values, user-home paths, or token formats quarantine the release.
- The experiments never inventory, stat, hash, search, or otherwise inspect the live archive or real correspondence—not even metadata-only.

## Source immutability controls

- Released fixture payloads are tracked and treated as immutable inputs.
- Parser workers receive one source item through a read-only mount and a separate empty output mount.
- Candidate harnesses consume only independently verified copies or read-only mounts; no source path is opened for write.
- Before and after every applicable test, independent verifiers recompute source item and package digests.
- A write attempt, changed byte, changed mode where mode is in scope, added file, missing file, or unexplained timestamp dependency stops downstream claims and records an integrity failure.
- Deduplication, junk classification, annotation, parsing, rendering, indexing, export, backup, restore, and rebuild affect derived or disposable state only.

## Network boundary

### Acquisition window

Dependency acquisition is the only network-enabled Phase-3 operation. It must:

- run separately before fixtures, candidate services, databases, keys, or credentials exist;
- contact only the official hosts listed in the reviewed dependency manifest;
- record requested URL, resolved version, artifact name, byte length, digest, and verification result without cookies or account authentication;
- produce a complete local cache, lock files, image digests, module sums, and acquisition log;
- end before any build or test begins.

If a component redirects to an undeclared host, requires an account, emits telemetry, runs a post-install network action, or cannot be integrity-checked, acquisition stops and that component remains unapproved.

### Build and execution window

- Builds use only the verified local cache and run with external network denied.
- Parser workers use a rootless container with `--network none`.
- Candidate services and the ephemeral database use a run-specific Podman `--internal` network, no published port, and disposable synthetic credentials.
- A service required by a rendering probe may bind an operating-system-assigned port on `127.0.0.1` or `::1` only; binding any other address is a hard failure.
- The safe-render probes route permitted observations only to a run-specific loopback canary. Reserved remote URLs must produce no DNS lookup or external connection.
- The deterministic model-router stub is in-process or loopback-only, owns no credentials or tools, and has no cloud fallback.
- Telemetry, analytics, crash upload, update checks, remote fonts/images/styles, package-manager calls, and external embeddings are disabled.

On macOS, Podman 6.1.2 is proposed only as a rootless Linux test harness. The machine must be named `mneme-phase3`, and its use does not approve Podman, containers, Docker, or any production deployment architecture. If the internal/no-network behavior cannot be independently observed, AT-S06 and the affected gate remain `Still Unproved`.

## Worker isolation profile

The parser worker must run as a non-root numeric user with:

- read-only root filesystem;
- all Linux capabilities dropped;
- `no-new-privileges` enabled;
- default-deny seccomp refined only by observed, reviewed needs;
- no host PID, IPC, user, or network namespace sharing;
- one read-only input file, one bounded output mount, and a 16 MiB in-memory temporary filesystem;
- one CPU, 256 MiB memory, 32 processes, 10-second wall-clock timeout, 8 MiB aggregate output, 128 output files, nesting depth 32, 64 MiB expansion ceiling, and 20:1 expansion-ratio ceiling;
- no archive, database, repository, home directory, SSH agent, keychain, environment secret, or container socket mount.

These are experimental test limits, not production choices. Any limit change requires a reviewed diff and a reason tied to a fixture or false result.

## Rendering safeguards

- Plain text is always the baseline representation.
- Hostile HTML is never inserted into the application origin or a privileged native bridge.
- The web probe uses a sandboxed child context plus a policy equivalent to `default-src 'none'`; scripts, forms, plugins, navigation, remote images, fonts, styles, frames, workers, and storage are denied.
- The WebKit probe uses a nonpersistent data store, no script message handlers, no application bridge, denied navigation, and explicit scheme/resource policy.
- Links are displayed as untrusted evidence and never activated by the test harness.
- The loopback canary and process/network observation must record zero prohibited requests. Rendering success without network evidence is not AT-S01 or AT-S06 pass evidence.
- Original HTML bytes remain in the read-only source package and are not rewritten by sanitization.

## Credentials, keys, and authority

- Synthetic API/session tokens begin `mneme_test_`, authorize only the current disposable harness, and expire at run end.
- PostgreSQL uses a run-specific random password supplied through a temporary file, not a command line, tracked file, source fixture, manifest, or routine log.
- `age` keys are generated inside `credentials/`, protect only synthetic backups, and are deleted during cleanup after key-loss evidence is complete.
- Token-shaped fixture strings are never loaded into an authentication field and must be redacted as `[REDACTED_SYNTHETIC_TOKEN]` in logs.
- No OAuth flow, provider scope, Apple identity, keychain item, browser cookie, SSH key, cloud credential, or real certificate is used.

## Logging and evidence minimization

Routine logs may contain only run ID, fixture ID, source-item ID, test ID, timestamps, status, byte counts, digest prefixes of at least 12 hexadecimal characters, error class, and bounded diagnostic codes. They must not contain message bodies, addresses, headers, extracted text, attachment content, raw prompts, token-shaped strings, database passwords, encryption keys, or user-home paths.

Raw evidence remains in the sentinel-bearing temporary root until reviewed. Only normalized, redacted, requirement-linked evidence enters the repository. A redaction failure blocks evidence publication and causes cleanup after enough metadata is retained to reproduce the failure safely.

## Supply-chain safeguards

- Direct versions are fixed before acquisition; transitive versions and artifact hashes are frozen in lock/module-sum files before build.
- Binary and wheel hashes are verified before unpacking or installation.
- Container tags are never sufficient: the resolved multi-architecture and arm64 manifest digests must be recorded, and execution uses the immutable digest.
- Builds run without network and must fail if the cache is incomplete.
- SBOM, license, notice, build-script, native-code, and advisory evidence is produced before a candidate test result can support G-09.
- An unverifiable artifact, ownership ambiguity, unknown license, unexpected native extension, undeclared post-install action, or dependency graph drift stops the affected slice.

## Stop and escalation conditions

Stop immediately if any operation:

- encounters possible real correspondence, personal identifiers, account metadata, or a live-archive path;
- requests an account, external credential, paid service, cloud AI, hosted model, telemetry, public listener, or production resource;
- cannot prove source read-only, network denial, resource bounds, dependency integrity, or disposable output scope;
- writes outside the sentinel-bearing run root or named experimental evidence paths;
- causes hostile content to execute, navigate, load a remote resource, or gain a native bridge;
- alters source bytes, loses user-controlled history, accepts fabricated citations, or treats derived state as authoritative;
- would send email, mutate a source system, select a stack, or create a stack-selection ADR.

The result is `Blocked` or `Fail` according to the accepted matrix. The control is never weakened merely to complete a run.
