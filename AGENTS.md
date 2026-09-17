# Agent Governance for Mneme

This file is the operating contract for the orchestrator, specialist agents, and other automated contributors.

## Current phase

Only the Phase-0 project control plane is authorized in the current phase. Do not add application code, dependencies, Docker configuration, infrastructure configuration, migrations, or implementation-stack choices unless the user explicitly authorizes a later phase.

## Autonomy and approval gates

Agents may independently perform reversible, local, well-scoped work that preserves the source archive and does not create external cost or exposure. User approval is required before:

- architecture or schema commitments;
- privacy or security posture changes;
- enabling external services, cloud providers, or paid resources;
- destructive, irreversible, or bulk data operations;
- production deployment or changes to production infrastructure;
- importing or processing real correspondence data.

Agents must explain the proposed change, its consequences, and its rollback or recovery path before an approval gate.

## Multi-agent operating model

The **orchestrator** owns the task brief, scope, sequencing, decision log, risk register, and final integration. It delegates bounded work to specialists and is responsible for resolving conflicts and presenting the reviewable result. Specialist roles may include:

- preservation and corpus: source formats, byte preservation, hashes, manifests, provenance, exports, backups, restore, and rebuildability;
- product and UX: single-user workflows, Find/Ask separation, performance, accessibility, and Mac/iPhone/iPad experience;
- research and AI: evidence grounding, citations, provenance, historical reasoning, model routing, and uncertainty;
- security and privacy: threat modeling, prompt injection, hostile content, credentials, supply chain, network exposure, and recovery;
- quality and review: requirements traceability, test-corpus design, adversarial review, and definition-of-done checks.

Agents must not silently broaden their role or make an unapproved architectural choice. The orchestrator remains accountable for the combined change.

### Staged gates

Work proceeds through explicit gates: **frame** (scope and risks), **design** (proposed decisions and approval needs), **build** (authorized reversible work), **verify** (tests, review, and recovery checks), and **accept** (user approval and recorded decisions). Importing or processing real correspondence is a separate approval gate and must not be bundled into implementation work.

### Review triggers

Request specialist review when work affects source preservation, privacy/security, external data transfer, AI behavior, user-facing research claims, destructive or irreversible actions, production deployment, or any decision likely to constrain future architecture. Use adversarial review for prompt injection, malicious content, provenance gaps, restore failure, and misleading answers.

### Test corpus and definition of done

Before real-data use, maintain a synthetic or explicitly authorized test corpus spanning Gmail/Google Workspace, Outlook, Eudora, MBOX, EML, sent mail, attachments, provider metadata, duplicates, junk, malformed messages, hostile HTML, and representative relationships and timelines. A change is done only when its requirements are traced, relevant specialists have reviewed it, tests and restore/rebuild checks pass, provenance and security implications are documented, user-facing uncertainty is handled, and all required approval gates are closed.

## Data handling

Treat correspondence as sensitive by default. The source archive is immutable and read-only; derived annotations and classifications may be user-controlled when reversible. For derived data, reversible means either undoable through recorded history or fully reconstructible from the source archive and processing rules. Never alter, delete, overwrite, or silently export source data. Keep derived data reproducible from the source archive. Do not place real correspondence, credentials, tokens, or private identifiers in source control, logs, prompts, tests, or examples.

## Working practice

Inspect before editing. Preserve unrelated user changes. Keep changes narrow and reviewable. Record material architectural choices in `docs/decisions/`. Do not commit unless the user explicitly asks.
