# R1 PostgreSQL OCI Image-Content Route Dossier

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Route outcome:** R2-ready for an exact digest-only, anonymous-pull route.

## Exact publisher route

| Field | Evidence |
|---|---|
| Product | Docker Official Image packaging for PostgreSQL 18.6 |
| Tag used only for initial resolution | `postgres:18.6-bookworm` |
| Official-images source of truth | [`library/postgres`](https://github.com/docker-library/official-images/blob/master/library/postgres) |
| Packaging source | [`docker-library/postgres`](https://github.com/docker-library/postgres), commit `e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc`, directory `18/bookworm` |
| Multi-architecture index | `sha256:1c59e2c3c818eaa0f0628f695b36e7c9e362d6b219b36a54a32df645cbd7e1af` |
| Target platform | `linux/arm64/v8` |
| Platform manifest | `sha256:4d155aa3f2c2cc1838bb70e81396f76373ec7275ec9ce9cf32873cd677c9a992` |
| Base | `debian:bookworm-slim@sha256:6bd27d44e6c32a66bbd72d7cb2b76a8ae3497ec2e5274a81abd1b37f6013fa1f` |
| Image metadata | Docker Hub [arm64 manifest page](https://hub.docker.com/layers/arm64v8/postgres/18-bookworm/images/sha256-4d155aa3f2c2cc1838bb70e81396f76373ec7275ec9ce9cf32873cd677c9a992) |

The official-images record names the 18.6-bookworm tag, architectures, source commit, and `18/bookworm` directory. The exact index and arm64 manifest were independently verified at Checkpoint A and agree with Docker Hub metadata.

## Expected API and redirect route

Docker's official [Registry API](https://docs.docker.com/reference/api/registry/latest/) defines:

1. an anonymous repository-scoped bearer token from `auth.docker.io`;
2. manifest and blob requests to `registry-1.docker.io`;
3. manifest selection by platform digest;
4. blob requests by immutable digest.

The registry specification allows a blob GET to return HTTP 307 to another download service. Docker's official [firewall allowlist](https://docs.docker.com/desktop/setup/allow-list/) explicitly names `production.cloudfront.docker.com` for Docker pull/push traffic. This confirms the host observed at Checkpoint A and demonstrates that `production.cloudflare.docker.com` in the accepted proposal was erroneous.

Expected future route:

- `https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/postgres:pull`;
- `https://registry-1.docker.io/v2/library/postgres/manifests/<accepted-digest>`;
- `https://registry-1.docker.io/v2/library/postgres/blobs/<accepted-digest>`;
- HTTP 307 only to `https://production.cloudfront.docker.com/...` for exact accepted blobs.

The bearer token is anonymous, pull-only, repository-scoped, memory-only, and not a Docker Hub login. No refresh token, credential helper, Docker config, account, or keychain entry is needed. A request for login, payment, broader scope, refresh token, or push capability is a stop.

## Exact content set

Only these fourteen blobs are proposed:

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

No mutable tag request is needed in renewed acquisition because the accepted index and platform digests are already frozen. No referrer, attestation, signature object, helper image, vulnerability database, or alternate architecture is in scope.

## Integrity and signature method

The official [Distribution API specification](https://distribution.github.io/distribution/spec/api/) requires clients fetching by digest to verify local bytes against the requested digest; it warns not to trust a response digest over the local calculation.

Proposed controls:

1. request every blob by the digest in the accepted arm64 manifest;
2. record initial URL, 307 destination host/path without signed query material, byte length, response headers, and completion status;
3. independently compute SHA-256 before accepting the blob;
4. reject mismatched length or digest and delete partial bytes;
5. preserve the index → platform manifest → config/layer descriptor chain;
6. perform decompression, path-safety inspection, package inventory, SBOM inputs, and license extraction offline only.

No detached image signature or accepted Sigstore/Notation proof has been established for this image. Docker documents retirement of Docker Content Trust for Official Images. R1 therefore records `content-addressed integrity and Official Images provenance; no detached signature established`. It does not mislabel digest verification as publisher signature verification.

## License sources

- PostgreSQL itself uses the [PostgreSQL License](https://www.postgresql.org/about/licence/).
- The Docker Official Image packaging repository uses its [MIT license](https://github.com/docker-library/postgres/blob/master/LICENSE).
- The [official image documentation](https://github.com/docker-library/docs/blob/master/postgres/README.md) warns that base-distribution and bundled components carry additional licenses.
- Complete Debian package names, versions, notices, and licenses remain unavailable until the fourteen blobs are acquired and inventoried offline.

No image-content license pass may occur from the PostgreSQL and packaging licenses alone.

## Installer and runtime side effects

Content acquisition is GET-only and does not import or execute the image. No local container store, Podman machine, volume, network, database, listener, or package installation is needed.

If later imported and run, the verified image metadata/source declares:

- `PGDATA=/var/lib/postgresql/18/docker`;
- volume `/var/lib/postgresql`;
- entrypoint `docker-entrypoint.sh`;
- default command `postgres`;
- exposed container port 5432;
- `SIGINT` stop signal;
- initialization behavior that writes database state;
- a generated sample configuration with `listen_addresses = '*'` inside the container.

Those runtime behaviors are security-relevant but are outside R1/R2 acquisition and do not authorize a service or listener.

## Proposed hosts

Future digest-only acquisition would permit exactly:

- `auth.docker.io`, anonymous pull token only;
- `registry-1.docker.io`, exact `library/postgres` manifest/blob paths;
- `production.cloudfront.docker.com`, exact redirected paths for the fourteen accepted digests.

Proposed removal from the future acquisition manifest:

- `production.cloudflare.docker.com`, because it is neither the observed redirect nor the host named by Docker's official allowlist.

`hub.docker.com` is evidence/UI only and is not needed for the blob route. Docker telemetry, Scout, analytics, update, support, login, and AI domains remain excluded.

## Rollback

Acquisition rollback is exact and local:

1. hold the anonymous token only in memory and allow it to expire;
2. write blobs only beneath a fresh sentinel-bearing cache root;
3. inventory temporary and completed files;
4. remove a partial file immediately on mismatch or interruption;
5. after review or later cleanup approval, validate sentinel/owner/realpath and remove only the fourteen cached blobs plus route metadata;
6. confirm no image store, container runtime state, registry credential/config, process, service, listener, volume, or database exists.

Anonymous Docker Hub pulls may be rate-limited. A 429 response stops the route; it does not authorize login, an account, payment, retry loops, or a mirror.

## Proposed route change

Prepare an R2 manifest diff that corrects the CDN hostname, freezes the exact index/platform/config/layer digests above, removes the mutable tag from acquisition, and restricts authorization to anonymous pull scope. Do not execute that diff or request any blob until R2 is explicitly accepted.
