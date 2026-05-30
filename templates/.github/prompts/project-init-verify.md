# Project Init Verification Prompt

Use this prompt before claiming that project-init handoff work is complete. Verification is evidence-based: the validator checks deterministic rules, while the agent reviews project-specific meaning against the stable docs.

## Verification Gate

MUST run this command from the generated project root before claiming completion:

```bash
python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json
```

For this skill repository's templates, MUST run:

```bash
python scripts/validate_handoff.py --root templates --contract templates/.github/project_handoff_contract.json
```

MUST record the command and result in `.github/TaskLogs/Execution.md` for generated projects, or in the active implementation notes when validating this skill repository.

## Evidence Checklist

MUST verify all of these before handoff:

- `AGENTS.md` contains the required reading order and points to the prompt chain.
- `.github/AI_WORKFLOW.md` describes modes, gates, durable state files, maintenance rules, prompt chain, and edit boundaries.
- `.github/project_handoff_contract.json` declares required files, headings, prompt requirements, managed-file categories, workflow transitions, placeholders, audit fields, and secret patterns.
- `scripts/validate_handoff.py` passes against the intended root and contract.
- `.github/TaskLogs/Execution.md` has concrete evidence, not only placeholders.
- Stable docs and task logs do not contradict each other.

## Failure Handling

If validation fails, MUST fix the root cause or record a blocker. MUST NOT delete a requirement just to make validation pass unless the requirement is wrong for the project and the reason is recorded in `.github/TaskLogs/Planning.md` or `.github/TaskLogs/Investigate.md`.

If a command cannot run in the current environment, MUST record the exact command attempted, the error, and the manual command the next agent or human should run.

## Completion Statement

A completion statement MUST include:

- Changed files or generated artifacts
- Validation command and result
- Known residual risks or "none recorded"
- Any files intentionally left unchanged

MUST NOT say "done" based only on visual inspection or prior chat context.
