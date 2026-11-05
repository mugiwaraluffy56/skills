#!/usr/bin/env bash
# Adapted from mattpocock/skills. See LICENSE.
# Maintainer convenience only; use the skills CLI for supported installation.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd -P)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")
names=()
srcs=()
count=0
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names[$count]="$(basename "$src")"
  srcs[$count]="$src"
  count=$((count + 1))
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -print0)

if [ "$count" -eq 0 ]; then
  echo 'No skills found; nothing to link.'
  exit 0
fi

# Preflight all destinations before writing any links. Resolve existing ancestors
# too, so an agent directory symlink cannot redirect writes into this repository.
for DEST in "${DESTS[@]}"; do
  resolved="$(node --input-type=module - "$DEST" <<'NODE'
import { existsSync, realpathSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
let path = process.argv[2];
const suffix = [];
while (!existsSync(path)) {
  const parent = dirname(path);
  if (parent === path) throw new Error('Cannot resolve destination');
  suffix.unshift(basename(path));
  path = parent;
}
console.log(join(realpathSync(path), ...suffix));
NODE
)"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST resolves into this repository; refusing to link." >&2
      exit 1
      ;;
  esac
  for ((i=0; i<count; i++)); do
    target="$DEST/${names[$i]}"
    if [ -L "$target" ] && [ "$(readlink "$target")" = "${srcs[$i]}" ]; then
      continue
    fi
    if [ -e "$target" ] || [ -L "$target" ]; then
      echo "error: $target already exists; refusing to replace it." >&2
      exit 1
    fi
  done
done

for DEST in "${DESTS[@]}"; do
  mkdir -p "$DEST"
  for ((i=0; i<count; i++)); do
    target="$DEST/${names[$i]}"
    if [ ! -L "$target" ]; then
      ln -s "${srcs[$i]}" "$target"
    fi
    echo "linked ${names[$i]} -> ${srcs[$i]} ($DEST)"
  done
done
