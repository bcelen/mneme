# Architecture Decision Records

This directory stores durable records of material decisions made after review. Each record should explain the context, decision, alternatives considered, consequences, approval boundary, and status.

## Status vocabulary

- **Proposed** — under discussion; not an implementation mandate.
- **Accepted** — explicitly approved and governing future work.
- **Superseded** — replaced by a later accepted decision.
- **Rejected** — considered and declined.

## Rules

- Do not use this directory to smuggle in unapproved implementation choices.
- Link decisions to the requirements and principles they affect.
- Record the approval boundary and date when a decision is accepted.
- Keep decisions small enough to review independently.
- Distinguish accepted product principles from provisional deployment context. Ubuntu 24.04, Docker, ZFS, and Tailscale are currently context to evaluate, not accepted implementation decisions.

No architecture decisions have been accepted in Phase 0 beyond the product and governance commitments documented elsewhere in `docs/`.
