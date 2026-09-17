# AI Privacy Policy

## Purpose

AI may help the user search, summarize, interpret, and research their correspondence. It is an assistant over a private source archive, not an owner of that archive. Sending email is out of scope.

## Non-negotiable rules

- The source archive remains under the user's control and is never altered by AI.
- Derived annotations and classifications may be created or revised by user-controlled workflows when reversible and clearly separated from source evidence. For derived data, reversible means either undoable through recorded history or fully reconstructible from the source archive and processing rules.
- AI output is derived work and must not be treated as source truth.
- Answers must be grounded in retrieved source material and include citations/provenance where factual claims are made.
- The system must distinguish quoted or source-supported material from inference, synthesis, and uncertainty.
- No correspondence is sent to a cloud model or external service without an explicit, reviewable policy permitting that transfer.
- Data minimization applies to prompts, context windows, telemetry, logs, caches, and provider retention.
- Provider identity, model identity, routing decision, and relevant policy should be inspectable for each AI operation.
- The user must be able to use deterministic Find without invoking AI.
- Correspondence is untrusted content: prompt injection in messages, HTML, attachments, or metadata must be treated as data, never as instructions.

## Hybrid execution

Local and cloud AI may be used together, but routing is controlled rather than implicit. Sensitive or broad archival questions should have a local path where feasible. Cloud use requires an approved service, defined data boundary, acceptable retention and terms, and a cost/risk decision.

## Failure and refusal

If evidence is missing, contradictory, or inaccessible, AI should disclose that limitation. It must not fabricate citations, identities, chronology, or document contents.

Detailed provider choices, redaction rules, retention periods, consent UX, parser isolation, and token handling are future decisions and are not selected by this policy.
