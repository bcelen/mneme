# Checkpoint-A Acquisition Register

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Rule:** A retrieved file is not an approved executable input unless source, exact version, byte length, integrity, signature/proof posture, dependency graph, and license evidence satisfy the accepted manifest.

## Python wheels

| Component | Exact URL | Filename | Bytes | SHA-256 | Result |
|---|---|---|---:|---|---|
| Django 6.1.1 | `https://files.pythonhosted.org/packages/8d/ca/c1040a4fd15754ede7df15fd72fc2e123045b473b253ab5f5284e11c651e/django-6.1.1-py3-none-any.whl` | `django-6.1.1-py3-none-any.whl` | 8,419,512 | `585fb82bf15053c42cf52e67c2f1b54a032dca384759315fd6678ab1870d1d72` | Verified and retained |
| asgiref 3.12.1 | `https://files.pythonhosted.org/packages/c0/1b/54f4ad77cd8a584fa70746c47df988e002cf1ee1eba43364d46f87803647/asgiref-3.12.1-py3-none-any.whl` | `asgiref-3.12.1-py3-none-any.whl` | 25,478 | `fe386d1c2bff7259ea95929266d12a8cf9a8b5a1c2598402967d8792e7a7c094` | Verified and retained |
| sqlparse 0.6.0 | `https://files.pythonhosted.org/packages/d9/50/f00935da0ec7cbf325f8dc4f772ae46fbc7b672dd62876e73f0a94adda57/sqlparse-0.6.0-py3-none-any.whl` | `sqlparse-0.6.0-py3-none-any.whl` | 50,070 | `b861c0288ce2fa56209a9a6412d2e066ac664b3873b89c26c9d8415e8e32996f` | Verified and retained |

Metadata was also acquired from the exact `https://pypi.org/pypi/<project>/<version>/json` endpoints. For all three artifacts, the published filename, size, and SHA-256 matched the independently computed values. PyPI reported `has_sig=false`; integrity therefore rests on the accepted exact hashes plus TLS source provenance, not a package signature.

The retained lock is exactly:

```text
Django==6.1.1 --hash=sha256:585fb82bf15053c42cf52e67c2f1b54a032dca384759315fd6678ab1870d1d72
asgiref==3.12.1 --hash=sha256:fe386d1c2bff7259ea95929266d12a8cf9a8b5a1c2598402967d8792e7a7c094
sqlparse==0.6.0 --hash=sha256:b861c0288ce2fa56209a9a6412d2e066ac664b3873b89c26c9d8415e8e32996f
```

No wheel was installed or imported.

## Go toolchain

| Requested artifact | Accepted expected SHA-256 | Result |
|---|---|---|
| `https://go.dev/dl/go1.27.1.darwin-arm64.tar.gz` | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` | HTTP 302 to `https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz`; redirect rejected because the host was not in the accepted allowlist; no archive bytes downloaded |

Go remains absent. No alternate mirror, package manager, or version was used.

## Go modules

The accepted module endpoints at `proxy.golang.org` supplied `.info`, `.mod`, and `.zip` files; `sum.golang.org` supplied checksum-database records. The executable ZIPs were inspected for unsafe paths and symlinks, hashed, and then removed because the Go toolchain verifier and complete reviewed graph were unavailable.

| Module | Version | ZIP bytes | ZIP SHA-256 | Sum-database content hash | Disposition |
|---|---:|---:|---|---|---|
| `github.com/jackc/pgx/v5` | v5.11.0 | 762,523 | `ada62e95244336484f86c274e04a6845f0c494c93b69d24f2ac4181b7c58b11d` | `h1:IzBBtyK9AHqf98cctWFifYSci2hgQR/cd56wB4p+ogg=` | ZIP removed; metadata retained |
| `github.com/jackc/pgpassfile` | v1.0.0 | 4,375 | `1cc79fb0b80f54b568afd3f4648dd1c349f746ad7c379df8d7f9e0eb1cac938b` | `h1:/6Hmqy13Ss2zCq62VdNG8tM1wchn8zjSGOBJ6icpsIM=` | ZIP removed; metadata retained |
| `github.com/jackc/pgservicefile` | v0.0.0-20240606120523-5a60cdf6a761 | 4,880 | `c9e31c91aebf96eb246bd410d1849cc7666d955a1e20ca2eba1c30b4eb89335f` | `h1:iCEnooe7UlwOQYpKFhBabPMi4aNAfoODPEFNiAnClxo=` | ZIP removed; metadata retained |
| `github.com/jackc/puddle/v2` | v2.2.2 | 24,095 | `f1f0789098a0bcb5ff3c7024f9ee387a6748446e1bc6713b13a63d763a9fb11e` | `h1:PR8nw+E/1w0GLuRFSmiioY6UooMp6KJv0/61nB7icHo=` | ZIP removed; metadata retained |
| `golang.org/x/sync` | v0.17.0 | 25,707 | `c5dcfd32e223edc7a003a51a166a81759a4beccb9a91eb85385b4d67a1c820c6` | `h1:l60nONMj9l5drqw6jlhIELNv9I0A4OFgRsG9k2oT9Ug=` | ZIP removed; metadata retained |
| `golang.org/x/text` | v0.29.0 | 9,234,225 | `fb47744565fd36da42ab2ebd3ee4db0038dfed4f703c926a9e7327debab8af77` | `h1:1neNs90w9YzJ9BocxfsQNHKuAT4pkghyXc4nhZ6sJvk=` | ZIP removed; metadata retained |

The exact module proxy URL form was `https://proxy.golang.org/<escaped-module>/@v/<version>.{info,mod,zip}`. The checksum records came from the exact module/version lookup endpoints at `https://sum.golang.org/lookup/`.

## Podman 6.1.2

| Artifact | Requested URL | Bytes | SHA-256 | Result |
|---|---|---:|---|---|
| macOS arm64 package | `https://github.com/podman-container-tools/podman/releases/download/v6.1.2/podman-installer-macos-arm64.pkg` | 76,397,383 | `88def43af7fbe7baf40fc2f12d69267f6d845768020709900fb1b8c3bfe015b3` | Published checksum matched; signature/side-effect checks failed; package removed |
| published checksums | `https://github.com/podman-container-tools/podman/releases/download/v6.1.2/shasums` | 830 | `8853016bc14230d401b59ce1364159c1dccadb2557f51c4d85a1b7a90c74bc21` | Retained as evidence |

Both requests redirected to the accepted `release-assets.githubusercontent.com` host. The package was expanded for metadata and script inspection without installation or execution.

## age 1.3.2

| Artifact | Requested URL | Bytes | SHA-256 | Result |
|---|---|---:|---|---|
| macOS arm64 archive | `https://github.com/FiloSottile/age/releases/download/v1.3.2/age-v1.3.2-darwin-arm64.tar.gz` | 18,106,798 | `e2020b073c44f692685a24d6abc378817eb81ffaaf49fd0531ef8565f767f2f5` | Accepted hash matched; proof could not be verified; archive removed |
| Sigsum proof | `https://github.com/FiloSottile/age/releases/download/v1.3.2/age-v1.3.2-darwin-arm64.tar.gz.proof` | 1,921 | `26e3fcc371f19e35c7d37500baf8e82c4386538dc6f47e66f4e0fefec50531e4` | Retained as evidence; unverified locally |

Both requests redirected to the accepted `release-assets.githubusercontent.com` host. The archive had nine safe entries and no unsafe path, device, or FIFO. The executable was extracted only into the disposable inspection directory for static code-signature inspection, was never run, and was then removed with the archive.

## PostgreSQL 18.6 OCI metadata and content

| Object | Registry request | Bytes | Digest / independent SHA-256 | Result |
|---|---|---:|---|---|
| Multi-architecture index for `18.6-bookworm` | `https://registry-1.docker.io/v2/library/postgres/manifests/18.6-bookworm` | 6,491 | `sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af` | Header and independent hash matched; retained |
| `linux/arm64/v8` manifest | `https://registry-1.docker.io/v2/library/postgres/manifests/sha256:4d155aa3f2c2cc1838bb70e81396f76373ec7275ec9ce9cf32873cd677c9a992` | 3,454 | `sha256:4d155aa3f2c2cc1838bb70e81396f76373ec7275ec9ce9cf32873cd677c9a992` | Header, index descriptor, and independent hash matched; retained |
| arm64 config blob | `https://registry-1.docker.io/v2/library/postgres/blobs/sha256:b85269e8c6aa961524542eb4dcca44c4aa1deba2cf507e9e28d5ba8f971aeab9` | Not transferred | Descriptor digest `sha256:b85269e8c6aa961524542eb4dcca44c4aa1deba2cf507e9e28d5ba8f971aeab9` | HTTP 307 to unallowlisted `production.cloudfront.docker.com`; rejected |
| Thirteen arm64 layers | Registry blob endpoints from the verified manifest | Not transferred | Thirteen immutable descriptor digests retained in the manifest | First blob redirect exposed the same unallowlisted host; all content retrieval stopped |

The verified OCI annotations identify version `18.6-bookworm`, source revision `e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc`, source tree `https://github.com/docker-library/postgres.git#e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc:18/bookworm`, and base image `debian:bookworm-slim` at `sha256:6bd27d44e6c32a66bbd72d7cb2b76a8ae3497ec2e5274a81abd1b37f6013fa1f`.

The arm64 manifest records these blobs; none was transferred:

| Kind | Bytes | Digest |
|---|---:|---|
| Config | 10,055 | `sha256:b85269e8c6aa961524542eb4dcca44c4aa1deba2cf507e9e28d5ba8f971aeab9` |
| Layer 01 | 28,117,289 | `sha256:75782e20ea1f4a9d9259bc20a5ecbbea8d5943bf5370bf0f5727900728f1cc9a` |
| Layer 02 | 1,170 | `sha256:545481733576eae22997a02807d7947613125ef556fc5267d8b71b8633888312` |
| Layer 03 | 4,519,566 | `sha256:60ec89b686ebd79b724a8429c13f58185a441a1c483bf8819931d566db040829` |
| Layer 04 | 1,203,841 | `sha256:f54f79a42a2dfe06e33db86854c4f0484d3fd98636de77570703312d26f0df24` |
| Layer 05 | 8,066,459 | `sha256:63ba4d1b9b1aa469776fb0250fffeace022a871a88d423518cc33fa388ffc663` |
| Layer 06 | 1,108,983 | `sha256:22a8987b6f5cb2778463a82a1f33a53b667e76f57aed25ffcba1f70b16c9ab59` |
| Layer 07 | 116 | `sha256:7ef8a510d41418d6cf3f98cf24533b81adcba4bd5689ae1e60c89ad5c4336e3f` |
| Layer 08 | 3,140 | `sha256:7105667d1505a2ae58b986439108a7fd8a3a8cab26eb47f1009ae60c3986ff2e` |
| Layer 09 | 112,194,873 | `sha256:840f3b8b2441f35405e77774444fdc3233c4c83ea240af495f58ad95390c67be` |
| Layer 10 | 19,319 | `sha256:3d2cfabac35eb0d31771041e04952ee51afdfb69a6d41a2dbae864f63bd7a070` |
| Layer 11 | 128 | `sha256:ca026fbec3730f56a63cea66221e2aadbf90e89f796f967dee89cfddeaf09819` |
| Layer 12 | 6,107 | `sha256:db077a768c3b2e74f651728b16ce42dd1adba16a42ec7b3402c1209f8204cfef` |
| Layer 13 | 186 | `sha256:53367cc5fc824588caec6e186b0a5641c4c80e25a36002faed84d4eb6e9dfb2a` |

Image content, package inventory, and image-license evidence were not acquired.
