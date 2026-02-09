# prompt 1
**The purpose of this document is to provide example prompts to drive the company.**

<task>
Bootstrap a fresh repository into an intent-driven, self-running solo-company system.

Create a minimal docs + rules structure so future agent runs automatically load constraints and workflows.

You MUST:
1) Create the file/folder structure described below.
2) Fill each file with high-quality, concise content (not placeholder lorem ipsum).
3) Keep everything generic (project-agnostic), suitable for any product/software/content venture.
4) Prefer Markdown, make it diff-friendly, and avoid tool-specific jargon unless needed.
5) Do NOT add any application code. Only docs/rules/scaffolding.

After creation, output:
- a tree of created files
- a 10-line quickstart explaining how I use the system day-to-day
</task>

<context>
Assume an empty folder.
This is a solo operator company. The system must run on “captured intent → structured execution”.
Roles are universal (Strategist, Visioneer, Architect, Breaker, Curator).
</context>

<file_structure>
/AGENTS.md
/.clinerules/core.md
/docs/company_driver.md
/docs/workflows.md
/docs/ai_roles.md
/docs/ai_constraints.md
/docs/intent_inbox.md
/docs/ops_quickstart.md
/docs/memory/decisions.md
/docs/memory/assumptions.md
/docs/memory/rejections.md
/docs/memory/glossary.md
</file_structure>

<requirements_by_file>
AGENTS.md:
- Explain the operating hierarchy: company_driver → workflows → roles → constraints → memory
- Hard rules: no DB writes in providers, no silent scope expansion, prefer small steps, always produce an artifact
- Default role if unspecified: Architect
- Include the core principle: “A conversation is an interaction to shape.”

.clinerules/core.md:
- Short, strict, execution-oriented rules.
- Enforce: select ONE workflow, activate ONE role at a time, produce at least one artifact, write decisions to memory.
- Include stop conditions (kill switch): max 3 iterations without new artifact; stop and summarize blockers.

docs/company_driver.md:
- Define triggers, default bias, what counts as “progress”, and when to stop.

docs/workflows.md:
- Provide 5–7 workflows with step sequences and role order.
- At minimum include: Idea→Execution, Friction→Fix, Drift→Realignment, Release→Ship, Learning→Codify.

docs/ai_roles.md:
- Define the 5 universal roles with perspective, focus, NOT responsible for, trigger phrase.

docs/ai_constraints.md:
- “Laws of physics” style constraints, prioritization rules, no premature optimization, no heavy refactors without intent.

docs/intent_inbox.md:
- A simple append-only format with timestamps and optional tags.
- Include a short example section.

docs/ops_quickstart.md:
- A daily 5-minute routine for a solo operator using this system.

docs/memory/*:
- Provide templates and conventions for entries (date, context, decision, consequence).
- glossary.md defines key terms like “intent”, “artifact”, “workflow”, “role”.
</requirements_by_file>

<constraints>
- Keep it generic and reusable.
- Don’t invent external tools or dependencies.
- Don’t ask me questions; make reasonable assumptions and proceed.
</constraints>


# prompt 2

<task>
Run the first operational cycle of this repository.

1) Read all governing files (AGENTS.md, .clinerules/core.md, docs/company_driver.md).
2) Initialize the system by performing a “Cold Start Alignment”.
3) Use the Drift → Realignment workflow.
4) Activate roles strictly in sequence, one at a time.
5) Produce concrete artifacts and write them to the appropriate files.

You MUST:
- Select exactly ONE workflow.
- Activate roles explicitly with their trigger phrases.
- Stop after producing durable artifacts.
- Update memory files where decisions or assumptions are made.

Do NOT:
- Add application code
- Invent projects
- Over-optimize structure
</task>

<context>
There is no project yet.
This is a fresh company system.
The goal is to establish initial direction, boundaries, and operating assumptions so future intent has somewhere to land.
</context>

<expected_artifacts>
- A short “Initial Direction” section added to docs/company_driver.md
- At least 3 explicit assumptions written to docs/memory/assumptions.md
- A concise status snapshot written to docs/memory/decisions.md
- If uncertainty remains, a clearly stated open question captured as an artifact
</expected_artifacts>

# prompt 3

<task>
Decide the first concrete output surface for this company and define what “shipped” means for it.

You MUST:
1) Select exactly ONE workflow: Decision → Commit.
2) Activate roles strictly one at a time, in sequence.
3) Produce a hard commitment, not a menu of options.
4) Write durable artifacts to memory.
5) Stop immediately after the commitment is recorded.

Do NOT:
- Start implementation
- Design systems
- Add application code
- Keep multiple options open

This is a commitment exercise, not ideation.
</task>

<context>
The system is initialized.
No product exists yet.
The goal is to choose the smallest output surface that allows real-world feedback and momentum.

Constraints:
- The output surface must be finishable by one person.
- “Shipped” must be objectively checkable.
- The definition of shipped must fit in 5 lines.
</context>

<workflow>
Decision → Commit
</workflow>

<role_sequence>
1) Strategist — decide what matters now and why
2) Visioneer — shape the value and user-facing outcome
3) Architect — sanity-check scope and define boundaries
4) Breaker — attempt to invalidate the commitment
5) Curator — record the decision and definition of shipped
</role_sequence>

<expected_artifacts>
- One committed output surface written to docs/memory/decisions.md
- A 5-line “Definition of Shipped” attached to that decision
- Any rejected alternatives recorded in docs/memory/rejections.md
</expected_artifacts>

## prompt 4

<task>
Plan the execution of Company Log — Issue #1.

You MUST:
1) Select exactly ONE workflow: execution_slice.
2) Activate exactly ONE role: Architect.
3) Convert the committed “Definition of Shipped” into a small, finite task list.
4) Each task must be concrete, checkable, and completable by one person.
5) Stop after producing the plan. No writing of the newsletter yet.

Do NOT:
- Revisit or question the decision
- Add scope
- Improve the idea
- Involve other roles
</task>

<context>
The output surface is fixed:
Public weekly “Company Log” newsletter.

The Definition of Shipped for Issue #1 is already recorded in docs/memory/decisions.md.

This step exists only to reduce ambiguity and create momentum.
</context>

<workflow>
execution_slice
</workflow>

<role>
Initialize Architect: Reduce the committed output to a minimal, executable plan.
</role>

<expected_artifacts>
- A checklist or task list written to docs/workflows.md OR a new file docs/company_log/issue_01_plan.md
- 3–7 tasks maximum
- Each task phrased as “Done when …”
</expected_artifacts>

## prompt 5

<task>
Produce Company Log — Issue #1 according to the existing execution plan.

You MUST:
1) Follow the task order defined in docs/company_log/issue_01_plan.md.
2) Activate roles sequentially and explicitly.
3) Stop immediately once the Definition of Shipped is satisfied.
4) Produce a publishable artifact (final newsletter text).

Do NOT:
- Expand scope
- Revisit decisions
- Optimize wording beyond clarity
- Add future-looking promises

This is a shipping task, not a branding exercise.
</task>

<context>
Output surface:
Public weekly “Company Log” newsletter.

Constraints:
- This is Issue #1, not a manifesto.
- Honest > impressive.
- Concrete > aspirational.
</context>

<role_sequence>
1) Initialize Visioneer: Draft the raw content focused on value and honesty.
2) Initialize Architect: Structure and tighten the draft to meet “shipped” criteria.
3) Initialize Curator: Finalize, format, and confirm shipped status.
</role_sequence>

<expected_artifacts>
- A final Issue #1 newsletter file (e.g. docs/company_log/issue_01.md)
- A short “Shipped confirmation” note appended to docs/memory/decisions.md
</expected_artifacts>
