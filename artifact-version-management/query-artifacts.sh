#!/bin/bash
set -euo pipefail

METADATA_DIR="metadata"

list_artifacts() {
    echo "=== Available Artifacts ==="

    shopt -s nullglob
    for metadata in "$METADATA_DIR"/*.json; do
        version=$(jq -r '.artifact.version' "$metadata")
        name=$(jq -r '.artifact.name' "$metadata")
        date=$(jq -r '.build.date' "$metadata")
        checksum=$(jq -r '.artifact.checksum.value' "$metadata" | cut -c1-16)
        echo "Version: $version | Artifact: $name | Built: $date | SHA256: ${checksum}..."
    done
}

get_artifact_info() {
    local version="${1:-}"

    if [ -z "$version" ]; then
        echo "Usage: $0 info VERSION"
        exit 1
    fi

    shopt -s nullglob
    for metadata in "$METADATA_DIR"/*.json; do
        artifact_version=$(jq -r '.artifact.version' "$metadata")
        if [ "$artifact_version" = "$version" ]; then
            echo "=== Artifact Information ==="
            jq '.' "$metadata"
            return 0
        fi
    done

    echo "No artifact found for version: $version"
    return 1
}

verify_artifact() {
    local artifact_path="${1:-}"
    local artifact_name
    artifact_name=$(basename "$artifact_path")
    local metadata_file="${METADATA_DIR}/${artifact_name}.json"

    if [ ! -f "$artifact_path" ]; then
        echo "Artifact not found: $artifact_path"
        return 1
    fi

    if [ ! -f "$metadata_file" ]; then
        echo "Metadata file not found: $metadata_file"
        return 1
    fi

    expected_checksum=$(jq -r '.artifact.checksum.value' "$metadata_file")
    actual_checksum=$(sha256sum "$artifact_path" | awk '{print $1}')

    if [ "$expected_checksum" = "$actual_checksum" ]; then
        echo "Verification PASSED: Checksums match"
        return 0
    else
        echo "Verification FAILED: Checksums do not match"
        echo "Expected: $expected_checksum"
        echo "Actual: $actual_checksum"
        return 1
    fi
}

case "${1:-}" in
    list)
        list_artifacts
        ;;
    info)
        get_artifact_info "${2:-}"
        ;;
    verify)
        verify_artifact "${2:-}"
        ;;
    *)
        echo "Usage: $0 {list|info VERSION|verify ARTIFACT_PATH}"
        exit 1
        ;;
esac
