# Project

## Purpose

<!-- One paragraph: what this project does, who it is for, and why it exists. -->

## Stable Inputs And Dependencies

<!-- List source data, external systems, local paths, credentials policy, APIs, model/tool boundaries, or other stable inputs. Do not include secrets. -->

## Production Path

<!-- Describe the current mainline in one short flow. Put routine commands in docs/runbook.md, not here. -->

```text
input
  -> processing step
  -> validation
  -> accepted output
```

## Repository Boundaries

- `docs/runbook.md`: routine operation.
- `docs/contracts/`: acceptance rules.
- `.github/TaskLogs/`: active state, evidence, investigations, and review notes.

<!-- Add project-specific source/output/work/cache boundaries here. -->

## Quality Gates

<!-- Define hard gates that must pass before output is accepted. Link to docs/contracts/*. -->

## Output Standards

<!-- Define human-facing output expectations, naming rules, review rules, and uncertainty/error handling. -->

## Downgraded Or Non-Production Paths

<!-- List old approaches that may remain useful for recovery/debugging but must not be maintained as the mainline. -->

## Non-Goals

- <!-- Explicitly out of scope for the current project/version. -->

## Current State Pointers

Current task status, command evidence, and residual risks are intentionally not maintained in this file.

- Active task: `.github/TaskLogs/CurrentTask.md`
- Open plan and locked decisions: `.github/TaskLogs/Planning.md`
- Evidence and run facts: `.github/TaskLogs/Execution.md`
- Investigations: `.github/TaskLogs/Investigate.md`
- Review findings: `.github/TaskLogs/Review.md`
