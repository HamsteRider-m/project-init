# <!-- Project Name -->

<!-- One sentence: what this project is. -->

## What This Is

<!-- Minimal background for a new human or agent. Keep detailed rules in Project.md and operations in docs/runbook.md. -->

## Current Production Path

```text
input -> processing -> validation -> accepted output
```

See `docs/runbook.md` for routine commands.

## Required Local Inputs

- <!-- source path, config, data, model, service, or credential location; never include secret values -->

## Common Commands

```bash
python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json
```

```bash
# Replace with the most common project verification command.
```

## Documentation Map

- `AGENTS.md`: agent entry and reading order.
- `Project.md`: project rules, boundaries, production mainline, and non-goals.
- `docs/runbook.md`: routine operation and failure handling.
- `docs/contracts/*`: acceptance rules.
- `.github/AI_WORKFLOW.md`: task-state workflow.
- `.github/TaskLogs/CurrentTask.md`: active task and acceptance criteria.
- `.github/TaskLogs/Planning.md`: open plan and locked decisions.
- `.github/TaskLogs/Execution.md`: command evidence and run facts.
- `.github/TaskLogs/Investigate.md`: historical failures and debugging evidence.
- `.github/TaskLogs/Review.md`: review findings and residual risks.

## Documentation Maintenance

- Update `Project.md` when stable rules, boundaries, production path, or non-goals change.
- Update `README.md` when the quickstart, common commands, or documentation map changes.
- Update `docs/runbook.md` when routine commands, prerequisites, or failure handling change.
- Update `docs/contracts/*` when pass/fail criteria or output boundaries change.
- Update TaskLogs when active state, evidence, investigations, review findings, or document debt changes.
- At the end of each task, record a documentation audit in `.github/TaskLogs/Execution.md`.
- Run `python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json` before accepting documentation changes.

## Boundaries

- <!-- outputs boundary -->
- <!-- work/cache/generated artifact boundary -->
- <!-- credential/privacy boundary -->
