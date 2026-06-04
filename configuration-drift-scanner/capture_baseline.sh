#!/bin/bash

set -euo pipefail

BASELINE_DIR="$HOME/config-drift-scanner/baselines"

mkdir -p "$BASELINE_DIR"

echo "Capturing baseline configuration..."

cp /etc/hosts "$BASELINE_DIR/hosts.baseline"

dpkg -l > "$BASELINE_DIR/packages.baseline"

systemctl list-units --type=service --state=running > "$BASELINE_DIR/services.baseline"

ip addr show > "$BASELINE_DIR/network.baseline"

env | sort > "$BASELINE_DIR/environment.baseline"

echo "Baseline captured successfully at: $BASELINE_DIR"
