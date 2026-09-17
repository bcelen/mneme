# Checkpoint-A Integrity and Signature Report

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18

## Verification method

Every downloaded file was hashed independently with the host SHA-256 implementation. Ecosystem metadata was compared only after the independent hash was recorded. Archive structure was inspected without installing or executing candidate code. A matching hash proves byte identity with the accepted or published value; it does not replace signature, provenance, side-effect, dependency, or license review.

## Python result

All three wheel hashes matched both the accepted manifest and PyPI release metadata. Wheel metadata confirmed universal `py3-none-any` artifacts. Archive scans found no native executable library, unsafe path, or symlink. PyPI reported no uploaded signature for the three files. The accepted exact hashes and two-source comparison are therefore the available integrity controls.

**Finding:** Verified for local cache retention. Installation remains outside Checkpoint A.

## Go result

The Go toolchain archive was never downloaded because its first redirect left the accepted host set. Without the exact toolchain, `go mod verify`, `go list -m -json all`, and checksum-database signature verification could not be run.

The six reviewed module ZIPs matched the content hashes returned by `sum.golang.org`, and their archive paths were structurally safe. Those observations are not promoted to full verification because:

1. the checksum-database records could not be verified with the Go toolchain;
2. the full minimal-version-selected graph could not be generated authoritatively;
3. eight graph members visible in published module files were not declared as allowed acquisition components;
4. executable ZIPs were therefore removed.

**Finding:** Partial provenance evidence only; no build-eligible Go cache exists.

## Podman result

The package SHA-256 matched the publisher's `shasums` file. macOS package signature inspection returned exactly `Status: invalid signature`. This does not satisfy the accepted requirement for an official signed package with captured Apple identity.

Static package expansion showed identifier `com.redhat.podman`, version `6.1.2`, install location `/opt`, root authorization, 236 payload files, and an estimated 159,091 KB installed size. The scripts would:

- recursively remove `/opt/podman` before installation;
- create `/etc/paths.d` and `/usr/local/etc/man.d` as root when absent;
- write `/etc/paths.d/podman-pkg`;
- run `/opt/podman/bin/podman-mac-helper install`;
- write `/usr/local/etc/man.d/podman.man.conf`.

These are installer side effects and include a destructive recursive removal not separately approved by Checkpoint A. No script or payload executable was run. The package was removed after evidence capture.

**Finding:** Rejected. Matching checksum is insufficient in the presence of an invalid signature and unapproved privileged/destructive effects.

## age result

The archive independently matched the exact SHA-256 accepted in the Gate-1 manifest. Its separate proof file was retained and hashed. The required `sigsum-verify` verifier was not installed or authorized as an additional dependency, so the proof could not be validated.

Static macOS inspection of the temporarily extracted `age` binary reported an ad-hoc linker signature, no TeamIdentifier, no CMS signing authority, no sealed resources, and no internal signing requirement. An ad-hoc signature supplies no publisher identity. Neither `age` nor `age-keygen` was executed, and no key was created.

**Finding:** Rejected as an executable input pending an approved and independently verifiable proof route. Archive and binary removed; proof and normalized inspection evidence retained.

## PostgreSQL OCI result

The tag response was an OCI image index. Its registry `Docker-Content-Digest` and independent SHA-256 agreed on:

`sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af`

The index selected the `linux/arm64/v8` manifest:

`sha256:4d155aa3f2c2cc1838bb70e81396f76373ec7275ec9ce9cf32873cd677c9a992`

The fetched platform manifest matched its index descriptor, response digest header, and independent hash. It identifies config digest `sha256:b85269e8c6aa961524542eb4dcca44c4aa1deba2cf507e9e28d5ba8f971aeab9` and thirteen immutable layer descriptors.

The first blob request returned a redirect to a host not in the accepted allowlist. No config or layer bytes were followed, pulled, decompressed, or retained. Thus the index and platform manifest are verified metadata, but image content, package inventory, SBOM inputs, and license inventory are absent.

**Finding:** Immutable metadata established; OCI image acquisition incomplete and unusable.

## Signature and proof summary

| Component | Hash | Signature/proof | Outcome |
|---|---|---|---|
| Python wheels | Exact accepted and PyPI hashes match | PyPI reports no file signatures | Verified under accepted hash policy |
| Go toolchain | Not acquired | Not evaluated | Rejected at redirect boundary |
| Go modules | Proxy ZIP hashes and sum records retained | Sum-database verification not run | Partial evidence; executable ZIPs removed |
| Podman package | Publisher hash matches | macOS package signature invalid | Rejected |
| age archive | Exact accepted hash matches | Sigsum proof unverified; binary ad-hoc signed | Rejected |
| PostgreSQL OCI | Index and arm64 manifest digests independently match | Content-addressed metadata only; blobs absent | Metadata verified; image incomplete |

No integrity failure was bypassed and no unsigned or incompletely verified executable was installed.
