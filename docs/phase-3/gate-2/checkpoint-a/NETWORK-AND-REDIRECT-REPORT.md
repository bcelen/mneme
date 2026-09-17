# Checkpoint-A Network and Redirect Report

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18

## Network rule

Checkpoint A allowed artifact-only traffic to the hosts accepted in `docs/phase-3/DEPENDENCY-MANIFESTS.md`. Redirects were normalized without query strings before durable recording. A redirect to any other host was rejected before artifact transfer. No source record, fixture, user identifier, project evidence, credential, or live-archive path was sent.

## Accepted hosts contacted

- `pypi.org` and `files.pythonhosted.org` for exact Python release metadata and wheels;
- `go.dev` for the exact Go toolchain request;
- `proxy.golang.org` and `sum.golang.org` for six reviewed module/version records;
- `github.com` and `release-assets.githubusercontent.com` for exact Podman and age release assets;
- `registry-1.docker.io` and `auth.docker.io` for anonymous PostgreSQL Official Image metadata and blob authorization.

No account sign-in, paid service, source provider, model provider, telemetry endpoint, analytics endpoint, or update service was used.

## Redirect register

| Item | Requested URL | Response | Normalized destination | Decision |
|---|---|---:|---|---|
| Go archive | `https://go.dev/dl/go1.27.1.darwin-arm64.tar.gz` | 302 | `https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz` | Rejected: host not allowlisted |
| Podman package | `https://github.com/podman-container-tools/podman/releases/download/v6.1.2/podman-installer-macos-arm64.pkg` | 302 | `https://release-assets.githubusercontent.com/github-production-release-asset/109145553/23e216df-b208-43e5-87aa-a329032db4f2` | Accepted host |
| Podman checksums | `https://github.com/podman-container-tools/podman/releases/download/v6.1.2/shasums` | 302 | `https://release-assets.githubusercontent.com/github-production-release-asset/109145553/c50044d5-c107-4925-a12e-57478b9cb1f1` | Accepted host |
| age archive | `https://github.com/FiloSottile/age/releases/download/v1.3.2/age-v1.3.2-darwin-arm64.tar.gz` | 302 | `https://release-assets.githubusercontent.com/github-production-release-asset/187403699/e19de7f8-c444-4066-a355-6466f4aa2e21` | Accepted host |
| age proof | `https://github.com/FiloSottile/age/releases/download/v1.3.2/age-v1.3.2-darwin-arm64.tar.gz.proof` | 302 | `https://release-assets.githubusercontent.com/github-production-release-asset/187403699/4fd489d8-1570-4d83-a53b-e8b593269f55` | Accepted host |
| PostgreSQL config blob | `https://registry-1.docker.io/v2/library/postgres/blobs/sha256:b85269e8c6aa961524542eb4dcca44c4aa1deba2cf507e9e28d5ba8f971aeab9` | 307 | `https://production.cloudfront.docker.com/registry-v2/docker/registry/v2/blobs/sha256/b8/b85269e8c6aa961524542eb4dcca44c4aa1deba2cf507e9e28d5ba8f971aeab9/data` | Rejected: host not allowlisted |

The accepted manifest listed `production.cloudflare.docker.com`; the observed Docker registry destination was `production.cloudfront.docker.com`. Similar names were not treated as equivalent.

## Authentication and sensitive URL handling

Docker registry metadata required an anonymous, short-lived bearer token from the accepted `auth.docker.io` endpoint. It was held only in process memory for the metadata request. No username, password, account, refresh token, credential helper, Docker configuration, or keychain entry was created.

Raw response headers containing bearer challenges, signed release-asset query parameters, or CDN token material were not copied into the repository. Durable redirect evidence strips query strings. A scan of the retained evidence found no Authorization header, bearer/JWT value, or signed-query secret.

## Network-window closure

All acquisition clients exited after the final rejected OCI redirect. There is no acquisition process, download manager, registry login, credential helper, listener, service, or persistent network session. The acquisition used ordinary short-lived host HTTPS clients; no dedicated network namespace existed, so an operating-system-wide network-disconnect claim is not made. The usable acquisition path is closed operationally by the absence of active clients and by the explicit stop before Checkpoint B.

No offline build or cache-completeness test was run because builds and tests were prohibited and the Go and OCI caches are incomplete.

## Network finding

The unknown-host stop control worked twice. Checkpoint A remains incomplete because the accepted allowlist does not describe the official redirect paths currently observed for Go and Docker Registry content. No allowlist was edited during acquisition.
