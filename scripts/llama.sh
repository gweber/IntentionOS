LOCAL_MODEL="qwen3:8b" \
LOCAL_BASE_URL="http://172.20.200.169:11434/v1/" \
./scripts/company_engine.py --dry-run \
  --allow-write docs/intent_inbox.md \
  "Logge diese Idee und schlage einen Workflow vor."
