# Security Principles

Mneme handles intimate personal correspondence and must be designed as a private system from the start. The source archive is preserved and read-only; derived data may be modified only through controlled, reversible operations. For derived data, reversible means either undoable through recorded history or fully reconstructible from the source archive and processing rules.

- Default to local-only exposure; remote access must use a private network. Tailscale is the current candidate deployment context, not an accepted implementation commitment.
- Do not expose administrative or data interfaces to the public internet by default.
- Protect credentials, encryption material, logs, indexes, caches, and backups as sensitive data.
- Preserve raw data integrity with immutable storage and controlled write paths.
- Separate read access to the archive from write access to derived state.
- Minimize copied data and retain only what is needed for a declared purpose.
- Treat attachments and extracted text as equally sensitive as the original message.
- Treat message bodies, HTML, scripts, links, attachments, and metadata as untrusted input. Prompt injection or instructions embedded in correspondence must never gain authority over the user, system, or agent.
- Isolate parsers and preview/extraction work from the archive and from privileged application capabilities; malformed or malicious HTML and attachments must not execute with trusted privileges.
- Protect OAuth tokens and provider credentials with least privilege, bounded scope, secure storage, rotation, and revocation procedures.
- Review dependencies, build tools, parser libraries, model integrations, and other supply-chain inputs before adoption; pinning or verification policies require later approval.
- Treat backups and exports as sensitive copies: protect access, integrity, retention, and restore paths, and verify that restore procedures work.
- Minimize network exposure and keep administrative, archive, and derived-data surfaces private by default.
- Record provenance for transformations and AI outputs.
- Make cloud transfer opt-in, policy-controlled, and visible to the user.
- Require explicit approval for security-posture changes, external services, production deployment, real-data import, and destructive operations.
- Plan for compromise: revoke access, preserve evidence, restore derived state, and keep the raw archive recoverable.
- Maintain a compromise-recovery path covering credential revocation, token rotation, network isolation, backup integrity checks, clean restoration, derived-data rebuild, and review of affected provenance.

Concrete technologies, threat models, encryption designs, and network policies remain to be selected and recorded in later decision records.
