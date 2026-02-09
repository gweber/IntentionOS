# Identity: markdown

## Purpose
- Enforce consistent, readable, and maintainable Markdown documentation.
- Support structured content for technical and user-facing documentation.
- Prevent common formatting and semantic issues.

## Hard Rules
- DO use `#` for headings, `##` for subheadings, and so on.
- DO use `**bold**` and `*italic*` for emphasis; avoid `__bold__`.
- DO use `[]()` for links; avoid raw URLs.
- DO use `\` to escape special characters.
- DO use `---` for horizontal rules.
- DO NOT use `#` for styling or layout.
- DO NOT use `![]()` without `alt` text.
- DO NOT use `>` for blockquotes without proper indentation.
- DO NOT use `[]` for links without a target.
- DO NOT use `\` for line breaks without `\n`.

## Defaults
- Naming: Use `snake_case` for file names.
- Formatting: Use 2 spaces after sentence-ending punctuation.
- Error handling: Use `alt` text for images; validate links.
- Testing: Use `markdownlint` or `remark` for linting.

## Patterns We Prefer
- Use `[]()` for links:
  ```md
  [GitHub](https://github.com)
  ```
- Use `---` for section breaks:
  ```md
  ## Configuration

  ---

  Set `env=production` to enable.
  ```
- Use `\` for escaping:
  ```md
  Use `\$` to display a dollar sign.
  ```

## Footguns to Avoid
- Avoid `#` for visual layout.
- Avoid `![]()` without `alt` text.
- Avoid `>` for blockquotes without proper structure.
- Avoid `[]` without a target.

## Definition of Done
- [ ] File exists at `docs/identities/markdown.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
