# R1 Proposed Route Changes

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Rule:** This document proposes future R2 edits. It does not apply them.

## Proposed dependency-manifest changes

| Area | Current accepted entry | Proposed R2 change | Reason | R1 status |
|---|---|---|---|---|
| Podman | v6.1.2 official macOS arm64 package | Mark package route `BLOCKED-SIGNATURE-AND-ROLLBACK`; remove it from acquirable artifacts; defer container-backed evidence | Invalid package signature, privileged/destructive script effects, and incomplete official rollback documentation | Blocked |
| Go toolchain | Go 1.27.1 archive via `go.dev` | Preserve exact archive/hash; name `dl.google.com` as publisher CDN; require archive-only extraction to disposable root | Go primary source establishes the CDN and exact hash | R2-ready |
| Go graph | pgx plus five named modules; unexpected entries block | Add eight discovered modules as metadata-only graph candidates; prohibit ZIP acquisition until selected graph and licenses are reviewed | Makes the known graph expansion explicit without authorizing payloads | Conditionally R2-ready |
| age | age 1.3.2 archive and proof; verifier absent | Keep artifact reacquisition disabled; add a blocker requiring an exact `sigsum-verify@v0.13.1` graph and v1.3.2 policy-compatibility evidence | The proof cannot be verified safely by an unreviewed verifier | Blocked |
| PostgreSQL | `postgres:18.6-bookworm`, index/platform digests; content host typo | Replace tag-based acquisition with fourteen exact blob digests; correct the CDN hostname; retain anonymous pull only | Docker primary evidence confirms content route and host | R2-ready |

## Proposed acquisition-host changes

These are proposed lines for a later reviewed diff, not current allowlist edits:

| Host | Proposed action | Exact purpose and restriction |
|---|---|---|
| `dl.google.com` | Add | One GET for `/go/go1.27.1.darwin-arm64.tar.gz`; no other path, version, package, or redirect |
| `production.cloudfront.docker.com` | Add | Follow 307 redirects only for the accepted PostgreSQL config and thirteen layer digests; signed query material remains ephemeral |
| `production.cloudflare.docker.com` | Remove | Erroneous hostname; not observed and not named in Docker's official allowlist |
| `go.dev` | Retain | Go release metadata; artifact request may redirect to the exact CDN |
| `proxy.golang.org` | Retain without expansion | Reviewed module metadata/checksum route; no new ZIP payload until graph approval |
| `sum.golang.org` | Retain without expansion | Checksum-database authentication for an approved module graph |
| `github.com` | Retain without expansion | Exact publisher release metadata and existing release asset paths only |
| `release-assets.githubusercontent.com` | Retain without expansion | Expected GitHub release asset CDN for exact reviewed assets only |
| `auth.docker.io` | Retain | Anonymous, pull-only, repository-scoped token for `library/postgres` |
| `registry-1.docker.io` | Retain | Exact accepted manifest and blob paths only |

No wildcard subdomain, alternate CDN, mirror, direct VCS host, convenience download host, package manager, login host, telemetry host, or update host is proposed.

## Exact future R2 boundaries

An R2 proposal may contain documentation changes only and must include:

1. a line-by-line allowlist diff with the two proposed hostname corrections/additions;
2. an exact artifact/digest table and expected HTTP status/redirect path per request;
3. independent integrity and signature/proof status for each component;
4. the Podman deferment and resulting Gate-2 controls that remain Blocked;
5. the eight Go modules marked metadata-only, with no ZIP authorization;
6. the age verifier blocker, with no verifier/module acquisition authorization;
7. the fourteen PostgreSQL blobs and anonymous-token handling rules;
8. exact cache paths, permissions, sentinel, inventories, and rollback steps;
9. specialist signoffs and unresolved disagreements;
10. a new user approval gate before any network request.

## R2 blockers that R1 does not close

- Podman has no acceptable signed package and bounded rollback route.
- The authoritative Go graph has not been computed with the exact toolchain.
- The `sigsum-verify` module graph and v1.3.2 proof compatibility are not established.
- PostgreSQL's full package/license inventory cannot exist before content acquisition.
- Offline completeness cannot be demonstrated until every retained route is locally complete.

R2 may propose controlled acquisition for the Go toolchain and PostgreSQL content while explicitly deferring Podman and age. Such an approval would close neither Checkpoint A nor Gate 2 by itself.

## Specialist review required before R2

- **Maintenance/supply chain:** Go CDN provenance, digest-only OCI route, graph-before-payload rule, and Podman/age blocker calibration.
- **Security/privacy:** anonymous token scope, redirect confinement, installer privilege/rollback, no direct VCS or credential fallback, and cache boundaries.
- **Licensing/cost:** Go/module license sources, deferred Podman bundled report, age/Sigsum licenses, OCI license-inventory limitation, and Docker rate-limit/account stop.
- **Quality/review:** exact host/path/digest reconciliation and negative stop cases.
- **Orchestrator:** staged authority, no route leakage into R3/R4/Checkpoint B, and no stack-selection inference.

## Explicit non-authorization

Acceptance of R1 would not authorize:

- applying these manifest or allowlist changes;
- contacting `dl.google.com` or `production.cloudfront.docker.com`;
- reacquiring Podman or age;
- acquiring Go, any Go module, `sigsum-verify`, or any OCI blob;
- installing, extracting, importing, executing, compiling, building, or testing anything;
- creating a fixture, credential, key, service, listener, container, image store, database, prototype, or generated artifact;
- starting R2, R3, R4, Checkpoint B, stack selection, commit, or push.

## Review request

Review is requested on four proposed dispositions:

1. defer Podman and preserve its dependent gates as Unproved;
2. permit a future R2 draft to add the exact Go CDN route while keeping module ZIPs blocked;
3. keep age blocked until the verifier trust chain is complete;
4. permit a future R2 draft to correct the Docker CDN hostname and name the fourteen exact blobs.
