# Core Rules (Execution)

These rules are designed for fast, reliable solo execution.

## Non-negotiables

1. **Select ONE workflow** for the run (see `intent/docs/workflows.md`).
2. **Activate ONE role at a time** (see `intent/docs/ai_roles.md`).
3. **Produce at least one artifact** before ending the run.
4. **Write decisions to memory** (`intent/memory/decisions.md`) whenever a choice changes future work.

## Operating discipline

- Work in **small steps** that can be reviewed and reversed.
- If you discover missing context, **capture it as an assumption** (`intent/memory/assumptions.md`) or request it explicitly.
- **Do not expand scope silently**. Label scope changes and re-choose a workflow if needed.

## Stop conditions (kill switch)

Stop and summarize blockers if **any** of the following occur:

- **3 iterations** without producing a new artifact.
- The current intent cannot be satisfied without external info not available in the repository.
- Progress becomes primarily speculative (guessing rather than verifying).

When stopping, provide:
1) what was attempted, 2) what is blocked, 3) the smallest next question or experiment.
