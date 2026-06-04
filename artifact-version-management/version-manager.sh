#!/bin/bash
set -euo pipefail

VERSION_FILE="VERSION"
CHANGELOG_FILE="CHANGELOG.md"

init_version() {
    if [ ! -f "$VERSION_FILE" ]; then
        echo "0.1.0" > "$VERSION_FILE"
        echo "# Changelog" > "$CHANGELOG_FILE"
        echo "" >> "$CHANGELOG_FILE"
        echo "Version initialized to 0.1.0"
    else
        echo "Version already exists: $(cat "$VERSION_FILE")"
    fi
}

get_version() {
    if [ ! -f "$VERSION_FILE" ]; then
        echo "VERSION file missing. Run: ./version-manager.sh init" >&2
        exit 1
    fi

    local version
    version=$(cat "$VERSION_FILE")

    if ! echo "$version" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "Invalid semantic version: $version" >&2
        exit 1
    fi

    echo "$version"
}

bump_version() {
    local bump_type="${1:-}"
    local current_version
    current_version=$(get_version)

    IFS='.' read -r major minor patch <<< "$current_version"

    case "$bump_type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo "Invalid bump type. Use: major, minor, or patch"
            exit 1
            ;;
    esac

    local new_version="${major}.${minor}.${patch}"
    echo "$new_version" > "$VERSION_FILE"
    sed -i "s/^VERSION=.*/VERSION=\"$new_version\"/" src/app.sh
    echo "Version bumped to $new_version"
}

update_changelog() {
    local version="$1"
    local message="${2:-No release notes provided}"
    local date
    date=$(date +%Y-%m-%d)

    local temp_file
    temp_file=$(mktemp)

    {
        echo "# Changelog"
        echo ""
        echo "## Version $version - $date"
        echo "- $message"
        echo ""
        if [ -f "$CHANGELOG_FILE" ]; then
            tail -n +2 "$CHANGELOG_FILE"
        fi
    } > "$temp_file"

    mv "$temp_file" "$CHANGELOG_FILE"
    echo "Changelog updated for version $version"
}

case "${1:-}" in
    init)
        init_version
        ;;
    get)
        get_version
        ;;
    bump)
        bump_version "${2:-}"
        ;;
    changelog)
        update_changelog "$(get_version)" "${2:-No release notes provided}"
        ;;
    *)
        echo "Usage: $0 {init|get|bump major|minor|patch|changelog 'message'}"
        exit 1
        ;;
esac
