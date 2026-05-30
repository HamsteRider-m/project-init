# Agent Entry

This repository uses document-backed project state. Use repository documents and local evidence as the source of truth; do not rely on prior chat history alone.

Before changing code, outputs, data, infrastructure, or batch jobs, read in this order:

1. `Project.md`
2. `README.md`
3. `docs/runbook.md`
4. The relevant contracts under `docs/contracts/`
5. `.github/AI_WORKFLOW.md`
6. `.github/prompts/project-init-system.md`
7. `.github/prompts/project-init-plan.md` when scope, risk, or sequencing is unclear
8. `.github/prompts/project-init-verify.md` before claiming completion
9. `.github/TaskLogs/CurrentTask.md`
10. `.github/TaskLogs/Planning.md`

The prompt chain is part of the harness contract: `AGENTS.md` gives the entry path, `.github/prompts/project-init-system.md` defines hard operating rules, `.github/prompts/project-init-plan.md` controls planning, `.github/prompts/project-init-verify.md` controls completion claims, `.github/project_handoff_contract.json` declares deterministic requirements, and `scripts/validate_handoff.py` enforces them.

Historical handoffs, debug notes, and investigations are supporting evidence only. Do not treat them as the current source of truth unless `Project.md` or `docs/runbook.md` says so.

If this directory is not a git repository and the user is initializing a durable project, initialize git before making project changes.

Tool-specific entry files, when present, are wrappers around this file. Keep the project workflow neutral and tool-agnostic unless the repository explicitly requires otherwise.
