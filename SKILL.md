---
name: project-init
description: Initialize a new project with full AI harness and guardrails: CLAUDE.md/AGENTS.md AI entry points, 7-mode workflow task logs, CI workflow, pre-commit hooks, and linter config. Use when user says "初始化项目", "搭建项目骨架", "init project", "project init", or /project-init.
---

# project-init

Scaffold a complete AI-constrained project harness from scratch. Run this at the start of every new project.

## What this skill creates

```
<project-root>/
├── CLAUDE.md                          # Claude entry point
├── AGENTS.md                          # Generic agent entry point
├── CODEX.md                           # Codex entry point
├── Project.md                         # Project purpose & scope (fill in)
├── .github/
│   ├── copilot-instructions.md        # 7-mode AI workflow definition
│   ├── KnowledgeBase/Index.md         # KB index
│   ├── TaskLogs/
│   │   ├── CurrentTask.md
│   │   ├── Planning.md
│   │   ├── Scrum.md
│   │   ├── Execution.md
│   │   ├── Review.md
│   │   ├── Investigate.md
│   │   └── KB.md
│   └── workflows/
│       └── ci.yml
├── .pre-commit-config.yaml
└── pyproject.toml                     # ruff + mypy config appended (Python only)
```

## Steps

### 1. Detect project type

```bash
# Check for existing language markers
ls pyproject.toml package.json Cargo.toml go.mod 2>/dev/null
```

Set `LANG` to `python`, `node`, or `unknown`.

### 2. Create AI entry point files

Create **CLAUDE.md**:

```markdown
# Claude Entry

Follow the same repo contract as every other AI tool:

1. read [Project.md](./Project.md)
2. read [.github/copilot-instructions.md](./.github/copilot-instructions.md)
3. read [.github/TaskLogs/CurrentTask.md](./.github/TaskLogs/CurrentTask.md)
4. read [.github/TaskLogs/Planning.md](./.github/TaskLogs/Planning.md)
5. read [.github/TaskLogs/Execution.md](./.github/TaskLogs/Execution.md)
6. read [.github/TaskLogs/Review.md](./.github/TaskLogs/Review.md)

Use repository documents as the source of truth for current task state, not prior chat messages alone.

Consult `.github/KnowledgeBase/Index.md` and the relevant files in `docs/` before design or implementation decisions.

Use `.github/TaskLogs/Scrum.md` for backlog or scope work.
Use `.github/TaskLogs/Investigate.md` for debugging investigations.
```

Create **AGENTS.md** and **CODEX.md** with identical content to CLAUDE.md.

### 3. Create Project.md

```markdown
# Project

## Purpose

<!-- One paragraph: what this system does and why it exists -->

## Key Terms

<!-- Define domain-specific terms used throughout the codebase -->

## Phase 0 — MVP

- [ ] <!-- first deliverable -->

## Non-Goals (v1)

- <!-- explicitly out of scope -->
```

### 4. Create .github/copilot-instructions.md

```markdown
# AI Workflow

This repo uses a 7-mode request protocol. Always identify the mode before acting.

## Modes

| Mode | Trigger | Output |
|---|---|---|
| `scrum` | backlog grooming, scope decisions | updated Scrum.md |
| `plan` | new task or feature design | updated Planning.md + CurrentTask.md |
| `execute` | implement a planned task | code changes + updated Execution.md |
| `verify` | check acceptance criteria | evidence recorded in Execution.md |
| `review` | post-implementation quality gate | Review.md with scores |
| `investigate` | debug a failure or unexpected behavior | Investigate.md with root cause |
| `kb` | capture a reusable decision or finding | KB.md + KnowledgeBase/Index.md |

## Durable State Files

| File | Purpose |
|---|---|
| `CurrentTask.md` | active task: title, scope, acceptance criteria |
| `Planning.md` | step-by-step plan with status |
| `Scrum.md` | backlog |
| `Execution.md` | run log, evidence, blockers |
| `Review.md` | review scores and findings |
| `Investigate.md` | debug investigations |
| `KB.md` | knowledge base entries |

## Gates

**Implementation gate**: a task entry in CurrentTask.md AND a plan in Planning.md must exist before writing code.

**Verification gate**: acceptance criteria evidence must be recorded in Execution.md before claiming completion. Evidence = actual command output, not assertions.
```

### 5. Create TaskLog skeleton files

Create each file under `.github/TaskLogs/`:

**CurrentTask.md**:
```markdown
# Current Task

## Title

<!-- task name -->

## Mode

plan

## Why

<!-- motivation -->

## In Scope

- 

## Out of Scope

- 

## Acceptance Criteria

- 
```

**Planning.md**:
```markdown
# Planning

## Steps

- [ ] 1. 
- [ ] 2. 

## Locked Decisions

- 
```

**Scrum.md**:
```markdown
# Backlog

## In Progress

- [ ] 

## Todo

- [ ] 

## Done

- [x] project initialized
```

**Execution.md**, **Review.md**, **Investigate.md**, **KB.md**: create as empty files with a `# <Title>` heading only.

**KnowledgeBase/Index.md**:
```markdown
# Knowledge Base Index

| Topic | File | Summary |
|---|---|---|
```

### 6. Create CI workflow

Create `.github/workflows/ci.yml`. Adapt to detected language:

**Python**:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --extra dev
      - run: uv run ruff check src/ tests/
      - run: uv run pytest -q
```

**Node**:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test
```

**Unknown**: create the Python template with a comment `# TODO: adapt to project language`.

### 7. Create .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

For non-Python projects, omit the ruff hook and keep only the generic hooks.

Then install hooks:
```bash
pre-commit install
```

### 8. Append linter config (Python only)

If `pyproject.toml` exists, append:
```toml
[tool.ruff]
target-version = "py312"
select = ["E", "F", "I"]

[tool.mypy]
strict = false
ignore_missing_imports = true
```

If `pyproject.toml` does not exist, skip silently (don't create it — that's the package manager's job).

### 9. Report

Print a summary table of what was created vs skipped, and remind the user to:
1. Fill in `Project.md` purpose section
2. Fill in `CurrentTask.md` with the first task
3. Run `pre-commit run --all-files` to verify hooks work
