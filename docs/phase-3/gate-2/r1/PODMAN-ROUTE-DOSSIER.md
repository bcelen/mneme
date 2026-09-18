# R1 Podman Route Dossier

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Route outcome:** Blocked. Do not renew the v6.1.2 package route.

## Exact publisher route

| Field | Evidence |
|---|---|
| Product and version | Podman 6.1.2 for macOS arm64 |
| Publisher project | Podman project; the canonical `containers/podman` GitHub URLs currently redirect to `podman-container-tools/podman` |
| Release record | [`v6.1.2` release](https://github.com/containers/podman/releases/tag/v6.1.2), tag commit `04f3aa4` |
| Installer | `podman-installer-macos-arm64.pkg` |
| Exact request | `https://github.com/podman-container-tools/podman/releases/download/v6.1.2/podman-installer-macos-arm64.pkg` |
| Published checksum record | `https://github.com/podman-container-tools/podman/releases/download/v6.1.2/shasums` |
| Package bytes | 76,397,383 |
| Package SHA-256 | `88def43af7fbe7baf40fc2f12d69267f6d845768020709900fb1b8c3bfe015b3` |

The official [installation guide](https://podman.io/docs/installation) recommends the GitHub release installer for macOS. The project [release process](https://github.com/containers/podman/blob/main/RELEASE_PROCESS.md) lists the macOS arm64 package and `shasums` among required release assets. The project [download policy](https://github.com/containers/podman/blob/main/DOWNLOADS.md) distinguishes official release artifacts, described as signed, from unsigned, mutable CI artifacts.

## Expected redirects and hosts

The accepted Checkpoint-A record observed:

1. the exact GitHub package/checksum URLs above;
2. HTTP 302 redirects to `release-assets.githubusercontent.com`;
3. no additional artifact host.

The current acquisition-host set is therefore:

- `github.com`, release metadata and initial asset request;
- `release-assets.githubusercontent.com`, exact release asset bytes.

`objects.githubusercontent.com` remains unnecessary for the observed asset route. `api.cirrus-ci.com` is explicitly excluded because the project labels CI artifacts unsigned and mutable.

No host addition is proposed for Podman in R2.

## Integrity and signature evidence

| Control | Result |
|---|---|
| Release tag | GitHub reports the tag/commit signature Verified, with GPG key `5A0F5FA1CEF5C874` now expired |
| Published checksum | Exact package SHA-256 matched the publisher's `shasums` |
| macOS package signature | Local `pkgutil --check-signature` returned `Status: invalid signature` |
| Apple team identity | Unavailable because the package signature did not validate |
| Asset-to-tag binding | A signed tag and matching checksum do not establish a valid Apple signature on the package asset |

The project-level claim that official release artifacts are signed conflicts with the host verification result for this exact package. R1 cannot resolve that conflict through documentation. Reacquiring identical bytes would not change the signature outcome.

## License sources

- The versioned project source carries the [Podman top-level license](https://github.com/containers/podman/blob/v6.1.2/LICENSE).
- The accepted package evidence retains the release license material and records an Apache-2.0/GPL and bundled-component posture.
- The package contains a broad executable payload; a complete bundled-component inventory and notices report is still required before installation or redistribution.

The top-level project license is not a substitute for a reconciled package-payload license report.

## Installer and runtime side effects

Static inspection of the exact package, without execution, found:

- package identifier `com.redhat.podman`, version 6.1.2;
- root authorization and install location `/opt`;
- 236 payload files and approximately 159,091 KB installed size;
- preinstall recursive removal of `/opt/podman`;
- creation of `/etc/paths.d` and `/usr/local/etc/man.d` if absent;
- postinstall writes to `/etc/paths.d/podman-pkg` and `/usr/local/etc/man.d/podman.man.conf`;
- postinstall execution of `/opt/podman/bin/podman-mac-helper install`.

The official macOS architecture also requires a Podman-managed Linux virtual machine. The [installation documentation](https://podman.io/docs/installation) states that the macOS CLI communicates with a service in that VM. The [machine-start documentation](https://docs.podman.io/en/latest/markdown/podman-machine-start.1.html) shows optional helper installation for Docker API socket forwarding.

These later runtime effects would include VM disk/state, SSH material, sockets, container storage, configuration, and possibly a helper service. None is authorized in R1.

## Rollback evidence

Rollback is not sufficiently specified for this package route:

- the installer has no reviewed, bounded uninstall script in the accepted evidence;
- upstream issue [containers/podman#18034](https://github.com/containers/podman/issues/18034) records the lack of complete macOS uninstall documentation;
- an exact rollback would need to distinguish pre-existing `/opt/podman`, path/manpath files, helper state, VM state, user container configuration, sockets, SSH material, and package receipts;
- broad recursive removal, global prune, `podman system reset`, and process-name-wide termination are not acceptable rollback mechanisms.

The only safe rollback for Checkpoint A was non-installation plus removal of the rejected package from the disposable cache; that rollback is complete.

## Proposed route decision

Adopt **P4 — defer container-backed evidence** for the next R2 draft. Preserve all Podman-dependent Gate-2 controls as Blocked or Unproved. Do not list the v6.1.2 package as an acquirable artifact.

P1 may be reconsidered only if the publisher provides either:

1. replacement bytes with a valid Apple package signature and documented team identity; or
2. an authoritative explanation plus a separately reviewable signature and rollback mechanism that satisfies the accepted contract.

P2 or P3 would be new routes with new dependencies and architecture/security evidence. They are outside this dossier and require a new proposal.
