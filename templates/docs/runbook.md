# Runbook

This is the routine operating manual. Stable project rules live in `Project.md`; acceptance rules live in `docs/contracts/`; execution evidence and historical investigations live in `.github/TaskLogs/`.

## Production Path

```text
input
  -> prepare
  -> process
  -> validate
  -> accepted output
```

## Preconditions

- <!-- required tools -->
- <!-- required local paths -->
- <!-- required environment variables, without secret values -->
- <!-- required source data -->

## Per-Item Procedure

1. Confirm inputs and expected parameters.
2. Prepare source material.
3. Run the production command.
4. Inspect generated work artifacts.
5. Run the first acceptance gate.
6. Generate final output only after the first gate passes.
7. Run the final acceptance gate.
8. Refresh summaries or review queues.

## Commands

```bash
# prepare
```

```bash
# process
```

```bash
python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json
```

## Failure Handling

- Missing input: stop, record the missing path/config, and ask for the source.
- Validation failure: regenerate from the failing step; do not manually patch output into apparent compliance.
- Secret or private data exposure: stop, remove the leaked value from generated files, rotate credentials if a real secret was written, and record the incident.
- Generated artifacts in final output: move them to the work/cache boundary and rerun validation.

## Acceptance Checklist

- Inputs are traceable.
- Work artifacts are stored outside final outputs.
- Required acceptance gates pass.
- `scripts/validate_handoff.py` returns exit code 0.
- Final outputs contain only allowed file types.
- Review items are recorded.
- Historical/debug paths are not treated as the current production mainline.
