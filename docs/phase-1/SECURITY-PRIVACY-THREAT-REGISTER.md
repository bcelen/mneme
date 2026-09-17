# Security and Privacy Threat Register

**Status:** Accepted
**Review date:** 2026-09-17
**Authority:** ADR-004
**Assessment boundary:** Planning analysis over synthetic scenarios only; no external authentication, real data, live services, or implementation testing.

## Rating and ownership

Risk ratings are preliminary and describe inherent risk before controls: **Low**, **Medium**, **High**, or **Critical**. Residual risk cannot be accepted until the proposed controls have implementation evidence and the accountable reviewer approves it. “Owner” names a specialist role, not a specific person.

## Register summary

| ID | Threat | Primary assets | Inherent risk | Proposed owner | Required evidence | Residual-risk posture |
|---|---|---|---|---|---|---|
| THR-001 | Unapproved or overbroad acquisition | Privacy, credentials, scope control | Critical | Preservation/corpus + security/privacy | Scope enforcement and no-auth planning test | Unaccepted until importer design review |
| THR-002 | Malicious HTML, remote content, and deceptive links | User device, privacy, network boundary | High | Security/privacy | AT-S01 and AT-S06 | Unaccepted until rendering isolation is proved |
| THR-003 | Parser exploitation or malformed-input escape | Host, source archive, derived state | Critical | Security/privacy | AT-S02 and AT-S07 | Unaccepted until parser isolation is proved |
| THR-004 | Hostile attachments and path traversal | Host, archive, user device | Critical | Security/privacy | AT-S02 and AT-S03 | Unaccepted until attachment controls are proved |
| THR-005 | Resource exhaustion and decompression expansion | Availability, storage, recovery | High | Security/privacy + quality/review | AT-S02, AT-S03, AT-S07 | Unaccepted until enforceable limits exist |
| THR-006 | Prompt injection and agent/tool manipulation | Policy, secrets, archive integrity, answer trust | Critical | Research/AI + security/privacy | AT-S04 | Unaccepted until authority separation is proved |
| THR-007 | OAuth token or provider-credential compromise | External accounts, correspondence, identity | Critical | Security/privacy | AT-S05 plus credential lifecycle review | No real account use until separately approved |
| THR-008 | Network exfiltration or unintended remote fetch | Correspondence, metadata, IP/location privacy | Critical | Security/privacy | AT-S06 | Unaccepted until default-deny behavior is proved |
| THR-009 | Unauthorized local, remote, or administrative access | Entire archive and derived state | Critical | Security/privacy | AT-S08 | Unaccepted until access model is approved |
| THR-010 | Dependency, build, parser, model, or update compromise | Host, archive, build integrity | High | Security/privacy + quality/review | AT-S09 | Unaccepted until supply-chain policy is approved |
| THR-011 | Sensitive leakage through logs, caches, temporary files, or telemetry | Content, credentials, metadata | High | Security/privacy | AT-S05 and AT-S08 | Unaccepted until minimization and deletion are proved |
| THR-012 | Backup or export disclosure, loss, or tampering | Full historical corpus and recovery copies | Critical | Preservation/corpus + security/privacy | AT-R04–R08 and AT-S10 | Unaccepted until verified recovery controls exist |
| THR-013 | Incomplete compromise detection and recovery | Trust in archive, provenance, operations | Critical | Orchestrator + security/privacy | AT-S07, AT-S10, AT-S12 | Unaccepted until a recovery drill passes |
| THR-014 | Unapproved cloud or model-provider transfer | Content, metadata, derived insights | Critical | Research/AI + security/privacy | AT-S11 | Default deny; each service requires separate approval |
| THR-015 | Manifest, provenance, or derived-history tampering | Integrity, citations, auditability | Critical | Preservation/corpus + quality/review | AT-P03–P06 and AT-L01–L06 | Unaccepted until independent verification is proved |

## Required controls and review triggers

### THR-001 — Unapproved or overbroad acquisition

- Require an explicit source-package scope, user authority, exclusions, acquisition route, and stop conditions before any access.
- Separate inventory planning from authentication and import permissions.
- Make empty, extra, or unexpectedly broad acquisitions fail closed and remain quarantined.
- Trigger user review for any source, account, folder, export, date range, or metadata class not named in the approved scope.

### THR-002 — Malicious HTML, remote content, and deceptive links

- Treat HTML as untrusted evidence, not application UI or instructions.
- Prevent script, form, event-handler, plugin, tracker, and remote-resource execution by default.
- Do not fetch images, fonts, styles, links, or previews from source content without a separate user action and policy.
- Preserve original bytes while providing an isolated, clearly labeled safe representation.

### THR-003 — Parser exploitation or malformed-input escape

- Isolate parsing from source-archive write access, credentials, network access, administrative capabilities, and unrelated files.
- Apply least privilege, bounded execution, explicit input/output boundaries, and safe failure.
- Quarantine crashes, unexpected output, or unsupported structures; do not silently skip or repair them.
- Trigger specialist review when adding or changing a parser.

### THR-004 — Hostile attachments and path traversal

- Never execute attachments as part of import, preview, extraction, indexing, or AI context preparation.
- Prevent archive traversal, absolute-path writes, symlink escapes, filename confusion, and content-type trust based only on extension.
- Keep original attachment bytes immutable and separate from any extracted or rendered derivative.
- Require an explicit user action and isolated pathway for opening risky material.

### THR-005 — Resource exhaustion and decompression expansion

- Enforce reviewed limits for input size, nesting, expansion, parser time, memory, output count, and concurrent work.
- Record limit-triggered outcomes as quarantined or incomplete, never as successful preservation.
- Ensure one failing item cannot starve integrity verification, recovery, or unrelated processing.
- Set actual limits only after corpus evidence and capacity review; this register does not choose values.

### THR-006 — Prompt injection and agent/tool manipulation

- Treat message bodies, headers, HTML, attachments, extracted text, OCR, and metadata as untrusted data.
- Keep system policy, user authorization, and tool permissions outside source-controlled context.
- Do not allow content to request tools, network access, credentials, policy changes, source mutation, or uncited claims.
- Require source citations and visible uncertainty; test indirect and encoded instructions as well as plain text.
- Trigger research/AI and security review whenever archive content can reach a model or agent.

### THR-007 — OAuth token or provider-credential compromise

- Use the least privilege and shortest practical lifetime consistent with an approved acquisition.
- Define secure storage, process exposure, rotation, revocation, expiry, audit, and incident procedures before authentication.
- Keep credentials out of source archives, manifests, logs, prompts, exports, test fixtures, and backups unless a separately protected recovery policy explicitly requires them.
- Provider access remains prohibited until a later approval names scopes and data boundaries.

### THR-008 — Network exfiltration or unintended remote fetch

- Default importer, parser, renderer, indexing, and test environments to no outbound network access.
- Make any network dependency explicit, minimal, observable, and separately approved.
- Prevent source-controlled URLs, tracking pixels, external attachments, or AI instructions from initiating traffic.
- Record attempted network use without logging sensitive payloads.

### THR-009 — Unauthorized local, remote, or administrative access

- Define authentication, session, device, privilege, and administrative boundaries before deployment.
- Keep archive, administration, and derived-data interfaces private by default.
- Tailscale remains provisional context and does not substitute for authorization or least privilege.
- Include physical access, stolen device, unattended session, and compromised administrator scenarios in later design review.

### THR-010 — Supply-chain compromise

- Inventory and review direct and transitive dependencies, parsers, build inputs, update channels, models, and external services.
- Require reproducible or independently verifiable provenance where feasible; record exceptions and residual risk.
- Define version control, vulnerability response, update review, artifact verification, and rollback before implementation acceptance.
- Block adoption when ownership, licensing, maintenance, or integrity cannot be assessed.

### THR-011 — Logs, caches, temporary files, and telemetry

- Minimize collection and avoid message content, addresses, attachment text, credentials, and raw prompts by default.
- Define retention, access, redaction, crash-report, temporary-file, and secure-cleanup behavior.
- Treat caches and extracted text as sensitive derived data with provenance and recovery implications.
- Make telemetry opt-in and policy-controlled; no external telemetry is assumed.

### THR-012 — Backup or export disclosure, loss, or tampering

- Protect backups and exports as full-sensitivity copies with integrity, access, encryption, retention, and custody controls.
- Verify manifests and hashes at creation, during periodic checks, and after restore.
- Keep recovery secrets and their recovery process from creating a single point of failure.
- Test complete, stale, corrupt, partial, and unavailable-key scenarios using synthetic data.

### THR-013 — Incomplete compromise detection and recovery

- Define observable indicators, containment authority, credential revocation, network isolation, evidence preservation, and user notification.
- Restore only from independently verified clean sources; review provenance since the last trusted point.
- Rebuild machine-derived data after compromise rather than trusting potentially altered state.
- Require a synthetic recovery drill before production approval and after material security changes.

### THR-014 — Unapproved cloud or model-provider transfer

- Default to no cloud transfer.
- Require a named service, exact data classes, purpose, minimization, region, retention, training-use terms, logging, cost, and deletion behavior before approval.
- Make the routing decision and provider/model identity visible for each approved AI operation.
- Block fallback to an unapproved provider or model.

### THR-015 — Manifest, provenance, or derived-history tampering

- Make integrity evidence independently verifiable and detect missing, added, reordered, or altered records where order matters.
- Restrict who or what may append provenance and user-history events.
- Keep corrections additive and attributable; never rewrite history to conceal a prior state.
- Stop citation, export, or rebuild claims when required lineage cannot be verified.

## Review cadence and escalation

Review the register before selecting a stack, adding an importer or parser, enabling model access, changing backup/export behavior, exposing a network service, or proposing a real-data dry run. New threats receive stable IDs and acceptance tests. Risk acceptance, deferral, or scope reduction requires explicit user approval when it affects privacy, security, external services, production, or real data.
