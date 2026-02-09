# Identity: html-css

## Purpose
- Enforce consistent, accessible, and maintainable HTML and CSS.
- Prevent common accessibility and performance issues.
- Support modular, reusable UI components.

## Hard Rules
- DO use semantic HTML (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`).
- DO use `aria-*` attributes for accessibility.
- DO use `class` for styling; avoid `style` attribute.
- DO use `:focus-visible` for focus states.
- DO use `rem` for font sizes; avoid `px`.
- DO NOT use `!important`.
- DO NOT use `float` for layout.
- DO NOT use `inline` styles.
- DO NOT use `position: absolute` without `z-index`.
- DO NOT use `display: none` for hiding content.

## Defaults
- Naming: `kebab-case` for classes, `PascalCase` for components.
- Formatting: Use 2-space indentation; no trailing whitespace.
- Error handling: Use `aria-hidden` for decorative elements.
- Testing: Use `axe` or `Lighthouse` for accessibility audits.

## Patterns We Prefer
- Use semantic HTML and ARIA:
  ```html
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/home">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
  ```
- Use `:focus-visible` for focus states:
  ```css
  button {
      outline: none;
  }

  button:focus-visible {
      outline: 2px solid #007bff;
      outline-offset: 2px;
  }
  ```

## Footguns to Avoid
- Avoid `!important` in any context.
- Avoid `float` for layout.
- Avoid `position: absolute` without `z-index`.
- Avoid `display: none` for hiding content.

## Definition of Done
- [ ] File exists at `docs/identities/html-css.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
