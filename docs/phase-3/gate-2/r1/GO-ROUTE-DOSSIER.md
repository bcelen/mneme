# R1 Go Toolchain and Dependency-Graph Route Dossier

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Route outcome:** Toolchain route is R2-ready; module payload acquisition remains blocked pending graph approval.

## Exact toolchain route

| Field | Evidence |
|---|---|
| Publisher source | [Go downloads](https://go.dev/dl/) |
| Product/version | Go 1.27.1, macOS arm64 archive |
| Artifact | `go1.27.1.darwin-arm64.tar.gz` |
| Publisher URL | `https://go.dev/dl/go1.27.1.darwin-arm64.tar.gz` |
| Publisher CDN URL | `https://dl.google.com/go/go1.27.1.darwin-arm64.tar.gz` |
| Publisher-rounded size | 65 MB; exact byte length must be recorded during an approved acquisition |
| SHA-256 | `ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12` |
| License | [Go BSD-style license](https://go.dev/LICENSE) |

Go's own download page publishes the artifact and SHA-256. The Go project's [`golang.org/dl` implementation](https://go.googlesource.com/dl/+/refs/heads/master/internal/version/version.go) constructs release URLs under `https://dl.google.com/go/`; the release infrastructure source also describes `dl.google.com/go` as the edge-cache location. This primary evidence explains the 302 observed at Checkpoint A.

## Expected redirects and proposed hosts

Expected route:

1. optional metadata read from `go.dev`;
2. exact archive request to `dl.google.com/go/go1.27.1.darwin-arm64.tar.gz`, either directly or after the observed 302;
3. no additional redirect host.

Proposed R2 acquisition hosts:

- `go.dev`, release metadata only;
- `dl.google.com`, restricted to the exact Go 1.27.1 macOS arm64 archive path.

This is a proposed future addition. The accepted allowlist is not changed by R1.

## Integrity and signature method

The publisher advertises a SHA-256 but no detached signature for this archive on the release page. The proposed verification chain is therefore:

1. record the exact publisher metadata page and hash before download;
2. acquire only the named archive;
3. independently compute SHA-256 and exact byte length;
4. reject a mismatch before extraction;
5. inspect archive paths, types, ownership metadata, links, devices, and expansion size without executing binaries;
6. extract only to a fresh sentinel-bearing owner-only root;
7. record `go version` only in a separately approved execution stage.

TLS and a matching published hash establish the accepted byte route but do not constitute a signed artifact. The signature/proof field must remain `publisher SHA-256; no detached signature advertised`.

## Installation and runtime side effects

The archive route avoids the macOS `.pkg` installer and system path modifications. A future extraction must remain under the disposable root and must not write `/usr/local/go`, `/etc/paths.d/go`, a shell profile, or Homebrew state.

Executing the Go tool later can create or modify:

- `GOENV` user configuration;
- `GOCACHE` build cache;
- `GOMODCACHE` module cache;
- `GOPATH` and its `bin` directory;
- checksum-database cache records;
- temporary build files;
- network requests through `GOPROXY`, `GOSUMDB`, direct VCS, or toolchain auto-selection if not constrained.

Any later approved execution must pin `GOROOT`, `GOPATH`, `GOBIN`, `GOCACHE`, `GOMODCACHE`, and `GOENV` inside the sentinel root; disable toolchain auto-download; set `GOPROXY` and `GOSUMDB` exactly; prohibit `direct` fallback; and disable interactive VCS/authentication paths.

## Rollback

Because the route is archive-only and owner-local, rollback can be exact:

1. stop only processes whose executable and working directory resolve under the sentinel root;
2. reconcile created paths with the run inventory;
3. validate owner, realpath, permissions, sentinel, and non-mount/non-symlink status;
4. remove only the exact extraction/cache root;
5. confirm no Go path/profile/system file was written and no process remains.

No package receipt, privileged helper, service, login item, or system uninstall is expected.

## Module distribution route

The official [Go Modules Reference](https://go.dev/ref/mod) establishes:

- `proxy.golang.org` as the public module proxy;
- `sum.golang.org` as the public checksum database;
- `.info`, `.mod`, and `.zip` proxy objects;
- content-hash verification through `go.sum` and the checksum database;
- `go list -m all` and `go mod graph` as graph evidence;
- `GOPROXY=off` as the no-network setting;
- `go mod verify` as a cache-modification check.

Checkpoint A observed direct 200 responses from both accepted hosts for the six reviewed modules. No redirect host is expected. Any future 3xx outside those hosts is a stop.

### Currently reviewed modules

| Module | Version | Publisher/source | License source |
|---|---:|---|---|
| `github.com/jackc/pgx/v5` | v5.11.0 | `https://github.com/jackc/pgx` | Versioned repository license; MIT |
| `github.com/jackc/pgpassfile` | v1.0.0 | `https://github.com/jackc/pgpassfile` | Versioned repository license; MIT |
| `github.com/jackc/pgservicefile` | v0.0.0-20240606120523-5a60cdf6a761 | `https://github.com/jackc/pgservicefile` | Versioned repository license; MIT |
| `github.com/jackc/puddle/v2` | v2.2.2 | `https://github.com/jackc/puddle` | Versioned repository license; MIT |
| `golang.org/x/sync` | v0.17.0 | `https://go.googlesource.com/sync` | Versioned repository license; BSD-3-Clause-style |
| `golang.org/x/text` | v0.29.0 | `https://go.googlesource.com/text` | Versioned repository license; BSD-3-Clause-style |

### Discovered graph members requiring disposition

| Module | Version | Primary source | License evidence | Proposed classification before graph computation |
|---|---:|---|---|---|
| `github.com/stretchr/testify` | v1.11.1 | [Versioned release](https://github.com/stretchr/testify/releases/tag/v1.11.1) | [MIT](https://github.com/stretchr/testify) | pgx test/module-graph input; not presumed runtime |
| `github.com/davecgh/go-spew` | v1.1.1 | `https://github.com/davecgh/go-spew` | [ISC](https://github.com/davecgh/go-spew) | testify transitive; not presumed runtime |
| `github.com/kr/pretty` | v0.3.0 | [Versioned tag](https://github.com/kr/pretty/tree/v0.3.0) | Versioned `License`; MIT | check transitive; not presumed runtime |
| `github.com/pmezard/go-difflib` | v1.0.0 | `https://github.com/pmezard/go-difflib` | Versioned `LICENSE`; BSD-3-Clause | testify transitive; not presumed runtime |
| `gopkg.in/check.v1` | v1.0.0-20201130134442-10cb98267c6c | `https://github.com/go-check/check` at commit `10cb98267c6c` | Versioned `LICENSE`; BSD-2-Clause | pgx/module-test graph input; not presumed runtime |
| `gopkg.in/yaml.v3` | v3.0.1 | [Versioned source](https://github.com/go-yaml/yaml/tree/v3.0.1) | [MIT and Apache-2.0](https://github.com/go-yaml/yaml) | testify transitive; not presumed runtime |
| `golang.org/x/tools` | v0.36.0 | [Versioned source](https://go.googlesource.com/tools/+/refs/tags/v0.36.0) | Versioned `LICENSE` and `PATENTS`; BSD-3-Clause-style | x/text tooling/tagx graph input; not presumed runtime |
| `golang.org/x/mod` | v0.27.0 | [Versioned source](https://go.googlesource.com/mod/+/refs/tags/v0.27.0) | Versioned `LICENSE` and `PATENTS`; BSD-3-Clause-style | x/tools/tooling graph input; not presumed runtime |

These classifications are hypotheses from published module files, not authoritative build-list results. No module may be dropped merely because it appears test-related, and none may be called runtime-linked without package/import evidence.

## Proposed graph sequence

1. Acquire and verify only the Go toolchain under a separately accepted R2 manifest.
2. Stop and review toolchain evidence before execution.
3. In a later approved metadata-only pass, use the six retained `.mod` files plus exact main-module metadata to compute `go mod graph` and `go list -m all` without downloading ZIP payloads.
4. If the command requests any unlisted `.mod` metadata, stop and add it to the proposed graph before access.
5. Present selected versions, graph edges, package-import reasons, license sources, and exact `.info/.mod/.zip/sumdb` request set.
6. Only after graph approval may module ZIP payloads be acquired.

The authoritative graph must be frozen before build; the current `go.sum.partial` remains evidence only.

## Proposed route change

The future R2 diff may add `dl.google.com` for the exact toolchain archive and may name the eight discovered modules as **metadata-only graph candidates**. It must not authorize their ZIP payloads, compile candidate code, or treat graph closure as stack selection.
