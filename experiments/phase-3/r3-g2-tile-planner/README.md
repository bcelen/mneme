# R3-G2 Literal Checksum-Tile Planner

**P2-01 status:** Accepted as an implementation-review prerequisite only

**Review date:** 2026-09-18

**Authority:** Static source acceptance only; no dependency, copied source,
build, test, execution, retained-input access, verifier, key, network action,
or generated output is authorized

**Build state:** Not authorized and intentionally incomplete until P2-02

**Execution state:** Not authorized

This isolated Phase-3 evidence tool is designed to derive a conservative,
literal checksum-tile path set from structurally valid Go checksum-database
lookup responses. It does not authenticate a response, signature, tree,
record, module hash, or tile.

## Current boundary

P2-01 contains only planner-owned source and its review manifest. It contains
no copied transparency-log implementation, license copy, synthetic fixture,
test, retained response, verifier key, credential, dependency, binary, or
generated planner output.

The source references the future local package `internal/tlog`. That package is
deliberately absent at P2-01. P2-02 must separately present the three exact,
hash-pinned Go 1.27.1 transparency-log source files and BSD license bytes for
review. This package must therefore not be built, tested, installed, or run at
P2-01.

## Safety properties encoded in planner-owned source

- Exact `plan` mode, tile height 8, and accepted hard caps are mandatory.
- The input manifest must declare exactly `L01` through `L14` and normalized
  `lookups/<ID>.lookup` destinations.
- Inputs are bounded, hash-checked, regular non-symlink files beneath the
  evaluated input root; undeclared directory entries stop planning.
- Signed notes are parsed as untrusted structure only. No verifier key,
  signature verification, Merkle verification, network package, process
  launch, cache, user-home lookup, service, or listener exists in the source.
- Every tile derivation uses a recording reader that returns
  `MNEME_PLAN_ONLY_TILE_CAPTURE`; `SaveTiles` is a hard stop.
- Every partial primary path receives a deterministic full-width fallback
  candidate. Data-tile paths and noncanonical paths stop planning.
- Outputs are deterministic, bounded, LF-terminated, and created only with
  exclusive file creation in an already empty output directory.
- The strongest possible result is `Structurally sufficient for literal tile
  planning`; it is explicitly not a checksum-integrity pass.

## Command contract

The accepted future command surface is:

```text
mneme-r3-g2-tile-plan \
  --mode plan \
  --input-manifest <literal-path> \
  --input-root <literal-path> \
  --tile-height 8 \
  --max-inputs 14 \
  --max-heads 14 \
  --max-operations 400 \
  --max-literal-paths 4096 \
  --output-root <literal-path>
```

This command is documentary at P2-01. No build or execution authority follows
from the presence of source.

## P2 sequence

1. **P2-01:** Accepted 2026-09-18 as an implementation-review prerequisite
   only; planner-owned source and `planner-owned-source-manifest.tsv` are
   frozen by the accepted commit.
2. **P2-02:** separately review exact copied tlog source and license bytes.
3. **P2-03:** separately review synthetic fixtures and tests.
4. **P2-04:** conduct the seven-function implementation review over the frozen
   combined diff.

P3 build or test work remains blocked until all four P2 items are individually
accepted. Retained-input access remains blocked until the later P4-E gate.
