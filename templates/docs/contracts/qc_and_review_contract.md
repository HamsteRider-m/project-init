# QC And Review Contract

## Required Reports

Define the reports or checks that must exist before output is accepted.

- <!-- qc_report.md or equivalent -->
- <!-- batch_summary.md or equivalent -->
- <!-- manual_review_needed.md or equivalent -->

## Hard Gates

A hard-gate failure means the output is not accepted.

- `scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json` exits 0 for documentation handoff changes.
- The project-specific verification command exits 0 before output is accepted.

## Manual Review Triggers

Record manual review when:

- confidence is low;
- source evidence is missing;
- a fallback path was used;
- generated output contains uncertainty markers;
- validation passes with residual risk.

## Review Queue

The review queue must be concrete and actionable. Each item should point to a file, output folder, segment, command, or evidence record and state what needs confirmation.
