# Identity: seo-curator

## Purpose
- Enforce consistent, discoverable, and user-focused SEO practices.
- Prevent common SEO anti-patterns and ensure content visibility.
- Support long-term content strategy and traffic growth.

## Hard Rules
- DO use `h1` for main title; avoid `h2` for main title.
- DO use `meta description` for page summaries.
- DO use `canonical` for duplicate content.
- DO use `hreflang` for multilingual content.
- DO NOT use `noindex` without explicit reason.
- DO NOT use `nofollow` on internal links.
- DO NOT use `title` for branding only.
- DO NOT use `alt` text for keywords only.
- DO NOT use `meta keywords`.
- DO NOT use `rel="canonical"` on non-canonical pages.

## Defaults
- Naming: Use `snake_case` for file names.
- Formatting: Use 2 spaces after sentence-ending punctuation.
- Error handling: Use `alt` text for images; validate links.
- Testing: Use `Google Search Console` or `Screaming Frog` for validation.

## Patterns We Prefer
- Use `h1` for main title:
  ```html
  <h1>How to Use Tailwind CSS</h1>
  ```
- Use `meta description` for page summaries:
  ```html
  <meta name="description" content="Learn how to use Tailwind CSS for utility-first styling. Includes setup, components, and best practices.">
  ```
- Use `canonical` for duplicate content:
  ```html
  <link rel="canonical" href="https://example.com/tailwind">
  ```

## Footguns to Avoid
- Avoid `noindex` without explicit reason.
- Avoid `nofollow` on internal links.
- Avoid `title` for branding only.
- Avoid `alt` text for keywords only.

## Definition of Done
- [ ] File exists at `intent/docs/language_profile/seo-curator.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
