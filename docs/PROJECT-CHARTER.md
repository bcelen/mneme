# Mneme Project Charter

## Mission

Build a private, intelligent archive of personal correspondence that helps one person research their own history without surrendering control of the underlying record. Sending email is out of scope; Mneme researches preserved correspondence and does not act as a mail client or outbound messaging system.

## System boundary

Mneme is a single-user personal correspondence research system. “Read-only” applies to the preserved source archive: source bytes are never edited in place. Derived annotations, identity links, classifications, indexes, and other views may be created or changed by the user or authorized workflows when those changes are reversible and do not rewrite the source archive. For derived data, reversible means either undoable through recorded history or fully reconstructible from the source archive and processing rules.

The **source archive** means the preserved, imported source record: messages, sent mail, attachments, documents, and provider metadata. **Derived data** means anything computed, extracted, linked, classified, summarized, indexed, or annotated from that source archive.

The planned corpus includes Gmail/Google Workspace, Outlook, Eudora, MBOX, and EML sources, including sent mail, attachments, and provider metadata.

## Accepted product principles

- Preserve a byte-faithful, application-independent source archive.
- Support deterministic retrieval and source-grounded research with citations and provenance.
- Keep all derived data rebuildable and distinguish evidence from interpretation.
- Treat people, identities, organizations, messages, conversations, attachments, documents, topics, events, relationships, and timelines as first-class conceptual entities.
- Provide a beautiful, fast, low-maintenance single-user experience across Mac, iPhone, and iPad.
- Keep sending email outside the product boundary.

## Provisional deployment context

An Ubuntu 24.04 home server, Docker, ZFS, and Tailscale are current deployment context and hypotheses, not accepted product or implementation commitments. Later decisions must preserve portability and require explicit review.

## Product commitments

1. Preserve an immutable source archive.
2. Make derived indexes, annotations, and classifications reconstructible.
3. Provide deterministic Find independently of AI.
4. Provide source-grounded AI Ask with citations and provenance.
5. Support ambitious historical and research use cases while clearly separating evidence from interpretation.
6. Use cloud and local AI only through controlled, explicit policy.

## Preservation commitments

Source ingestion must preserve source bytes and record hashes, manifests, provenance, and the relationship between each source item and its derived data. The archive must be exportable in an application-independent form, backed up, restorable, and subject to restore verification. Indexes and derived data must be rebuildable from the preserved source archive and recorded processing history.

## Phase-0 exit condition

The project has a reviewed control plane: scope, requirements, principles, privacy policy, agent governance, and decision-record structure. No runtime implementation is implied by this phase.
