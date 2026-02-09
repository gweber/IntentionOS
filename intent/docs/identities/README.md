# Identities

## Purpose
This directory contains **source documentation** for reusable "identities" that define coding style, preferred patterns, and role/output behaviors across languages, stacks, and roles.

Identities are not agent instructions or runtime constraints. They are reference materials for workflows to select and apply during development.

## How to Use

### Select a Primary Identity
- Choose **one** identity per code task based on the language, stack, or role.
- Use it to guide implementation, testing, and review.

### Optionally Add Secondary Identities
- Add **0–2** secondary identities for context (e.g., `typescript` + `tailwind` for a React app).
- Secondary identities should not override the primary.

## Identity Types

### Language/Stack Identities
- `php-laravel.md`: Laravel PHP conventions, service layer, form requests, policies.
- `typescript.md`: Strict typing, pure functions, error handling.
- `javascript.md`: ES6+ best practices, no `var`, avoid global state.
- `python.md`: Type hints, small functions, explicit IO.
- `sql.md`: Explicit columns, `EXPLAIN`, transactions.
- `bash.md`: Safe scripting, `set -euo pipefail`, `"$VAR"`.
- `markdown.md`: Consistent, readable, maintainable Markdown.
- `html-css.md`: Semantic HTML, `:focus-visible`, `rem`.
- `livewire.md`: Component boundaries, `wire:model`, `@keydown.enter`.
- `tailwind.md`: Utility-first, `dark:`, `hover:`.

### Role/Output Identities
- `code-reviewer.md`: Checklist, severity levels, how to propose changes.
- `incident-debugger.md`: Repro steps, hypotheses, minimal fix, postmortem notes.
- `tech-writer.md`: Docs format, examples, clarity rules.
- `seo-curator.md`: "hubs not bins", merge criteria, when NOT to merge, logging decisions.
- `product-spec.md`: PRD format, acceptance criteria, edge cases, non-goals.
