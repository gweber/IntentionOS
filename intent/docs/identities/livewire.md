# Identity: livewire

## Purpose
- Enforce consistent, performant, and maintainable Livewire component structure.
- Prevent common re-rendering and state management issues.
- Support scalable, reactive UIs.

## Hard Rules
- DO use `wire:model` for two-way binding; avoid `wire:click` for form inputs.
- DO use `wire:click` for actions; avoid `@click` in templates.
- DO use `@poll` for periodic updates.
- DO use `@keydown.enter` for form submission.
- DO NOT use `wire:ignore` unless necessary.
- DO NOT use `wire:loading` without `wire:target`.
- DO NOT use `@click` for form submission.
- DO NOT use `@change` on inputs without `wire:model`.
- DO NOT use `@input` on inputs without `wire:model`.
- DO NOT use `@focus` on inputs without `wire:model`.

## Defaults
- Naming: `PascalCase` for components, `snake_case` for methods.
- Formatting: Use 2-space indentation; no trailing whitespace.
- Error handling: Use `@error` for validation; avoid `@if` for error display.
- Testing: Use `Livewire::test()` for component tests.

## Patterns We Prefer
- Use `wire:model` for form binding:
  ```php
  <input wire:model="email" type="email" />
  ```
- Use `@keydown.enter` for form submission:
  ```php
  <form wire:submit.prevent="save">
      <input wire:model="name" type="text" />
      <button type="submit">Save</button>
  </form>
  ```
- Use `@poll` for periodic updates:
  ```php
  <div wire:poll.3000ms="refreshData">
      {{ $data }}
  </div>
  ```

## Footguns to Avoid
- Avoid `wire:ignore` on large components.
- Avoid `@click` on form inputs.
- Avoid `@change` without `wire:model`.
- Avoid `@input` without `wire:model`.

## Definition of Done
- [ ] File exists at `docs/identities/livewire.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
