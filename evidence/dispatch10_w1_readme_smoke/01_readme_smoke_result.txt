$ bash ./.dispatch10_w1_smoke.sh
rc=0

[script]
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


[stdout]
SCRATCH=/tmp/tmp.ESanlpgzao
PYTHON=python3
CODEX_HOME=/tmp/tmp.ESanlpgzao/Codex Home With Spaces
CLAUDE_HOME=/tmp/tmp.ESanlpgzao/ClaudeHome
Usage: ./install.sh [all|codex|claude]

Installs project-init to agent skill homes:
  codex   /tmp/tmp.ESanlpgzao/Codex Home With Spaces/skills/project-init
  claude  /tmp/tmp.ESanlpgzao/ClaudeHome/skills/project-init
  all     both targets (default)

Environment overrides:
  CODEX_HOME   default: /home/gomay/.codex
  CLAUDE_HOME  default: /home/gomay/.claude

Safety note: install overwrites SKILL.md, templates/, and scripts/ inside
only the target project-init skill directory shown above.
Installing project-init to: /tmp/tmp.ESanlpgzao/Codex Home With Spaces/skills/project-init
Overwrite scope: /tmp/tmp.ESanlpgzao/Codex Home With Spaces/skills/project-init/SKILL.md, /tmp/tmp.ESanlpgzao/Codex Home With Spaces/skills/project-init/templates/, /tmp/tmp.ESanlpgzao/Codex Home With Spaces/skills/project-init/scripts/
Installed project-init to /tmp/tmp.ESanlpgzao/Codex Home With Spaces/skills/project-init
Installing project-init to: /tmp/tmp.ESanlpgzao/ClaudeHome/skills/project-init
Overwrite scope: /tmp/tmp.ESanlpgzao/ClaudeHome/skills/project-init/SKILL.md, /tmp/tmp.ESanlpgzao/ClaudeHome/skills/project-init/templates/, /tmp/tmp.ESanlpgzao/ClaudeHome/skills/project-init/scripts/
Installed project-init to /tmp/tmp.ESanlpgzao/ClaudeHome/skills/project-init
Reload the target agent runtime to activate project-init.
[]


[stderr]
wsl: Failed to start the systemd user session for 'gomay'. See journalctl for more details.

