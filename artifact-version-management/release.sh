#!/bin/bash
set -euo pipefail

release_type="${1:-}"
release_notes="${2:-Release update}"

if [ -z "$release_type" ]; then
    echo "Usage: $0 {major|minor|patch} 'release notes'"
    exit 1
fi

echo "=== Starting Release Process ==="

if ! git diff-index --quiet HEAD --; then
    echo "Error: Working directory has uncommitted changes"
    git status --short
    exit 1
fi

./version-manager.sh bump "$release_type"
new_version=$(./version-manager.sh get)

./version-manager.sh changelog "$release_notes"

git add VERSION CHANGELOG.md src/app.sh
git commit -m "Bump version to $new_version"

./build.sh

git add builds/ metadata/
git commit -m "Add build artifacts for version $new_version"

echo ""
echo "=== Release Complete ==="
echo "Version: $new_version"
echo "Tag: v$new_version"
