---
name: project-init
description: "Initialize or refresh a project with a document-backed AI handoff loop: AGENTS.md, Project.md, README.md, docs/runbook.md, docs/contracts/*, and .github/TaskLogs/*. Use when the user asks to waza think project-init, 初始化项目, 搭建项目骨架, init project, project init, create project docs, update project-init docs, or make a repo easier for no-context agents to resume."
---

# project-init

Create a tool-neutral project documentation harness that lets a no-context agent resume work from repository documents instead of chat history.

`waza think project-init` is package-level invocation language for this skill. Treat it as the phrase a user or agent can say to request the project-init workflow, not as a shell command, binary, or runtime dependency.

Example prompts:

```text
waza think project-init for this repo
Use project-init to add an agent handoff loop
Refresh this repo's project-init docs and validation contract
```

## Default Handoff Loop

```text
AGENTS.md
  -> Project.md
  -> README.md
  -> docs/runbook.md
  -> docs/contracts/*
  -> .github/TaskLogs/*
```

Use one stable entry point by default: `AGENTS.md`. Tool-specific files such as `CLAUDE.md`, `CODEX.md`, or `.github/copilot-instructions.md` are optional wrappers that point back to `AGENTS.md`; they must not become independent sources of truth.

## What To Create

Default scaffold:

```text
<project-root>/
├── AGENTS.md
├── Project.md
├── README.md
├── docs/
│   ├── runbook.md
│   ├── folder_structure.md
│   └── contracts/
│       ├── output_contract.md
│       └── qc_and_review_contract.md
├── scripts/
│   └── validate_handoff.py
└── .github/
    ├── project_handoff_contract.json
    ├── AI_WORKFLOW.md
    └── TaskLogs/
        ├── CurrentTask.md
        ├── Planning.md
        ├── Execution.md
        ├── Review.md
        ├── Investigate.md
        └── KB.md
```

Optional scaffold:

```text
CLAUDE.md
CODEX.md
.github/copilot-instructions.md
.github/workflows/ci.yml
.pre-commit-config.yaml
```

Only add optional files when the user asks for that tool surface or the project already uses it.

## Workflow

1. Confirm the project root with `pwd` or `git rev-parse --show-toplevel`.
2. Inspect existing docs before writing:
   - `AGENTS.md`, `Project.md`, `README.md`
   - `docs/`
   - `.github/AI_WORKFLOW.md`
   - `.github/TaskLogs/`
   - tool-specific entry files if present
3. If the directory is not a git repository and the user is initializing a durable project, run `git init` before edits.
4. Copy templates from `templates/` and adapt placeholders to the project. Preserve useful existing content; do not overwrite user edits blindly.
5. Keep responsibilities separated:
   - `Project.md`: stable purpose, boundaries, production path, non-goals, quality principles.
   - `README.md`: quickstart and documentation map.
   - `docs/runbook.md`: routine commands and failure handling.
   - `docs/contracts/*`: acceptance rules, not operations.
   - `.github/TaskLogs/*`: current state, plans, evidence, investigations, and review notes.
6. Add tool-specific wrappers only if requested. A wrapper should say to read `AGENTS.md`, not duplicate the workflow.
7. Before ending the task, run the documentation audit:
   - Did `Project.md` gain or lose a stable rule, boundary, production path, or non-goal?
   - Did `README.md` still point to the right quickstart and documentation map?
   - Did `docs/runbook.md` need new or changed routine commands, failure handling, or prerequisites?
   - Did `docs/contracts/*` need acceptance criteria updates?
   - Did `.github/TaskLogs/Execution.md` record verification evidence and the audit result?
   - Did `.github/TaskLogs/Investigate.md` or `Review.md` need evidence or residual-risk updates?
8. Run validation:
   - `python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json`
   - `git diff --check`
   - a secret scan appropriate for the project, at minimum common token prefixes/patterns mentioned in docs.
9. Report created/updated/skipped files, verification commands, documentation-audit outcome, and any remaining manual fill-ins.

## Complete Loop Recipe

When a user invokes `waza think project-init`, complete the loop end to end:

1. Identify the target project root and inspect existing handoff docs before copying templates.
2. Copy only the needed scaffold files from `templates/`; merge with existing content instead of replacing project-specific facts.
3. Replace placeholders with real project purpose, boundaries, commands, contracts, and current task state.
4. Keep `AGENTS.md` as the stable entry point; add optional wrappers only when the project asks for those tool surfaces.
5. Run generated-project validation from the target root:
   - `python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json`
6. Run `git diff --check` and a basic secret-pattern scan before handoff.
7. Report changed files, exact verification commands and exit codes, audit outcome, and any manual fill-ins that remain.

## Migration Rules For Existing Repos

- Do not delete historical handoff or investigation docs. Add a clear header that marks them historical/debug-only and points to the current Project/runbook/contracts.
- If multiple files describe the same "current" pipeline, move the complete operational procedure into `docs/runbook.md`, keep stable rules in `Project.md`, and leave evidence in TaskLogs.
- Do not put current task status in `Project.md` unless the project explicitly wants a short pointer section.
- Do not let TaskLogs become stable project rules.
- Do not add CI, pre-commit, package manager files, or language-specific config unless the project type is clear and the user wants those surfaces.

## Maintenance Rules

| File | Maintain When | Do Not Use For |
|---|---|---|
| `AGENTS.md` | reading order or agent-wide repository rule changes | task status, detailed operations |
| `Project.md` | stable purpose, boundaries, mainline, quality principles, non-goals | run logs, temporary status |
| `README.md` | quickstart, common commands, documentation map | long handoff/debug history |
| `docs/runbook.md` | routine procedure, prerequisites, commands, failure handling | acceptance policy or current task status |
| `docs/contracts/*` | pass/fail criteria, output boundaries, review gates | step-by-step operating instructions |
| `.github/AI_WORKFLOW.md` | task-state workflow and end-of-task audit rules | project-specific production rules |
| `.github/TaskLogs/CurrentTask.md` | active task scope and acceptance criteria | stable project rules |
| `.github/TaskLogs/Planning.md` | unfinished plan and locked decisions | completed run evidence |
| `.github/TaskLogs/Execution.md` | command evidence, generated paths, blockers, audit result | project constitution |
| `.github/TaskLogs/Investigate.md` | root-cause evidence and downgraded-path rationale | routine operation |
| `.github/TaskLogs/Review.md` | review findings and residual risks | stable acceptance contracts |
| `.github/TaskLogs/KB.md` | optional durable decisions or procedures | mandatory reading path |

## Template Use

Copy only the needed templates. The template folder intentionally includes optional wrapper files, but the default project should not create every wrapper.

For a new minimal project, create:

```text
AGENTS.md
Project.md
README.md
docs/runbook.md
docs/folder_structure.md
docs/contracts/output_contract.md
docs/contracts/qc_and_review_contract.md
scripts/validate_handoff.py
.github/project_handoff_contract.json
.github/AI_WORKFLOW.md
.github/TaskLogs/CurrentTask.md
.github/TaskLogs/Planning.md
.github/TaskLogs/Execution.md
.github/TaskLogs/Review.md
.github/TaskLogs/Investigate.md
.github/TaskLogs/KB.md
```

For a project with an existing workflow, merge the template structure into the existing docs instead of replacing project-specific facts.

## Deterministic Acceptance Layer

The handoff loop should not rely on an LLM saying "looks good." Generated projects should include:

- `.github/project_handoff_contract.json`: machine-readable required files, headings, reading order, wrapper rules, audit fields, forbidden placeholders, and secret patterns.
- `scripts/validate_handoff.py`: deterministic validator. It exits non-zero when the project violates the contract.
- CI or pre-commit wiring when the user wants automated enforcement.

The validator checks structure and obvious drift. It does not prove the project-specific content is correct; human/agent review still fills in meaningful domain details.

## Installing This Skill

Use the repository install script when updating local agent runtimes:

```bash
./install.sh all      # Codex + Claude default homes
./install.sh codex
./install.sh claude
```

The script installs into each selected agent home under `skills/project-init/`. Inside that skill directory it replaces `SKILL.md`, `templates/`, and `scripts/`; it does not modify generated project repositories. When calling it through WSL from Windows, pass `CODEX_HOME` or `CLAUDE_HOME` in the same `bash` invocation if you want a Windows-mounted target.

After install, reload the target agent runtime. To validate the installed copy without touching real homes, run from the repository root in Git Bash or another POSIX shell with `python` on `PATH`; export scratch `CODEX_HOME`/`CLAUDE_HOME` values before install so they persist for the following validator command:

```bash
SCRATCH="$(mktemp -d)"
export CODEX_HOME="$SCRATCH/Codex Home With Spaces"
export CLAUDE_HOME="$SCRATCH/ClaudeHome"
./install.sh all
python "$CODEX_HOME/skills/project-init/scripts/validate_handoff.py" \
  --root "$CODEX_HOME/skills/project-init/templates" \
  --contract "$CODEX_HOME/skills/project-init/templates/.github/project_handoff_contract.json" \
  --json
```
