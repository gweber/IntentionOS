# Workflows

Pick **one** workflow per run. Each workflow lists an ordered sequence and a typical role order.

Role glossary: see `intent/docs/ai_roles.md`.

---

## 1) Idea → Execution

Use when: you have a new idea and want to turn it into a shippable slice.

**Steps**
1. Capture intent (one sentence) + success criteria.
2. Define the smallest valuable artifact.
3. Identify risks/unknowns and the shortest test.
4. Produce a plan (steps, constraints, definition of done).
5. Execute in small increments.
6. Record decisions and update memory.

**Role order**: Visioneer → Strategist → Architect → Breaker → Curator

---

## 2) Friction → Fix

Use when: something feels slow, confusing, brittle, or repeatedly breaks.

**Steps**
1. Describe the friction in observable terms (symptoms, frequency, cost).
2. Reproduce or bound it (what conditions trigger it?).
3. Propose a minimal fix and a guardrail.
4. Validate the fix (tests/checklist).
5. Codify into a rule/runbook.

**Role order**: Breaker → Architect → Curator

---

## 3) Drift → Realignment

Use when: output exists but alignment is missing.

**Steps**
1. Restate current intent and why it matters.
2. Compare work-in-progress to success criteria.
3. Identify what to stop, start, and continue.
4. Choose a new single focus for the next run.
5. Record the realignment decision.

**Role order**: Strategist → Visioneer → Architect → Curator

---

## 4) Release → Ship

Use when: preparing to deliver something to users/audience/stakeholders.

**Steps**
1. Define “shipped” and the release boundary.
2. Prepare a release checklist (quality, comms, rollback).
3. Run a preflight review (known risks + mitigations).
4. Ship the release.
5. Post-ship: record learnings and follow-up intents.

**Role order**: Architect → Breaker → Curator → Strategist

---

## 5) Learning → Codify

Use when: you learned something that should change future behavior.

**Steps**
1. State the lesson as a falsifiable claim.
2. Describe evidence (what happened) and context.
3. Extract a rule, checklist item, or constraint.
4. Update memory and relevant docs.
5. Add a small “practice” intent to reinforce it.

**Role order**: Curator → Strategist → Architect

---

## 6) Decision → Commit

Use when: you are stuck between options and need a reversible choice.

**Steps**
1. Write the decision question and options.
2. Define decision criteria (time, risk, reversibility).
3. Choose the smallest reversible option that unblocks progress.
4. Record the decision + consequence.
5. Create a follow-up intent to validate.

**Role order**: Strategist → Architect → Curator
