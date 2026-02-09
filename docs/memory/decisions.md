# Decisions (Memory)

Purpose: record decisions that change future work.

## Conventions

- Append-only. Do not edit old decisions; supersede them with a new entry.
- Prefer explicit tradeoffs and consequences.
- Link to related intents by quoting the intent line or date.

## Template

```
## YYYY-MM-DD — Decision: <short title>

Context:
- <what prompted the decision>
- <relevant constraints>

Decision:
- <what we chose>

Alternatives considered:
- <option A> — <why not>
- <option B> — <why not>

Consequences:
- Immediate: <what changes now>
- Later: <what this enables/blocks>

Follow-up:
- <a small check/experiment to validate>
```

## 2026-02-09 — Decision: Cold Start Alignment baseline + next realignment focus

Context:
- Repository is a fresh company system (“no project yet”).
- Goal of the run: establish initial direction, boundaries, and operating assumptions.
- Constraints: one workflow per run; one role at a time; artifacts over opinions; no silent scope expansion.

Decision:
- Use **Drift → Realignment** as the operational workflow for this run.
- Set the **single focus for the next run** to: choose the first concrete **output surface** we will ship against.

Alternatives considered:
- Start building application code now — rejected (violates doc-first boundary; high chance of invented scope).
- Pick a multi-project roadmap — rejected (too early; increases fragility).

Consequences:
- Immediate: direction is explicitly doc-first; open question is acknowledged rather than forced.
- Later: once an output surface is chosen, “shipped” can be defined and subsequent intents can be evaluated against it.

Follow-up:
- Run **Decision → Commit** to choose the output surface and write a 5-line “definition of shipped” for it.

## 2026-02-09 — Decision: First output surface is a public weekly “Company Log” newsletter

Context:
- No product exists yet; we need the smallest surface that can reach real humans and produce feedback.
- Constraints: solo-executable; objectively checkable “shipped”; momentum over infrastructure.

Decision:
- The first concrete output surface is a **public weekly “Company Log” newsletter** (written update) with an explicit ask for replies.

Definition of Shipped (5 lines):
1) Issue #1 is published at a stable public URL (no login required).
2) Issue #1 contains: a one-sentence promise, this week’s focus, and one explicit question for readers.
3) Email subscription is enabled and a test subscription successfully receives the issue.
4) A visible reply path exists (reply-to works or a contact email is listed in the issue).
5) The URL is sent to 10 specific people asking for feedback.

Alternatives considered:
- Landing page + waitlist form — rejected (adds infrastructure/design overhead before we have narrative clarity).
- Shipping a prototype/app immediately — rejected (high scope risk; no clear user promise yet).

Consequences:
- Immediate: weekly cadence becomes the forcing function; writing precedes building.
- Later: subscriber replies + qualitative feedback define what to build and for whom.

Follow-up:
- Publish Issue #1 and record 3 key feedback points as new intents.

## 2026-02-09 — Shipped confirmation (artifact): Issue #1 newsletter text drafted

Context:
- Issue #1 execution plan requires a publishable Issue #1 draft.
- Publishing surface (stable public URL) + subscription + reply-to are not selected/configured yet.

Confirmation:
- The publishable Issue #1 newsletter text exists at: `docs/company_log/issue_01.md`.

Notes:
- This does **not** satisfy the full “Definition of Shipped” for the newsletter output surface yet (public URL, subscription test, reply path test, outreach to 10 people remain).
