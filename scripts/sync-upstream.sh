#!/usr/bin/env bash
#
# sync-upstream.sh: Synchronize local & cloud fork with upstream main repository
#

set -e

echo "🔄 Fetching latest updates from upstream (Alishahryar1/free-claude-code)..."
git fetch upstream main

echo "🔀 Merging upstream/main into local main..."
git merge upstream/main -m "chore: sync with upstream main release"

echo "📦 Syncing uv dependencies..."
if command -v uv >/dev/null 2>&1; then
    uv sync
fi

echo "🚀 Pushing updated release to origin (sachin7x/free-claude-code-proxy)..."
git push origin main

echo "✅ Upstream synchronization complete!"
