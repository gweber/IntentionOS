# Language Profile: php-laravel

## Purpose
- Enforce consistent Laravel application structure and development practices.
- Reduce ambiguity in controller/service layering, validation, and authorization.
- Ensure testable, maintainable, and secure PHP applications.

## Hard Rules
- DO use Form Requests for all incoming HTTP validation.
- DO keep controllers thin; move business logic to Services or Actions.
- DO use Policies and Gates for authorization; never inline logic.
- DO write reversible migrations; avoid destructive operations without explicit `--force`.
- DO not write to the database in service providers or global bootstrapping code.
- DO use `App\Models\` namespace for Eloquent models.
- DO name form requests `CreateXRequest`, `UpdateXRequest`, etc.
- DO NOT use `any` in PHP; use `mixed` or explicit types.
- DO NOT put complex logic in `routes/web.php`.
- DO NOT skip feature tests for user-facing flows.

## Defaults
- Naming: `snake_case` for files, `PascalCase` for classes.
- Formatting: PSR-12 with PHP_CodeSniffer.
- Error handling: Throw exceptions, use `try/catch` in controllers.
- Testing: Feature tests for HTTP flows; unit tests for pure logic in `tests/Unit`.

## Patterns We Prefer
- Use `FormRequest` to encapsulate validation:
  ```php
  class CreatePostRequest extends FormRequest
  {
      public function authorize(): bool
      {
          return $this->user()->can('create', Post::class);
      }

      public function rules(): array
      {
          return [
              'title' => 'required|string|max:255',
              'body' => 'required|string',
          ];
      }
  }
  ```
- Use `Action` classes for complex workflows:
  ```php
  class PublishPostAction
  {
      public function __invoke(Post $post): void
      {
          $post->update(['published_at' => now()]);
          event(new PostPublished($post));
      }
  }
  ```

## Footguns to Avoid
- Avoid `DB::transaction` without proper rollback handling.
- Avoid `->first()` on collections without checking for null.
- Avoid `->where('id', $id)` on Eloquent models without using `findOrFail`.
- Avoid `->get()` on large result sets without pagination.

## Definition of Done
- [ ] File exists at `intent/docs/language_profiles/php-laravel.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
