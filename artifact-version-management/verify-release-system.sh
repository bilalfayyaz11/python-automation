#!/bin/bash

echo "=== Release System Verification ==="
echo ""

echo "1. Version Management:"
if [ -f VERSION ] && grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$' VERSION; then
    echo "   PASS - Version file valid: $(cat VERSION)"
else
    echo "   FAIL - Version file missing or invalid"
fi

echo "2. Build Artifacts:"
artifact_count=$(find builds -name "*.tar.gz" 2>/dev/null | wc -l)
if [ "$artifact_count" -gt 0 ]; then
    echo "   PASS - Found $artifact_count artifact(s)"
else
    echo "   FAIL - No artifacts found"
fi

echo "3. Metadata:"
metadata_count=$(find metadata -name "*.json" 2>/dev/null | wc -l)
if [ "$metadata_count" -gt 0 ]; then
    echo "   PASS - Found $metadata_count metadata file(s)"
else
    echo "   FAIL - No metadata found"
fi

echo "4. Metadata JSON Validation:"
for meta in metadata/*.json; do
    if jq empty "$meta" 2>/dev/null; then
        echo "   PASS - Valid JSON: $(basename "$meta")"
    else
        echo "   FAIL - Invalid JSON: $(basename "$meta")"
    fi
done

echo "5. Git Tags:"
tag_count=$(git tag | wc -l)
if [ "$tag_count" -gt 0 ]; then
    echo "   PASS - Found $tag_count tag(s)"
    git tag | head -3
else
    echo "   FAIL - No tags found"
fi

echo "6. Artifact Integrity:"
artifact=$(find builds -name "*.tar.gz" | head -1)
if [ -n "$artifact" ]; then
    ./query-artifacts.sh verify "$artifact" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "   PASS - Artifact integrity verified"
    else
        echo "   FAIL - Artifact verification failed"
    fi
else
    echo "   SKIP - No artifacts to verify"
fi

echo ""
echo "=== Verification Complete ==="
