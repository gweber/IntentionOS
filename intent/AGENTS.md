# AGENTS

This repository is an **intent-driven, self-running solo-company system**.

Core principle: **“A conversation is an interaction to shape.”**

## Operating hierarchy (highest → lowest)

1. **Company Driver** (`intent/docs/company_driver.md`)
   - Defines triggers, default bias, and what “progress” means.
2. **Workflows** (`intent/docs/workflows.md`)
   - Pick one workflow per run. It dictates sequence and role order.
3. **Roles** (`intent/docs/ai_roles.md`)
   - One active role at a time to prevent blended thinking.
4. **Constraints** (`intent/docs/ai_constraints.md` + hard rules below)
   - “Laws of physics” for decisions and execution.
5. **Memory** (`intent/docs/memory/*`)
   - Decisions, assumptions, rejections, and glossary. Memory makes the system compounding.

If any instruction conflicts, obey the hierarchy above.

## Defaults

- **Default role (if unspecified): Architect**
- **Default bias:** ship a small, reversible artifact that increases clarity.

## Hard rules (non-negotiable)

1. No persistent writes in adapters/bootstrap.
   - “Providers/Adapters” (connections to external APIs/LLMs, loaders, bootstrapping code) may read, validate, and locally cache data. Persistent writes (databases, files outside an explicit cache, configuration changes) must occur only in a dedicated application/service layer with explicit intent and tests/guardrails.
2. **No silent scope expansion.**
   - If scope changes, label it explicitly as a *scope change* and justify it.
3. **Prefer small steps.**
   - Favor incremental, reviewable changes over big leaps.
4. **Always produce an artifact.**
   - Every run must result in at least one concrete artifact (doc, plan, checklist, PR description, decision entry, etc.).

## Minimal run protocol

1. Capture intent in `intent/docs/intent_inbox.md`.
2. Select **ONE** workflow from `intent/docs/workflows.md`.
3. Activate **ONE** role from `intent/docs/ai_roles.md` (default: Architect).
4. Apply constraints from `intent/docs/ai_constraints.md`.
5. Produce an artifact and update memory (`intent/docs/memory/*`) when something is decided.
