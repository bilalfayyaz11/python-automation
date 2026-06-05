#!/bin/bash
set -e

FILL_DIR="/tmp/disk-fill-test"
MAX_MB=512

mkdir -p "$FILL_DIR"

echo "Triggering disk space incident safely..."
df -h /

for i in $(seq 1 8); do
  dd if=/dev/zero of="$FILL_DIR/fill-$i.img" bs=64M count=1 status=progress
  USED=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
  echo "Current disk usage: ${USED}%"

  if [ "$USED" -ge 90 ]; then
    echo "Disk usage reached safety threshold."
    break
  fi
done

echo "Disk space incident triggered"
df -h /
