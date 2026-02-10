## Language Profiles

Language Profiles define **binding technical rules** for writing and modifying source code.
Each task must select **one Primary Language Profile**.
Optional Extension Profiles may be added to cover adjacent domains.

---

### Primary Language Profiles

These profiles define the core rules of a programming language or primary stack.

- `php-laravel.md`
  Laravel PHP conventions, service boundaries, form requests, policies, testing strategy

- `typescript.md`
  Strict typing, module boundaries, explicit error handling, predictable side effects

- `javascript.md`
  ES6+, no `var`, controlled global state, explicit runtime assumptions

- `python.md`
  Type hints, small functions, explicit IO boundaries, clarity over cleverness

- `sql.md`
  Explicit columns, transactions, `EXPLAIN` usage, no `SELECT *`

- `bash.md`
  Safe scripting, `set -euo pipefail`, strict quoting, defensive defaults

---

### Extension Profiles (Domain / Framework)

These profiles **extend** a primary language profile.
They must not override primary rules.

- `html-css.md`
  Semantic HTML, accessibility basics, layout conventions, CSS hygiene

- `tailwind.md`
  Utility-first styling, class composition rules, responsive and dark-mode patterns

- `livewire.md`
  Livewire component boundaries, state handling, event and lifecycle conventions

- `markdown.md`
  Structured, readable, maintainable Markdown for documentation and specs

---

### Non-Language Profiles (Out of Scope Here)

The following files are **not Language Profiles** and should not be listed as such:

- `product-spec.md`
  Product and requirement specification format (belongs to Identities)

These are intentionally excluded from Language Profile selection.

---

### Rule Summary

- Exactly **one Primary Language Profile** is required for any code change
- Up to **two Extension Profiles** may be added if needed
- Extension Profiles never override Primary rules
- If no suitable Primary Profile exists, execution must stop and a minimal profile must be created first
