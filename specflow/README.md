# Specflow

Specflow is the project workflow for turning an idea into reviewed, verifiable
software. Work moves through five phases in order:

1. **Intent** — State the vision, goals, constraints, measurable success
   criteria, and non-goals. Keep observed current behavior separate from
   desired behavior.
2. **Roadmap** — Break the intent into three to five ordered phases. Give each
   phase a goal, deliverables, dependencies, and status.
3. **Tasks** — Break each phase into atomic tasks. Every task names its owner
   (human or AI), inputs, expected output, dependencies, and verification.
4. **Execute** — Work only on approved tasks. Use the repository's
   `agents.md` TDD gates for code changes. Record decisions, changed files,
   commands, and actual verification results in the proposal.
5. **Refine** — Compare results to the original intent and acceptance criteria.
   Record gaps and decisions, update affected phases/tasks, and return to the
   appropriate earlier phase when scope changes.

## How to use the flow

1. Copy [proposal-template.md](./proposal-template.md) to
   `proposals/NNN-short-name.md`.
2. Complete Intent, Roadmap, and Tasks. Label assumptions and distinguish
   existing behavior from desired behavior.
3. Review the proposal with the product owner. Do not execute proposed work
   until its scope and acceptance criteria are approved.
4. During Execute, update task status and append evidence; do not replace
   expected verification with an unrun command or claim.
5. Complete Refine after execution. If criteria fail, record the gap and create
   follow-up tasks; if the intent changes, revise the proposal and seek approval
   again.

## Status values

- Proposal: drafted and awaiting review; not authorization to implement new
  scope.
- Approved: intent and acceptance criteria have been accepted.
- In progress: approved tasks are being executed.
- Refined: execution was evaluated and follow-up decisions are recorded.
- Complete: acceptance criteria passed, evidence is recorded, and remaining
  gaps are either resolved or explicitly deferred.

Proposal documents are the source of truth for scope and decisions. Keep
completed proposals as history; create a new numbered proposal for independent
features rather than silently changing the meaning of an approved one.

## First proposal

[001 — Product catalog API baseline](./proposals/001-product-catalog.md)
documents the current product creation and listing implementation. It records
what exists today as the baseline and explicitly marks unimplemented or
unverified behavior as gaps, not as shipped requirements.
