#!/bin/bash
set -euo pipefail

BUILD_DIR="builds"
METADATA_DIR="metadata"
VERSION=$(cat VERSION)
BUILD_NUMBER=${BUILD_NUMBER:-$(date +%s)}
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
GIT_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

mkdir -p "$BUILD_DIR" "$METADATA_DIR"

build_artifact() {
    local artifact_name="app-${VERSION}-${BUILD_NUMBER}.tar.gz"
    local artifact_path="${BUILD_DIR}/${artifact_name}"

    tar -czf "$artifact_path" src/ VERSION CHANGELOG.md

    echo "$artifact_path"
}

generate_metadata() {
    local artifact_path="$1"
    local artifact_name
    artifact_name=$(basename "$artifact_path")
    local checksum
    checksum=$(sha256sum "$artifact_path" | awk '{print $1}')
    local size
    size=$(stat -c%s "$artifact_path")
    local metadata_file="${METADATA_DIR}/${artifact_name}.json"

    cat > "$metadata_file" << METADATA
{
  "artifact": {
    "name": "$artifact_name",
    "version": "$VERSION",
    "path": "$artifact_path",
    "size": $size,
    "checksum": {
      "algorithm": "sha256",
      "value": "$checksum"
    }
  },
  "build": {
    "number": "$BUILD_NUMBER",
    "date": "$BUILD_DATE",
    "builder": "$(whoami)@$(hostname)",
    "os": "$(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"')"
  },
  "source": {
    "commit": "$GIT_COMMIT",
    "branch": "$GIT_BRANCH",
    "repository": "$(git config --get remote.origin.url 2>/dev/null || echo local)"
  }
}
METADATA

    echo "$metadata_file"
}

create_git_tag() {
    local version="$1"
    local artifact_path="$2"
    local tag_name="v${version}"

    if git rev-parse "$tag_name" >/dev/null 2>&1; then
        echo "Tag $tag_name already exists"
        return 0
    fi

    git tag -a "$tag_name" -m "Release version $version

Build: $BUILD_NUMBER
Date: $BUILD_DATE
Commit: $GIT_COMMIT
Artifact: $(basename "$artifact_path")"

    echo "Git tag created: $tag_name"
}

echo "=== Starting Build Process ==="
echo "Version: $VERSION"
echo "Build Number: $BUILD_NUMBER"

artifact_path=$(build_artifact)
metadata_file=$(generate_metadata "$artifact_path")
create_git_tag "$VERSION" "$artifact_path"

echo ""
echo "=== Build Complete ==="
echo "Artifact: $artifact_path"
echo "Metadata: $metadata_file"
echo ""
cat "$metadata_file" | jq '.'
