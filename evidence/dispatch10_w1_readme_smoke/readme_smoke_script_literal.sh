set -euo pipefail
SCRATCH="$(mktemp -d)"
export CODEX_HOME="$SCRATCH/Codex Home With Spaces"
export CLAUDE_HOME="$SCRATCH/ClaudeHome"
PYTHON="${PYTHON:-python3}"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON="python"
./install.sh all
"$PYTHON" "$CODEX_HOME/skills/project-init/scripts/validate_handoff.py"   --root "$CODEX_HOME/skills/project-init/templates"   --contract "$CODEX_HOME/skills/project-init/templates/.github/project_handoff_contract.json"   --json
printf '
PYTHON_USED=%s
' "$PYTHON"
printf 'CODEX_HOME=%s
' "$CODEX_HOME"
printf 'CLAUDE_HOME=%s
' "$CLAUDE_HOME"
