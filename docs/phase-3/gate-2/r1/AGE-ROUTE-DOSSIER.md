# R1 age Verification Route Dossier

**Status:** Accepted
**Review date:** 2026-09-18
**Evidence date:** 2026-09-18
**Route outcome:** Blocked pending an exact, independently reviewable Sigsum verifier graph.

## Exact publisher route

| Field | Evidence |
|---|---|
| Publisher project | [`FiloSottile/age`](https://github.com/FiloSottile/age) |
| Release | [age v1.3.2](https://github.com/FiloSottile/age/releases/tag/v1.3.2), commit `b74dce4` |
| Archive | `age-v1.3.2-darwin-arm64.tar.gz` |
| Archive URL | `https://github.com/FiloSottile/age/releases/download/v1.3.2/age-v1.3.2-darwin-arm64.tar.gz` |
| Archive bytes | 18,106,798 |
| Archive SHA-256 | `e2020b073c44f692685a24d6abc378817eb81ffaaf49fd0531ef8565f767f2f5` |
| Proof | `age-v1.3.2-darwin-arm64.tar.gz.proof` |
| Proof URL | `https://github.com/FiloSottile/age/releases/download/v1.3.2/age-v1.3.2-darwin-arm64.tar.gz.proof` |
| Proof bytes | 1,921 |
| Proof SHA-256 | `26e3fcc371f19e35c7d37500baf8e82c4386538dc6f47e66f4e0fefec50531e4` |
| License | [age BSD-3-Clause license](https://github.com/FiloSottile/age/blob/main/LICENSE) |

The project [README](https://github.com/FiloSottile/age/blob/main/README.md) identifies prebuilt macOS arm64 binaries and directs users to verify their Sigsum proofs.

## Expected redirects and hosts

Checkpoint A observed both exact GitHub URLs redirect by HTTP 302 to `release-assets.githubusercontent.com`, with no additional asset host.

Artifact hosts already accepted:

- `github.com`;
- `release-assets.githubusercontent.com`.

The project's convenience download host `dl.filippo.io` is documented but is unnecessary because the exact GitHub asset route and bytes are already known. It is not proposed for the acquisition allowlist.

No age artifact reacquisition is proposed. The rejected executable archive was removed; only the proof and normalized evidence remain.

## Integrity and signature method

The exact archive hash matches the publisher's release metadata. Static archive inspection found nine safe entries and no unsafe path, device, or FIFO. The extracted binary had only an ad-hoc linker signature; that signature provides no publisher identity.

The publisher's [Sigsum instructions](https://github.com/FiloSottile/age/blob/main/SIGSUM.md) define the authenticity mechanism:

- two age release Ed25519 public keys:
  - `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM1WpnEswJLPzvXJDiswowy48U+G+G1kmgwUE2eaRHZG`;
  - `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAz2WM5CyPLqiNjk7CLl4roDXwKhQ0QExXLebukZEZFS`;
- verifier module `sigsum.org/sigsum-go/cmd/sigsum-verify@v0.13.1`;
- built-in policy `sigsum-generic-2025-1`;
- proof supplied as a file and archive bytes supplied on standard input.

Sigsum's [verification documentation](https://www.sigsum.org/getting-started/) states that proof verification requires no outbound network connection once the verifier, policy, public key, proof, and artifact are local.

## Verifier trust chain

| Field | R1 evidence |
|---|---|
| Publisher source | Official repository `https://git.glasklar.is/sigsum/core/sigsum-go/`; GitHub is explicitly a mirror |
| Module | `sigsum.org/sigsum-go` |
| Version named by age | v0.13.1 |
| Command | `cmd/sigsum-verify` |
| License | BSD-2-Clause, recorded by the official source repository metadata |
| Proposed distribution | Exact Go module graph via `proxy.golang.org` and `sum.golang.org`; no direct VCS fallback |
| Signature/integrity | Go module content hashes and checksum database, then offline binary provenance from the verified module graph |

The verifier is not a single dependency-free artifact. Its complete module graph, selected versions, hashes, licenses, and build inputs have not been established. Acquiring or building it now would violate the accepted graph-before-payload rule.

There is also a documentation-version caveat: the current age Sigsum page's concrete example names v1.3.1 while the release under review is v1.3.2. The project publishes a v1.3.2 proof, but R1 does not infer that an older example alone proves verifier/policy compatibility. That compatibility must be confirmed from the proof format and accepted verifier source before R2.

## Installer and runtime side effects

The age release archive has no installer. Future approved extraction would write only beneath a sentinel root. Running `age` or `age-keygen` is not required for proof verification and remains prohibited during acquisition.

Building `sigsum-verify` through `go install` would:

- resolve and acquire its Go module graph;
- compile code and write a binary to `GOBIN`;
- populate Go module/build caches;
- potentially contact proxy/checksum services unless all inputs are pre-cached and network disabled.

Those are R3/R4 activities, not R1 or automatic consequences of approving this dossier.

## Proposed hosts

No new acquisition host is proposed yet.

If the verifier graph is later accepted, the preferred distribution route uses only:

- `proxy.golang.org` for exact `.info`, `.mod`, and `.zip` objects;
- `sum.golang.org` for checksum-database authentication.

`git.glasklar.is` and `www.sigsum.org` are publisher/documentation evidence sources, not proposed artifact hosts. `direct` VCS fallback is prohibited.

## Rollback

A future verifier acquisition/build must place `GOROOT`, `GOPATH`, `GOBIN`, `GOCACHE`, `GOMODCACHE`, `GOENV`, source, binary, and evidence beneath one exact sentinel root. Rollback removes only that inventoried root after process and open-file checks. It must leave no binary in a user/system path and no persistent Go environment change.

The age archive/proof evidence remains separately inventoried. No age key, encrypted file, keychain entry, config file, or backup is created during verification-route work.

## Proposed route decision

Keep A1 Blocked until the exact `sigsum-verify@v0.13.1` module graph and policy compatibility with the v1.3.2 proof are documented and reviewed. Do not add the verifier to the accepted dependency manifest in the initial R2 diff.

If that trust chain is disproportionate, A3—remove the age-specific probe and leave encryption-implementation evidence Unproved—remains the bounded alternative. Selecting A3 would not weaken the general backup/restore contract, but it would reduce Phase-3 encryption evidence explicitly.
