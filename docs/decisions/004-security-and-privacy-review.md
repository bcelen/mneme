# ADR-004: Security and Privacy Review for Preservation Work

**Status:** Accepted
**Phase:** 1 — Preservation Foundation

## Context

Importers, parsers, previews, AI context, credentials, backups, and network access create distinct risks. Email content is untrusted data and may contain prompt injection, malicious HTML, active links, or hostile attachments.

## Proposal

Before implementation or real-data use, perform a documented review covering:

- importer and parser isolation, resource limits, malformed input, and safe failure;
- non-execution and sanitization of HTML, scripts, links, and attachments;
- prompt injection resistance and strict separation between correspondence content and agent/system instructions;
- OAuth tokens and provider credentials, including least privilege, secure storage, rotation, revocation, and logs;
- dependency, parser, build, model, and other supply-chain risks;
- backups, exports, access control, retention, integrity, and restore paths;
- network exposure, private access, administrative surfaces, and cloud-transfer boundaries;
- logging and telemetry minimization;
- compromise detection, isolation, credential revocation, clean restore, provenance review, and derived-data rebuild.

Each risk must have a mitigation, test or evidence requirement, owner, residual-risk statement, or explicit deferral. No external account authentication is part of this review.

## Alternatives considered

- Rely on provider security and parser defaults: rejected because Mneme combines sources, transformations, and AI workflows with additional attack surfaces.
- Treat imported content as trusted instructions: rejected because correspondence is untrusted input.

## Consequences

Security review becomes a release gate for importers, parsers, AI context, external services, and production exposure. Some mitigations may require later architectural choices, which must be separately proposed and approved.

## Approval boundary

Acceptance authorizes review and synthetic testing. It does not authorize credentials, provider access, real-data import, cloud transfer, or deployment.
