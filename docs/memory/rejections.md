# Rejections (Memory)

Purpose: document paths intentionally not taken, so they are not re-litigated.

## 2026-02-09 — Rejection: Start building application code during Cold Start Alignment

Context:
- This repository is a fresh company system; the goal is initial direction and boundaries.

Rejected path:
- Implement product/application code before selecting a concrete output surface.

Why rejected:
- High risk of invented scope and irreversible coupling.
- The system’s default bias is clarity-first and reversible decisions.

Revisit when:
- An output surface is chosen and “shipped” is defined.

## 2026-02-09 — Rejection: Make the first output surface a landing page + waitlist

Context:
- Choosing a first output surface that is finishable solo and yields real-world feedback fast.

Rejected approach:
- Start with a website/landing page and collect emails via a form.

Reason:
- Requires design + deployment + form/CRM choices before we’ve earned narrative clarity; slower feedback loop than writing.

Reconsider if:
- The newsletter consistently produces demand and we need a canonical home for onboarding.

Alternative:
- Publish a public weekly “Company Log” newsletter with an explicit question and reply path.

## 2026-02-09 — Rejection: Start with a prototype/app as the public surface

Context:
- No validated promise or user segment yet.

Rejected approach:
- Build and ship an MVP/prototype first to “see what happens.”

Reason:
- High risk of invented scope and wasted build cycles; feedback becomes about UI details instead of the underlying problem.

Reconsider if:
- The Company Log converges on a specific user + promise and we can name a tight 1-week build.

Alternative:
- Use writing to force specificity and pull real replies before building.

## Conventions

- Append-only.
- Reject ideas with respect; focus on constraints and tradeoffs.
- A rejection can be temporary. Mark when it can be reconsidered.

## Template

```
## YYYY-MM-DD — Rejection: <short title>

Context:
- <what prompted evaluation>

Rejected approach:
- <what we are not doing>

Reason:
- <constraint/tradeoff>

Reconsider if:
- <condition that would change the decision>

Alternative:
- <what we do instead>
```

# prompt 4

<task>
Plan the execution of Company Log — Issue #1.

You MUST:
1) Select exactly ONE workflow: execution_slice.
2) Activate exactly ONE role: Architect.
3) Convert the committed “Definition of Shipped” into a small, finite task list.
4) Each task must be concrete, checkable, and completable by one person.
5) Stop after producing the plan. No writing of the newsletter yet.

Do NOT:
- Revisit or question the decision
- Add scope
- Improve the idea
- Involve other roles
</task>

<context>
The output surface is fixed:
Public weekly “Company Log” newsletter.

The Definition of Shipped for Issue #1 is already recorded in docs/memory/decisions.md.

This step exists only to reduce ambiguity and create momentum.
</context>

<workflow>
execution_slice
</workflow>

<role>
Initialize Architect: Reduce the committed output to a minimal, executable plan.
</role>

<expected_artifacts>
- A checklist or task list written to docs/workflows.md OR a new file docs/company_log/issue_01_plan.md
- 3–7 tasks maximum
- Each task phrased as “Done when …”
</expected_artifacts>
