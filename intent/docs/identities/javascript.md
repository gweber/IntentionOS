# Identity: javascript

## Purpose
- Enforce consistent, safe, and readable JavaScript code in modern environments.
- Prevent common pitfalls in dynamic typing and async handling.
- Support interoperability with TypeScript and runtime safety.

## Hard Rules
- DO use `const` or `let` for variable declarations; never use `var`.
- DO use `strict` mode in all files.
- DO use `null` or `undefined` explicitly; avoid `false` or `0` as falsy defaults.
- DO use `async/await` for all async operations; avoid `.then()` chains.
- DO not use `eval()` or `Function()` constructor.
- DO use `JSON.parse()` only on trusted input.
- DO use `Array.from()` or spread syntax instead of `Array.prototype.slice()`.
- DO NOT use `==` or `!=`; use `===` or `!==`.
- DO NOT export mutable global state.
- DO NOT use `with` statement.

## Defaults
- Naming: `camelCase` for variables, `PascalCase` for constructors.
- Formatting: Prettier with `--single-quote` and `--trailing-comma=es5`.
- Error handling: Use `try/catch` for runtime errors; avoid silent failures.
- Testing: Unit tests for pure functions; integration tests for async flows.

## Patterns We Prefer
- Use `async/await` for async control flow:
  ```js
  async function fetchUserData(id) {
      try {
          const response = await fetch(`/api/users/${id}`);
          if (!response.ok) throw new Error('Failed to fetch');
          return await response.json();
      } catch (error) {
          console.error('Fetch failed:', error);
          throw error;
      }
  }
  ```
- Use `Object.hasOwn()` instead of `hasOwnProperty`:
  ```js
  if (Object.hasOwn(obj, 'key')) {
      console.log(obj.key);
  }
  ```

## Footguns to Avoid
- Avoid `JSON.parse()` on untrusted input.
- Avoid `Array.prototype.map()` on sparse arrays.
- Avoid `setTimeout(() => {}, 0)` for microtasks.
- Avoid `==` comparisons with `null` or `undefined`.

## Definition of Done
- [ ] File exists at `docs/identities/javascript.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
