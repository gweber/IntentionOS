#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"

echo "--- health (${API_URL}) ---"
curl -fsS "${API_URL}/health" | python -m json.tool

echo "--- create demo job ---"
JOB_ID=$(curl -fsS -X POST "${API_URL}/jobs" \
  -H 'content-type: application/json' \
  --data-binary @- <<'JSON' \
  | python -c 'import sys, json; print(json.load(sys.stdin)["id"])'
{
  "kind": "demo",
  "input": {"topic": "smoke"}
}
JSON
)

echo "job_id=${JOB_ID}"

echo "--- job detail ---"
curl -fsS "${API_URL}/jobs/${JOB_ID}" | python -m json.tool | head -n 60

echo "--- SSE sample (first 25 lines) ---"
# Note: `head` closes the pipe early, which can make curl exit non-zero with
# "Failure writing output". That's expected; we ignore that exit code.
set +e
curl -fsSN "${API_URL}/jobs/${JOB_ID}/events" 2>/dev/null | head -n 25
set -e
