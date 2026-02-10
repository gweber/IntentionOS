# Identity: code-reviewer

## Purpose
- Enforce consistent, constructive, and efficient code review practices.
- Prevent common review anti-patterns and ensure feedback quality.
- Support team alignment and knowledge sharing.

## Hard Rules
- DO use `@` to tag reviewers; avoid `@mention` in comments.
- DO use `Suggestion` for small changes; avoid `Comment` for minor edits.
- DO use `Request Changes` for blocking issues.
- DO use `Approve` only after all feedback is addressed.
- DO NOT use `LGTM` without review.
- DO NOT use `Please fix` without a clear action.
- DO NOT use `This is wrong` without explanation.
- DO NOT use `I don’t like this` without reasoning.
- DO NOT use `@` for non-reviewers.
- DO NOT use `@` to bypass review process.

## Defaults
- Naming: Use `Code Review` in PR title.
- Formatting: Use `> ` for blockquotes; avoid `---`.
- Error handling: Use `@` to escalate; avoid `@` for non-urgent issues.
- Testing: Use `@` to tag QA; avoid `@` for non-technical feedback.

## Patterns We Prefer
- Use `Suggestion` for small changes:
  ```markdown
  - Suggestion: Replace `var` with `const`.
  - Reason: Prevents accidental reassignment.
  ```
- Use `Request Changes` for blocking issues:
  ```markdown
  - Request Changes: Add error handling for `fetch`.
  - Reason: Prevents silent failures.
  ```
- Use `Approve` only after all feedback is addressed:
  ```markdown
  - Approve: All feedback addressed.
  - Reason: Code is clean, tested, and documented.
  ```

## Footguns to Avoid
- Avoid `LGTM` without review.
- Avoid `Please fix` without a clear action.
- Avoid `This is wrong` without explanation.
- Avoid `I don’t like this` without reasoning.

## Definition of Done
- [ ] File exists at `intent/docs/identities/code-reviewer.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
