#!/usr/bin/env bash
set -euo pipefail
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

case "$1" in
  validate) validate_target "$2" ;;
  safe) is_safe_skill_target "$2" ;;
  walk)
    path="$2"
    seen=0
    while [ "$path" != "/" ] && [ "$path" != "." ]; do
      printf '%s\n' "$path"
      seen=$((seen+1))
      [ "$seen" -lt 20 ] || { echo "walk exceeded limit" >&2; exit 9; }
      parent="$(dirname "$path")"
      [ "$parent" != "$path" ] || break
      path="$parent"
    done
    printf '%s\n' "$path"
    ;;
  *) echo "bad harness mode" >&2; exit 2 ;;
esac
