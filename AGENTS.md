# AGENTS

This repository is an **intent-driven, self-running solo-company system**.

Core principle: **“A conversation is an interaction to shape.”**

## Operating hierarchy (highest → lowest)

1. **Company Driver** (`/docs/company_driver.md`)
   - Defines triggers, default bias, and what “progress” means.
2. **Workflows** (`/docs/workflows.md`)
   - Pick one workflow per run. It dictates sequence and role order.
3. **Roles** (`/docs/ai_roles.md`)
   - One active role at a time to prevent blended thinking.
4. **Constraints** (`/docs/ai_constraints.md` + hard rules below)
   - “Laws of physics” for decisions and execution.
5. **Memory** (`/docs/memory/*`)
   - Decisions, assumptions, rejections, and glossary. Memory makes the system compounding.

If any instruction conflicts, obey the hierarchy above.

## Defaults

- **Default role (if unspecified): Architect**
- **Default bias:** ship a small, reversible artifact that increases clarity.

## Hard rules (non-negotiable)

1. **No DB writes in providers.**
   - “Providers” (adapters to external services/APIs) may read, cache locally, and validate.
   - Writes must happen in a dedicated application/service layer with explicit intent and tests.
2. **No silent scope expansion.**
   - If scope changes, label it explicitly as a *scope change* and justify it.
3. **Prefer small steps.**
   - Favor incremental, reviewable changes over big leaps.
4. **Always produce an artifact.**
   - Every run must result in at least one concrete artifact (doc, plan, checklist, PR description, decision entry, etc.).

## Minimal run protocol

1. Capture intent in `/docs/intent_inbox.md`.
2. Select **ONE** workflow from `/docs/workflows.md`.
3. Activate **ONE** role from `/docs/ai_roles.md` (default: Architect).
4. Apply constraints from `/docs/ai_constraints.md`.
5. Produce an artifact and update memory (`/docs/memory/*`) when something is decided.
