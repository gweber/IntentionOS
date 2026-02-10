# Language Profile: tailwind

## Purpose
- Enforce consistent, utility-first, and maintainable CSS using Tailwind.
- Prevent ad-hoc CSS sprawl and ensure design system alignment.
- Support rapid UI development with reusable, predictable classes.

## Hard Rules
- DO use utility-first classes; avoid custom `style` attributes.
- DO use `@apply` only in `tailwind.config.js` or `theme` sections.
- DO use `dark:` prefix for dark mode variants.
- DO use `hover:`, `focus:`, `active:` for interactive states.
- DO NOT use `!important`.
- DO NOT use `@layer` in component files.
- DO NOT use `@screen` for responsive design.
- DO NOT use `@variants` for custom variants.
- DO NOT use `@import` in CSS files.
- DO NOT use `class` for layout; use Tailwind’s grid and flex utilities.

## Defaults
- Naming: `kebab-case` for classes, `PascalCase` for components.
- Formatting: Use 2-space indentation; no trailing whitespace.
- Error handling: Use `@layer` only in config; avoid inline `@layer`.
- Testing: Use `playwright` or `cypress` for visual regression testing.

## Patterns We Prefer
- Use utility-first classes:
  ```html
  <div class="p-4 bg-gray-100 rounded-lg shadow-sm">
      <h2 class="text-xl font-semibold text-gray-800">Welcome</h2>
      <p class="text-gray-600 mt-2">This is a card.</p>
  </div>
  ```
- Use `dark:` for dark mode:
  ```html
  <div class="dark:bg-gray-800 dark:text-white">
      Content here
  </div>
  ```
- Use `hover:` for interactive states:
  ```html
  <button class="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded">
      Submit
  </button>
  ```

## Footguns to Avoid
- Avoid `!important` in any context.
- Avoid `@layer` in component files.
- Avoid `@screen` for responsive design.
- Avoid `@variants` for custom variants.

## Definition of Done
- [ ] File exists at `intent/docs/language_profiles/tailwind.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
