# Project Init System Prompt

This prompt is the hard operating contract for a no-context agent working in this repository. It exists to make the harness self-enforcing: `AGENTS.md` tells the agent what to read, this prompt tells the agent how to reason, `.github/project_handoff_contract.json` declares what must be true, and `scripts/validate_handoff.py` checks the deterministic parts.

## Purpose

MUST make the repository resumable from files, not chat history. The agent must leave behind enough source-of-truth documents, task state, and validation evidence that a future agent can continue safely with no prior conversation.

## Required Reading Order

Before changing code, outputs, data, infrastructure, or durable documentation, MUST read these files in order:

1. `AGENTS.md`
2. `Project.md`
3. `README.md`
4. `docs/runbook.md`
5. `docs/contracts/`
6. `.github/AI_WORKFLOW.md`
7. `.github/prompts/project-init-system.md`
8. `.github/prompts/project-init-plan.md` when scope, risk, or sequencing is unclear
9. `.github/prompts/project-init-verify.md` before claiming completion
10. `.github/TaskLogs/CurrentTask.md`
11. `.github/TaskLogs/Planning.md`

If a file is missing, MUST either create it from the project-init template with project-specific facts or record the blocker in `.github/TaskLogs/Execution.md` and stop before risky changes.

## Source Of Truth Hierarchy

MUST resolve conflicts in this order:

1. User's latest explicit instruction for the active task
2. `Project.md` stable purpose, boundaries, production path, and non-goals
3. `docs/contracts/*` pass/fail and output boundary rules
4. `docs/runbook.md` routine commands and failure handling
5. `.github/AI_WORKFLOW.md` and `.github/prompts/*` agent process rules
6. `.github/TaskLogs/*` active task state and evidence
7. Historical handoffs, issue comments, or chat logs

MUST NOT let `TaskLogs`, wrappers, old chats, or generated output override stable project rules.

## Edit Boundaries

MUST treat files as managed categories:

- Stable source files: `Project.md`, `README.md`, `docs/runbook.md`, `docs/folder_structure.md`, and `docs/contracts/*`. Edit only when stable facts, commands, boundaries, or acceptance gates change.
- Agent process files: `AGENTS.md`, `.github/AI_WORKFLOW.md`, `.github/prompts/*`, `.github/project_handoff_contract.json`, and `scripts/validate_handoff.py`. Edit only when the handoff loop itself changes.
- Active task state: `.github/TaskLogs/CurrentTask.md`, `.github/TaskLogs/Planning.md`, `.github/TaskLogs/Execution.md`, `.github/TaskLogs/Review.md`, `.github/TaskLogs/Investigate.md`, and `.github/TaskLogs/KB.md`. Update while doing work; keep transient command evidence out of stable source files.
- Wrapper files: `CLAUDE.md`, `CODEX.md`, and `.github/copilot-instructions.md`. They MUST point back to `AGENTS.md` and MUST NOT become independent rule books.

MUST NOT edit unrelated files just to satisfy process. MUST NOT erase useful human-written project facts when refreshing templates.

## Operating Loop

For every non-trivial task, MUST run this loop:

1. Classify mode using `.github/AI_WORKFLOW.md`: `plan`, `execute`, `verify`, `review`, `investigate`, or `kb`.
2. Record active scope and acceptance criteria in `.github/TaskLogs/CurrentTask.md` or `.github/TaskLogs/Planning.md` before risky edits.
3. Make the smallest useful change set that satisfies the project contracts.
4. Record commands, artifacts, changed documents, and blockers in `.github/TaskLogs/Execution.md`.
5. Run `python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json` before claiming handoff completion.
6. Use `.github/prompts/project-init-verify.md` to decide whether evidence is sufficient.

## Non-Negotiable Rules

MUST NOT claim completion without validation evidence or an explicitly recorded blocker. MUST NOT rely on memory of prior chat as proof. MUST NOT hide failed commands. MUST NOT put secrets in docs, task logs, prompts, JSON, or scripts. MUST keep project-specific content concrete; unresolved placeholders are blockers, not acceptable handoff content.
