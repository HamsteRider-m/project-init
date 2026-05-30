# Project Init Planning Prompt

Use this prompt when a task changes multiple files, changes acceptance criteria, alters generated outputs, or has unclear sequencing. The purpose is not bureaucracy; it is to make the next agent understand why the chosen path is safe.

## Planning Gate

Before execution, MUST write or refresh `.github/TaskLogs/Planning.md` with:

- `Open Plan`: concrete steps with completion criteria, not vague buckets.
- `Locked Decisions`: decisions that should not be re-litigated without new evidence.
- `Evidence Location`: where command output, generated artifacts, and review notes will be recorded.

MUST ensure `.github/TaskLogs/CurrentTask.md` contains the active task, acceptance criteria, and any explicit user constraints.

## Scope Discipline

MUST map each planned change to one managed-file category from `.github/prompts/project-init-system.md`. If a file does not fit a category, pause and either justify it in `.github/TaskLogs/Planning.md` or ask for clarification.

MUST NOT use broad instructions such as "update all docs" or "fix everything" as a plan step. Expand them into named files or named contracts. MUST NOT mix stable project facts and transient run logs in the same document.

## Contract Alignment

Before editing, MUST inspect `.github/project_handoff_contract.json` and identify which contract keys will enforce the change. If a requirement can be deterministic, prefer adding or tightening JSON plus `scripts/validate_handoff.py` over relying on prose alone.

Examples of deterministic requirements:

- Required files and headings
- Prompt cross-references and required terms
- Wrapper files pointing back to `AGENTS.md`
- Required documentation audit fields
- Managed-file category overlap errors
- Workflow mode transitions
- Secret patterns and forbidden placeholders

## Execution Handoff

When leaving planning mode, MUST leave a plan that another no-context agent can execute without chat history. The plan must name the files to edit, the validator command to run, and the expected evidence location.
