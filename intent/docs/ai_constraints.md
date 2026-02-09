# AI Constraints

These constraints are the system’s “laws of physics.” They keep work safe, legible, and compounding.

## Prioritization rules

1. **Safety over speed** when a change is hard to undo.
2. **Clarity over cleverness.** Prefer obvious solutions.
3. **Smallest useful artifact first.** Ship slices, not epics.
4. **Reversibility first.** Choose options that preserve future flexibility.

## Execution constraints

- **No premature optimization.** Optimize only after measuring a bottleneck.
- **No heavy refactors without intent.** Refactors must be explicitly requested and scoped.
- **No silent scope expansion.** Any scope change must be labeled and justified.
- **Prefer explicit assumptions.** If information is missing, write it down (see `intent/docs/memory/assumptions.md`).
- **Make progress observable.** A run should end with something reviewable.

## Design constraints (generic)

- Prefer **simple interfaces** and **clear ownership** of responsibilities.
- Avoid coupling decisions across unrelated domains.
- When uncertain, choose the path that creates **learning** fastest.
