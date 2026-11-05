#!/usr/bin/env bash
# Adapted from mattpocock/skills. See LICENSE.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
find skills -name SKILL.md -not -path '*/node_modules/*' | sort
