# Mneme Local Identities 1 — Address Identities

The product requirements separate people from identities: "one person may have multiple addresses or identifiers, and an identity must not be silently treated as a person." This experiment implements only the identity side, at the narrowest level: an **identity is one normalized address**. It never creates or implies a person. Prototype 4 (and through it prototype 3) is loaded by path and left unchanged.

## Model

- Addresses come from the derived `From` and `To` fields of non-quarantined occurrences, normalized with prototype 4's rule: the lower-cased address specification, so display names and case never matter.
- Display names are kept as evidence per identity and per occurrence. They never merge or split identities. `Míra Sol` and `Mira Sol` appear as two display names of `mira.sol@example.test`.
- Each identity reports `occurrences` and `distinct_source_hashes`. Exact-byte duplicates count as occurrences, and the gap between the two numbers makes that visible.
- `first_seen_utc` and `last_seen_utc` use only parseable `Date` headers, normalized to UTC; `undated_occurrences` counts the rest.
- `identity` adds an occurrence list (roles, date, display names, and a subject citation that resolves through `show`) and correspondents: for each other address, how many occurrences this identity sent to it and received from it.

Everything is computed at query time from the verified current generation; no derived state is added or changed.

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-identities-1/mneme_identities.py identities --state <state>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-identities-1/mneme_identities.py identity --state <state> --address mira.sol@example.test
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-identities-1/tests/test_identities.py
```

## Boundary

No people, aliases, organizations, merging, or user annotation. Linking identities to a person is a user-controlled, reversible modeling decision that this experiment deliberately does not make.
