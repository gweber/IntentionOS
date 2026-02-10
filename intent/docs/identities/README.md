# Identities

## Purpose
This directory contains **Identities**: reusable reference documents that define a **cognitive stance and output behavior** for non-code-producing work.

Identities describe **how an agent should think, evaluate, structure, and communicate** when performing tasks such as review, analysis, auditing, or documentation.

Identities are **not execution constraints** and **do not define code style**.
They guide reasoning and output quality, not syntax or implementation details.

---

## When Identities Apply

An Identity should be selected when the task primarily involves:
- reviewing existing code
- evaluating quality, risk, or correctness
- producing documentation or specifications
- debugging or incident analysis
- curating, merging, or organizing information

If **source code is being created or modified**, a **Language Profile** is required instead.
Identities may still be used as secondary context, but they are never sufficient on their own for coding tasks.

---

## How to Use

### Select a Primary Identity
- Choose **exactly one** primary Identity per task.
- The Identity defines:
  - reasoning approach
  - evaluation criteria
  - structure of the output
  - tone and level of rigor

### Optional Secondary Identities
- Add **0–1** secondary Identity only if explicitly helpful.
- Secondary Identities must not conflict with the primary Identity.
- If a conflict exists, the **primary Identity wins**.

---

## Scope of an Identity

An Identity may define:
- checklists and heuristics
- severity or priority levels
- decision criteria
- documentation structure
- reporting or feedback formats
- what to focus on and what to ignore

An Identity must **not**:
- define programming language syntax
- define formatting or naming rules for source code
- override Language Profiles
- introduce system-wide policies or constraints

---

## Available Identities

### Review & Quality
- `code-reviewer.md`
  Review checklist, severity levels, how to propose changes

- `incident-debugger.md`
  Reproduction steps, hypotheses, minimal fix, postmortem notes

### Documentation & Communication
- `tech-writer.md`
  Documentation structure, examples, clarity and consistency rules

### Curation & Analysis
- `seo-curator.md`
  “Hubs not bins”, merge criteria, when *not* to merge, decision logging

---

## Relationship to Language Profiles

- **Identities** define *how to think and evaluate*
- **Language Profiles** define *how code must be written*

They serve different purposes and must not be conflated.

---

## Rule Summary

- Non-code task ⇒ Identity required
- Exactly one primary Identity per task
- Identities guide reasoning, not execution
- Code changes always require a Language Profile
