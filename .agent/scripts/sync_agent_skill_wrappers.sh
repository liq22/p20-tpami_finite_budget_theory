#!/usr/bin/env bash
# Regenerate the deliberately minimal Claude/Codex host entrypoints.
#
# Canonical internal modules remain under .agent/skills. The generator exposes
# only 00-router and explicit grill-me, then removes stale wrappers when clean.
#
# Usage:
#   bash .agent/scripts/sync_agent_skill_wrappers.sh [REPO_ROOT] [both|claude|codex] [--clean]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REPO_ROOT="${1:-$DEFAULT_REPO_ROOT}"
TARGET="${2:-both}"
CLEAN_FLAG=""
if [[ "${3:-}" == "--clean" || "${CLEAN_ENV:-1}" == "1" ]]; then
  CLEAN_FLAG="--clean"
fi

python "$SCRIPT_DIR/generate_agent_skill_wrappers.py" \
  --repo-root "$REPO_ROOT" \
  --source-dir ".agent/skills" \
  --target "$TARGET" \
  $CLEAN_FLAG

echo
echo "Done. Canonical internal skills: $REPO_ROOT/.agent/skills"
echo "Host-visible allowlist: 00-router, grill-me"
if [ "$TARGET" = "both" ] || [ "$TARGET" = "claude" ]; then
  echo "  Claude entrypoints: $REPO_ROOT/.claude/skills"
fi
if [ "$TARGET" = "both" ] || [ "$TARGET" = "codex" ]; then
  echo "  Codex entrypoints:  $REPO_ROOT/.codex/skills"
fi
echo "Restart Claude Code / Codex to pick up wrapper changes."
