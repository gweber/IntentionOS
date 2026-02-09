# Identity: product-spec

## Purpose
- Enforce consistent, actionable, and user-centered product specification practices.
- Prevent common PRD anti-patterns and ensure alignment with user needs.
- Support feature planning, development, and validation.

## Hard Rules
- DO use `User Story` format for requirements.
- DO use `Acceptance Criteria` for validation.
- DO use `Edge Cases` for boundary conditions.
- DO use `Non-Goals` for scope clarity.
- DO NOT use `I want` without a user need.
- DO NOT use `This should do X` without a user context.
- DO NOT use `Let’s add Y` without a user benefit.
- DO NOT use `We need Z` without a user impact.
- DO NOT use `This is a feature` without a user story.
- DO NOT use `This is a bug` without a user scenario.

## Defaults
- Naming: Use `snake_case` for file names.
- Formatting: Use 2 spaces after sentence-ending punctuation.
- Error handling: Use `alt` text for images; validate links.
- Testing: Use `Google Search Console` or `Screaming Frog` for validation.

## Patterns We Prefer
- Use `User Story` format:
  ```md
  As a user, I want to log in so I can access my account.
  ```
- Use `Acceptance Criteria` for validation:
  ```md
  - Given I am on the login page
  - When I enter my email and password
  - Then I should see a "Login successful" message
  ```
- Use `Edge Cases` for boundary conditions:
  ```md
  - Edge Case: User enters invalid email format.
  - Expected: Show error "Invalid email format".
  ```
- Use `Non-Goals` for scope clarity:
  ```md
  - Non-Goals: This feature does not support multi-factor authentication.
  ```

## Footguns to Avoid
- Avoid `I want` without a user need.
- Avoid `This should do X` without a user context.
- Avoid `Let’s add Y` without a user benefit.
- Avoid `We need Z` without a user impact.

## Definition of Done
- [ ] File exists at `docs/identities/product-spec.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
