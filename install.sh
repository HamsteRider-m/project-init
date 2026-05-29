#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-${HOME}/.codex}"
CLAUDE_HOME="${CLAUDE_HOME:-${HOME}/.claude}"

install_skill() {
  local target="$1"
  mkdir -p "$target"
  cp "$SCRIPT_DIR/SKILL.md" "$target/SKILL.md"
  rm -rf "$target/templates"
  cp -R "$SCRIPT_DIR/templates" "$target/templates"
  echo "Installed project-init to $target"
}

case "${1:-all}" in
  all)
    install_skill "$CODEX_HOME/skills/project-init"
    install_skill "$CLAUDE_HOME/skills/project-init"
    ;;
  codex)
    install_skill "$CODEX_HOME/skills/project-init"
    ;;
  claude)
    install_skill "$CLAUDE_HOME/skills/project-init"
    ;;
  *)
    echo "Usage: $0 [all|codex|claude]" >&2
    exit 2
    ;;
esac

echo "Reload the target agent runtime to activate project-init."
