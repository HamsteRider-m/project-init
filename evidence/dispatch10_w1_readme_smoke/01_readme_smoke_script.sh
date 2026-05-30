#!/usr/bin/env bash
set -euo pipefail
SCRATCH="$(mktemp -d)"
echo "SCRATCH=$SCRATCH"
export CODEX_HOME="$SCRATCH/Codex Home With Spaces"
export CLAUDE_HOME="$SCRATCH/ClaudeHome"
PYTHON="${PYTHON:-python3}"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON="python"
echo "PYTHON=$PYTHON"
echo "CODEX_HOME=$CODEX_HOME"
echo "CLAUDE_HOME=$CLAUDE_HOME"
./install.sh all
"$PYTHON" "$CODEX_HOME/skills/project-init/scripts/validate_handoff.py"   --root "$CODEX_HOME/skills/project-init/templates"   --contract "$CODEX_HOME/skills/project-init/templates/.github/project_handoff_contract.json"   --json
