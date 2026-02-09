# Identity: typescript

## Purpose
- Enforce strict, safe, and maintainable TypeScript codebases.
- Prevent common runtime errors via compile-time guarantees.
- Promote functional and predictable code patterns.

## Hard Rules
- DO use `strict` mode in `tsconfig.json`.
- DO use `never` for unreachable code, `unknown` instead of `any`.
- DO prefer pure functions; avoid hidden global state or side effects.
- DO use `Result<T, E>` type for error handling (e.g., `Either<T, E>` or `Result<T, E>`).
- DO not use `any` unless explicitly justified and documented.
- DO use `const` over `let` for variable declarations.
- DO name types using `PascalCase` and interfaces using `I` prefix (e.g., `IUser`, `IPost`).
- DO NOT use `var`.
- DO NOT use `eval()` or `Function()` constructor.
- DO NOT export mutable global state.

## Defaults
- Naming: `camelCase` for variables, `PascalCase` for types/interfaces.
- Formatting: Prettier with `--single-quote` and `--trailing-comma=es5`.
- Error handling: Use typed results (`Result<T, E>`) or `throw` with `Error` subclasses.
- Testing: Unit tests for pure functions; integration tests for side-effecting logic.

## Patterns We Prefer
- Use `Result<T, E>` for error handling:
  ```ts
  type Result<T, E> = { success: true; data: T } | { success: false; error: E };

  function divide(a: number, b: number): Result<number, string> {
      if (b === 0) return { success: false, error: 'Division by zero' };
      return { success: true, data: a / b };
  }
  ```
- Use `readonly` for immutable data:
  ```ts
  interface User {
      readonly id: number;
      readonly name: string;
      readonly createdAt: Date;
  }
  ```

## Footguns to Avoid
- Avoid `as any` or `as unknown` without comment.
- Avoid `Object.keys(obj).map(...)` without type guard.
- Avoid `JSON.parse()` without validation.
- Avoid `Promise.all()` on unbounded arrays.

## Definition of Done
- [x] File exists at `docs/identities/typescript.md`
- [x] Follows template exactly
- [x] Includes `Definition of Done` checklist
- [x] Uses `DO`/`DO NOT` in Hard Rules
- [x] Contains at least one code snippet
- [x] No external modifications made
- [x] All sections present and filled
- [x] No markdown linting errors
- [x] No unused or redundant lines
- [x] Matches final formatted state in search/replace
