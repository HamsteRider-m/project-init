# Folder Structure

This project keeps final outputs separate from engineering artifacts and historical evidence.

## Root

- `AGENTS.md`: agent entry and reading order.
- `Project.md`: stable project rules.
- `README.md`: quickstart and documentation map.
- `docs/runbook.md`: routine operation.
- `docs/contracts/`: acceptance rules.
- `.github/TaskLogs/`: task state, evidence, investigations, and review notes.

## Final Outputs

<!-- Define where accepted final outputs live and which file types are allowed. -->

Final output folders should contain human-facing deliverables only.

## Work Artifacts

<!-- Define where JSON, logs, chunks, caches, temp files, generated intermediates, and audit artifacts live. -->

Work artifacts must not be mixed into final output folders.

## Historical Or Debug Material

Historical handoffs and debug notes are evidence. They must point back to `Project.md` and `docs/runbook.md` for current rules and routine operation.
