# project-init

`project-init` packages a document-backed handoff loop for repositories that need AI agents to resume work from files instead of chat history.

It installs as an agent skill and provides templates for:

- one stable agent entry point: `AGENTS.md`
- project purpose and boundaries: `Project.md`
- user quickstart: `README.md`
- operations: `docs/runbook.md`
- acceptance contracts: `docs/contracts/*`
- task handoff state: `.github/TaskLogs/*`
- hard prompt chain: `.github/prompts/*`
- deterministic validation: `.github/project_handoff_contract.json` plus `scripts/validate_handoff.py`

## Waza Think Invocation

Use `waza think project-init` as package-level invocation language for agents, not as a shell command or runtime dependency.

Example user prompts:

```text
waza think project-init for this repo
Use project-init to add an agent handoff loop
Refresh this repo's project-init docs and validation contract
```

When invoked, the agent should inspect the target repo, copy only needed templates, adapt placeholders to real project facts, preserve useful existing docs, and run validation before handoff.

## Install

From this repository:

```bash
./install.sh all      # install to Codex and Claude default homes
./install.sh codex    # install to $CODEX_HOME or ~/.codex
./install.sh claude   # install to $CLAUDE_HOME or ~/.claude
```

For isolated or Windows/WSL installs, export homes before running the installer in a Git Bash/POSIX shell:

```bash
export CODEX_HOME="/tmp/Codex Home With Spaces"
export CLAUDE_HOME="/tmp/ClaudeHome"
./install.sh all
```

The installer writes only under each selected agent home at `skills/project-init/`. Inside that skill directory it replaces `SKILL.md`, `templates/`, and `scripts/`; it does not modify generated project repositories.

Reload the target agent runtime after install.

## Smoke Validation

Validate this package's templates from the repository root:

```bash
python scripts/validate_handoff.py --root templates --contract templates/.github/project_handoff_contract.json --json
```

A passing run exits `0` and prints an empty JSON array:

```json
[]
```

To smoke-test installation without touching real agent homes, use scratch homes outside this repository, then validate the installed template copy:

```bash
SCRATCH="$(mktemp -d)"
export CODEX_HOME="$SCRATCH/Codex Home With Spaces"
export CLAUDE_HOME="$SCRATCH/ClaudeHome"
PYTHON="${PYTHON:-}"
if [ -z "$PYTHON" ]; then
  for CANDIDATE in python3 python py; do
    if command -v "$CANDIDATE" >/dev/null 2>&1 && "$CANDIDATE" --version >/dev/null 2>&1; then
      PYTHON="$CANDIDATE"
      break
    fi
  done
fi
[ -n "$PYTHON" ] || { echo "Python 3 is required" >&2; exit 1; }
./install.sh all
"$PYTHON" "$CODEX_HOME/skills/project-init/scripts/validate_handoff.py" \
  --root "$CODEX_HOME/skills/project-init/templates" \
  --contract "$CODEX_HOME/skills/project-init/templates/.github/project_handoff_contract.json" \
  --json
```

## Generated Project Validation

After using the templates in a target repository, run validation from that generated project root:

```bash
python scripts/validate_handoff.py --root . --contract .github/project_handoff_contract.json
```

For a generated project, fix any reported missing files, heading drift, placeholder remnants, wrapper drift, or secret-pattern findings before handing off.

## Template Use

Use the default scaffold for most repositories:

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
.github/prompts/*
.github/TaskLogs/*
```

Optional wrappers such as `CLAUDE.md`, `CODEX.md`, `.github/copilot-instructions.md`, CI, or pre-commit config should be added only when that surface is requested or already used.

## Safety Notes

- Treat templates as starting points; replace placeholders with project-specific facts before validation and handoff.
- Keep `AGENTS.md` as the stable entry point. Tool-specific wrappers should point back to it instead of duplicating rules.
- Validation checks structural drift and obvious secrets/placeholders; it does not prove domain correctness.
- Review `git diff` before ending work and do not commit unless the user explicitly asks.
