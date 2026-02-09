# Intent Inbox (Append-Only)

This is the capture point for raw intent. Append new entries; do not rewrite history.

## Format

Each entry is one line:

```
YYYY-MM-DD HH:MM — intent statement (one sentence) #tag1 #tag2
```

Guidelines:

- Keep it concrete: “Do X so that Y is true.”
- Tags are optional; prefer a small vocabulary.
- If an intent becomes a project, leave the original entry and add a new one that links forward.

## Examples

```
2026-02-09 09:05 — Clarify what “shipped” means for the next release and create a checklist #release
2026-02-09 09:12 — Identify why onboarding feels slow and propose a minimal fix + guardrail #friction
2026-02-09 09:30 — Turn last week’s learning into a repeatable rule and add it to constraints #learning

2026-02-09 02:24 — Run Cold Start Alignment and establish initial direction, boundaries, and operating assumptions for this company system #coldstart #alignment #drift

2026-02-09 02:28 — Decide the first concrete output surface for this company and define what “shipped” means for it #decision #ship

2026-02-09 02:31 — Plan the execution of Company Log — Issue #1 as a small checklist so shipping is unambiguous #companylog #ship #planning

2026-02-09 02:40 — Draft Company Log — Issue #1 newsletter text (publishable) so it can be posted and sent for feedback #companylog #ship
```
