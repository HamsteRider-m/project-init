#!/usr/bin/env bash
set -e

SKILL_DIR="${HOME}/.claude/skills/project-init"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SKILL_DIR"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

echo "project-init skill installed to $SKILL_DIR"
echo "Reload Claude Code to activate."
