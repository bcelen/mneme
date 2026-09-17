# Checkpoint-A Cache and Cleanup Report

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18

## Disposable root

The exact acquisition root is:

`/tmp/mneme-phase3-checkpoint-a.H9KN5d`

It is owner-only with mode `0700` and carries `MNEME_PHASE3_DISPOSABLE.json`. It is outside the Mneme repository. At the evidence cutoff it occupies approximately 8.5 MB.

## Retained local cache

Twenty-five download-area files remain:

- three verified Python wheels;
- eighteen non-executable Go `.info`, `.mod`, and `.sumdb` records for six reviewed modules;
- one age Sigsum proof;
- one Podman published checksum file;
- one PostgreSQL OCI index;
- one PostgreSQL arm64 platform manifest.

The metadata area retains approximately fifty small records:

- independent pre-rejection and retained-cache checksum manifests;
- exact Python requirements lock and explicitly partial Go checksum file;
- artifact, redirect, graph, and cache inventories;
- PyPI JSON and wheel metadata;
- six Go, three Python, Podman, and age license records;
- Podman package metadata, payload list, and pre/post-install scripts;
- Podman package-signature and age code-signature reports;
- sanitized request/response metadata needed to reproduce the findings.

The age proof, Podman checksums, Go metadata, and OCI manifests are retained as non-executable evidence, not as approved install inputs.

## Removed or never-created state

The following acquired executable archives were removed after normalized evidence was captured:

- six Go module ZIP files;
- `podman-installer-macos-arm64.pkg`;
- `age-v1.3.2-darwin-arm64.tar.gz` and its temporary extracted binary.

The Go toolchain archive and PostgreSQL config/layer blobs were never transferred. Zero-byte failed-transfer placeholders were removed. Temporary inspection and tool directories were removed after confirming they contained no required review evidence.

No virtual environment, Homebrew package, `/opt/podman` installation, path file, helper, Go installation, age installation, PostgreSQL tool, Podman machine, container image, volume, network, credential, key, service, listener, fixture, candidate tree, build output, prototype, or test output exists from this checkpoint.

Host command lookup after acquisition still found no `go`, `podman`, `docker`, `psql`, `postgres`, or `age` executable.

## Repository boundary

The Gate-2 documentation commit preceded acquisition. The acquisition root and every binary/cache artifact remain outside the repository and are not staged or committed. The only proposed repository changes after Checkpoint A are this normalized documentation package.

## Cleanup posture

The cache remains available for user review because deleting it before review would remove raw supporting evidence. It is temporary, not backed up, and may disappear under normal operating-system cleanup. If removal is later authorized, cleanup must:

1. resolve the exact physical path;
2. require the owner-only directory and expected sentinel;
3. compare its inventory with the retained-cache record;
4. remove only that exact root;
5. confirm no process has an open working directory or file beneath it;
6. record the post-removal absence.

No global cache purge, package uninstall, broad wildcard, recursive home/repository deletion, or unrelated process termination is permitted.
