#!/usr/bin/env bash
# Install skills from this repo into an agent's skills directory (copy, no network).
# Usage: ./install.sh [--target claude|hermes|DIR] [--link] [skill ...]
#   default target: claude (~/.claude/skills); default skills: all
#   --link  symlink instead of copy (for development)
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target="$HOME/.claude/skills"; link=0; names=()

while [ $# -gt 0 ]; do
  case "$1" in
    --target)
      [ $# -ge 2 ] || { echo "--target needs a value" >&2; exit 2; }
      case "$2" in
        claude) target="$HOME/.claude/skills" ;;
        hermes) target="$HOME/.hermes/skills" ;;
        *) target="$2" ;;
      esac; shift 2 ;;
    --link) link=1; shift ;;
    -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
    *) names+=("$1"); shift ;;
  esac
done

if [ ${#names[@]} -eq 0 ]; then
  for d in "$repo"/skills/*/; do names+=("$(basename "$d")"); done
fi

mkdir -p "$target"
for n in "${names[@]}"; do
  src="$repo/skills/$n"
  [ -f "$src/SKILL.md" ] || { echo "unknown skill: $n" >&2; exit 1; }
  rm -rf "${target:?}/$n"
  if [ "$link" -eq 1 ]; then ln -s "$src" "$target/$n"; else cp -r "$src" "$target/$n"; fi
  echo "installed $n -> $target/$n"
done
