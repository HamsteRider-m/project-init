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

### Planning Gate

Use `.github/prompts/project-init-plan.md` before execution when scope, risk, sequencing, or acceptance criteria are unclear. Planning output belongs in `TaskLogs/Planning.md`; command evidence belongs in `TaskLogs/Execution.md`.

### Verification Gate

Before claiming completion, record evidence in `TaskLogs/Execution.md`. Evidence should be command output, generated file paths, counts, or concise review notes tied to actual files.

For documentation or handoff changes, the deterministic gate is:

```bash
python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json
```

This command must pass before the documentation loop is considered accepted. Use `.github/prompts/project-init-verify.md` to check the non-deterministic evidence and completion statement.

### Privacy Gate

Do not move private data, secrets, tokens, credentials, local model weights, customer data, or generated outputs into handoff docs unless the project contract explicitly allows it. Prefer references to local paths and redacted evidence.

## Prompt Chain

| Prompt | Required Use | Enforces |
|---|---|---|
| `.github/prompts/project-init-system.md` | before changing code, outputs, data, infrastructure, or durable docs | reading order, source-of-truth hierarchy, edit boundaries, operating loop |
| `.github/prompts/project-init-plan.md` | before multi-file, risky, ambiguous, or contract-changing work | concrete plan, locked decisions, deterministic contract alignment |
| `.github/prompts/project-init-verify.md` | before claiming completion | validation evidence, residual risk statement, blocker handling |

The prompt chain is intentionally connected to `.github/project_handoff_contract.json` and `scripts/validate_handoff.py`. If a prompt adds a deterministic requirement, update the JSON contract and validator in the same change.

## Edit Boundaries

| Category | Files | Edit When |
|---|---|---|
| Stable source | `Project.md`, `README.md`, `docs/runbook.md`, `docs/folder_structure.md`, `docs/contracts/*` | stable purpose, commands, boundaries, outputs, or acceptance gates change |
| Agent process | `AGENTS.md`, `.github/AI_WORKFLOW.md`, `.github/prompts/*`, `.github/project_handoff_contract.json`, `scripts/validate_handoff.py` | the handoff loop, validator, or prompt contract changes |
| Active task state | `.github/TaskLogs/CurrentTask.md`, `.github/TaskLogs/Planning.md`, `.github/TaskLogs/Execution.md`, `.github/TaskLogs/Review.md`, `.github/TaskLogs/Investigate.md`, `.github/TaskLogs/KB.md` | scope, plan, commands, evidence, findings, blockers, or durable lessons change |
| Wrappers | `CLAUDE.md`, `CODEX.md`, `.github/copilot-instructions.md` | a tool needs an entry shim; wrapper must point back to `AGENTS.md` |

Do not copy transient run logs into stable source files. Do not put stable acceptance rules only in TaskLogs.

## Durable State Files

| File | Purpose |
|---|---|
| `Project.md` | stable purpose, boundaries, production path, non-goals |
| `README.md` | quickstart and documentation map for humans and agents |
| `docs/runbook.md` | routine commands, prerequisites, failure handling, acceptance checklist |
| `docs/contracts/output_contract.md` | final output boundary and rejection rules |
| `docs/contracts/qc_and_review_contract.md` | required reports, hard gates, manual review triggers |
| `.github/project_handoff_contract.json` | deterministic validation contract consumed by `scripts/validate_handoff.py` |
| `.github/prompts/*` | hard prompt rules for system behavior, planning, and verification |
| `TaskLogs/CurrentTask.md` | active task scope and acceptance criteria |
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
| `.github/prompts/*` | agent operating rules, planning gate, or verification gate change | project-specific command logs |
| `.github/project_handoff_contract.json` | deterministic requirements change | prose-only preferences that cannot be validated |
| `scripts/validate_handoff.py` | JSON contract gains deterministic checks | project-specific facts better held in JSON/docs |
| `TaskLogs/CurrentTask.md` | active task scope or acceptance criteria changes | historical evidence |
| `TaskLogs/Planning.md` | open plan or locked decisions change | completed command logs |
| `TaskLogs/Execution.md` | commands run, generated artifacts, blockers, or doc-audit result change | stable project rules |
| `TaskLogs/Investigate.md` | root cause, downgraded path, or recovery evidence changes | routine operation |
| `TaskLogs/Review.md` | findings, residual risks, test gaps, or document debt change | source-of-truth contracts |
| `TaskLogs/KB.md` | optional durable lesson should be retained | mandatory reading path |
