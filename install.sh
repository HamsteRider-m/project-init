#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-${HOME}/.codex}"
CLAUDE_HOME="${CLAUDE_HOME:-${HOME}/.claude}"

usage() {
  cat <<EOF
Usage: $0 [all|codex|claude]

Installs project-init to agent skill homes:
  codex   $CODEX_HOME/skills/project-init
  claude  $CLAUDE_HOME/skills/project-init
  all     both targets (default)

Environment overrides:
  CODEX_HOME   default: $HOME/.codex
  CLAUDE_HOME  default: $HOME/.claude

Safety note: install overwrites SKILL.md, templates/, and scripts/ inside
only the target project-init skill directory shown above.
EOF
}

is_safe_skill_target() {
  local target="$1"
  case "$target" in
    /*/skills/project-init|[A-Za-z]:/*/skills/project-init) return 0 ;;
    *) return 1 ;;
  esac
}

validate_target() {
  local target="$1"
  if ! is_safe_skill_target "$target"; then
    echo "Refusing unsafe install target: $target" >&2
    echo "Expected absolute target path to end with /skills/project-init." >&2
    exit 3
  fi

  local path="$target"
  local parent
  while [ "$path" != "/" ] && [ "$path" != "." ]; do
    if [ -L "$path" ]; then
      echo "Refusing unsafe install target containing symlink: $path" >&2
      exit 3
    fi
    parent="$(dirname "$path")"
    [ "$parent" != "$path" ] || break
    path="$parent"
  done
}

install_skill() {
  local target="$1"
  validate_target "$target"
  echo "Installing project-init to: $target"
  echo "Overwrite scope: $target/SKILL.md, $target/templates/, $target/scripts/"
  mkdir -p "$target"
  rm -f "$target/SKILL.md"
  cp "$SCRIPT_DIR/SKILL.md" "$target/SKILL.md"
  rm -rf "$target/templates"
  cp -R "$SCRIPT_DIR/templates" "$target/templates"
  rm -rf "$target/scripts"
  cp -R "$SCRIPT_DIR/scripts" "$target/scripts"
  echo "Installed project-init to $target"
}

case "${1:-all}" in
  all)
    usage
    install_skill "$CODEX_HOME/skills/project-init"
    install_skill "$CLAUDE_HOME/skills/project-init"
    ;;
  codex)
    usage
    install_skill "$CODEX_HOME/skills/project-init"
    ;;
  claude)
    usage
    install_skill "$CLAUDE_HOME/skills/project-init"
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

echo "Reload the target agent runtime to activate project-init."
