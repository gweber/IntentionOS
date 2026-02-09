# Company Driver

This document defines how the company “steers” work from captured intent to structured execution.

## Triggers (when to start a run)

Start a run when any of the following is true:

- A new intent is captured in `docs/intent_inbox.md`.
- You feel friction (confusion, slow progress, recurring mistakes).
- The work drifts (busy, but not aligned).
- You are preparing to ship/release.
- You learned something worth codifying.

## Default bias

1. **Clarity before complexity.** Prefer the smallest step that increases clarity.
2. **Artifacts over opinions.** A tangible output beats a strong hunch.
3. **Reversible decisions by default.** Avoid locking into irreversible choices early.

## Initial Direction (Cold Start Alignment)

This repository is the operating system for a solo company.

- **North Star:** compound clarity into consistent output (shipping small, reviewable artifacts that reduce uncertainty).
- **What we are building (for now):** a lightweight, documentation-first execution system that turns intent → action → memory.
- **What we are not doing (yet):** product/application development, multi-project portfolio planning, or tooling-heavy automation.
- **Primary constraint:** keep runs small, reversible, and legible; prefer docs and checklists over code.
- **Success signal (near-term):** weekly evidence of compounding: fewer repeated confusions + clearer next actions + durable memory entries.

### Open question (to resolve soon)

What is the first concrete “output surface” we want this company to ship against (e.g., a small software tool, a content series, a service offering)?

## What counts as “progress”

Progress is any change that reduces uncertainty or increases throughput **without** increasing fragility.

Examples:

- A clearly scoped plan with acceptance criteria.
- A decision recorded with consequences.
- A workflow/runbook that prevents repeated mistakes.
- A shipped increment (or a defined release checklist).
- A rejected path documented so it is not re-litigated.

## When to stop

Stop the run when one is true:

- The selected workflow is complete and at least one artifact was produced.
- The next step requires new external information.
- You hit the kill switch in `.clinerules/core.md`.

Always end with: **Next intent** (one sentence) + **Next smallest step** (one action).
