# Assumptions (Memory)

Purpose: capture uncertain facts used to proceed. Assumptions must be testable or revisitable.

## Conventions

- Append-only.
- Every assumption should have a **validation plan** or **expiration**.
- When validated or disproven, add a new entry noting the outcome.

## Template

```
## YYYY-MM-DD — Assumption: <short title>

Context:
- <why we needed to assume>

Assumption:
- <statement believed to be true>

Why it matters:
- <what decisions depend on it>

Validation:
- Method: <how to check>
- By: <date/condition>

Outcome (later):
- <confirmed | disproven | still unknown>
```

## 2026-02-09 — Assumption: The system should stay doc-first until an output surface is chosen

Context:
- Cold Start Alignment: we need boundaries to avoid inventing projects or coding too early.

Assumption:
- Early progress will come primarily from docs (direction, workflows, memory) rather than application code.

Why it matters:
- Prevents premature product building and keeps runs reversible.

Validation:
- Method: Review the next 3 runs and confirm artifacts are mostly docs/checklists (not app code).
- By: After 3 completed runs.

Outcome (later):
- still unknown

## 2026-02-09 — Assumption: A single “output surface” can be selected in one focused run

Context:
- Drift → Realignment requires choosing one new focus; we identified “output surface” as the key missing alignment.

Assumption:
- We can choose one initial output surface (tool vs content vs service vs OSS) without requiring extensive market research.

Why it matters:
- Many future intents depend on a concrete definition of “shipped”.

Validation:
- Method: Run a Decision → Commit workflow limited to 30 minutes and record the chosen surface + a minimal ship definition.
- By: Next run.

Outcome (later):
- still unknown

## 2026-02-09 — Assumption: Small runs (≤45 minutes) are sufficient to compound clarity

Context:
- This is a solo system; throughput depends on repeatability and low setup cost.

Assumption:
- Time-boxed runs (target ≤45 minutes) will produce enough durable artifacts to improve alignment week over week.

Why it matters:
- If false, the operating cadence/constraints need adjustment (longer sessions or different artifact targets).

Validation:
- Method: Track 5 runs; confirm each ends with at least one durable artifact + a clear next intent.
- By: After 5 runs.

Outcome (later):
- still unknown

## 2026-02-09 — Assumption: Issue #1 can be drafted before the publishing surface is selected

Context:
- Issue #1 execution requires a stable public URL + working subscription + working reply path.
- The publishing platform is not chosen yet, but we still want a publishable text artifact.

Assumption:
- It is useful to draft Issue #1 with placeholders for the public URL and reply address, and fill them once the platform is selected.

Why it matters:
- Unblocks writing and review while platform selection is pending.

Validation:
- Method: Once a platform is chosen, replace placeholders (URL + reply path), publish, and confirm the live issue matches the draft.
- By: Before sending Issue #1 to 10 people.

Outcome (later):
- still unknown
