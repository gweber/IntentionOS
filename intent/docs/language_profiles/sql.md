# Language Profile: sql

## Purpose
- Enforce safe, performant, and maintainable SQL queries.
- Prevent common injection and performance issues.
- Ensure consistency across database operations.

## Hard Rules
- DO use explicit column lists; never use `SELECT *`.
- DO use parameterized queries; never concatenate values into SQL strings.
- DO use `EXPLAIN` to analyze query performance before production.
- DO use transactions for multi-step operations.
- DO use `LIMIT` on `UPDATE` and `DELETE` to prevent accidental mass changes.
- DO name indexes using `idx_<table>_<column>` pattern.
- DO use `IS NULL` instead of `= NULL`.
- DO NOT use `DROP TABLE` without explicit `--force` or `--confirm`.
- DO NOT use `TRUNCATE` on production tables.
- DO NOT use `UNION ALL` without a `LIMIT` in dev.

## Defaults
- Naming: `snake_case` for columns, `PascalCase` for table names.
- Formatting: Use `UPPER` for SQL keywords, `lower` for identifiers.
- Error handling: Use `BEGIN/ROLLBACK` for transaction safety.
- Testing: Use `pgTAP` or `sqlite3` test suite for schema and query validation.

## Patterns We Prefer
- Use `EXPLAIN` to validate query plan:
  ```sql
  EXPLAIN (ANALYZE, BUFFERS)
  SELECT u.name, p.title
  FROM users u
  JOIN posts p ON u.id = p.user_id
  WHERE p.created_at > '2025-01-01'
  ORDER BY p.created_at DESC
  LIMIT 10;
  ```
- Use `WITH` for complex queries:
  ```sql
  WITH user_stats AS (
      SELECT
          u.id,
          COUNT(p.id) AS post_count
      FROM users u
      LEFT JOIN posts p ON u.id = p.user_id
      GROUP BY u.id
  )
  SELECT u.name, s.post_count
  FROM users u
  JOIN user_stats s ON u.id = s.id
  WHERE s.post_count > 5;
  ```

## Footguns to Avoid
- Avoid `SELECT *` in production queries.
- Avoid `UPDATE` without `WHERE` or `LIMIT`.
- Avoid `DELETE` without `LIMIT`.
- Avoid `UNION` without `ALL` when duplicates are acceptable.

## Definition of Done
- [ ] File exists at `intent/docs/language_profiles/sql.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
