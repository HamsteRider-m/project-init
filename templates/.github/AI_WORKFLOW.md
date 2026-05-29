# AI Workflow

This repo uses document-backed task state. The documents should make work resumable without turning the repo into a process exercise.

TaskLogs record active task state and evidence. They must not replace `Project.md`, `docs/runbook.md`, or `docs/contracts/*` as stable project rules.

## Modes

| Mode | Use When | Primary File |
|---|---|---|
| `plan` | defining scope, risks, or a next run | `TaskLogs/Planning.md` |
| `execute` | changing code, data, outputs, or docs | `TaskLogs/Execution.md` |
| `verify` | checking acceptance criteria and evidence | `TaskLogs/Execution.md` |
| `review` | judging output quality or implementation risk | `TaskLogs/Review.md` |
| `investigate` | debugging failures or unexpected behavior | `TaskLogs/Investigate.md` |
| `kb` | capturing durable procedures or decisions | `TaskLogs/KB.md` |

## Gates

### Verification Gate

Before claiming completion, record evidence in `TaskLogs/Execution.md`. Evidence should be command output, generated file paths, counts, or concise review notes tied to actual files.

### Privacy Gate

Do not move private data, credentials, tokens, or local-only material outside the workspace unless the user explicitly asks.

### End-Of-Task Documentation Audit

Before claiming a task complete, check whether the change altered any stable rule, operation, acceptance gate, evidence trail, or residual risk.

Record the audit result in `TaskLogs/Execution.md`:

- `Project.md`: updated / unchanged, with reason.
- `README.md`: updated / unchanged, with reason.
- `docs/runbook.md`: updated / unchanged, with reason.
- `docs/contracts/*`: updated / unchanged, with reason.
- `TaskLogs`: updated / unchanged, with evidence location.

If a document should change but the task cannot safely update it, record that as document debt in `TaskLogs/Review.md`.

## Durable State Files

| File | Purpose |
|---|---|
| `TaskLogs/CurrentTask.md` | active task and acceptance criteria |
| `TaskLogs/Planning.md` | open plan and locked decisions |
| `TaskLogs/Execution.md` | commands, evidence, blockers |
| `TaskLogs/Review.md` | output or code review findings |
| `TaskLogs/Investigate.md` | debugging notes and root-cause evidence |
| `TaskLogs/KB.md` | optional durable findings worth retaining |

## Maintenance Rules

| File | Update When | Keep Out |
|---|---|---|
| `Project.md` | stable rules, boundaries, production path, non-goals change | temporary task status |
| `README.md` | quickstart, common commands, or documentation map changes | long debugging history |
| `docs/runbook.md` | routine commands, prerequisites, or failure handling change | acceptance policy |
| `docs/contracts/*` | pass/fail criteria, output boundaries, or review gates change | command logs |
| `TaskLogs/CurrentTask.md` | active task scope or acceptance criteria changes | historical evidence |
| `TaskLogs/Planning.md` | open plan or locked decisions change | completed command logs |
| `TaskLogs/Execution.md` | commands run, generated artifacts, blockers, or doc-audit result change | stable project rules |
| `TaskLogs/Investigate.md` | root cause, downgraded path, or recovery evidence changes | routine operation |
| `TaskLogs/Review.md` | findings, residual risks, test gaps, or document debt change | source-of-truth contracts |
| `TaskLogs/KB.md` | optional durable lesson should be retained | mandatory reading path |
