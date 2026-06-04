#!/bin/bash

set -euo pipefail

CURRENT_DIR="$HOME/config-drift-scanner/current"

mkdir -p "$CURRENT_DIR"

echo "Capturing current configuration..."

cp /etc/hosts "$CURRENT_DIR/hosts.current"

dpkg -l > "$CURRENT_DIR/packages.current"

systemctl list-units --type=service --state=running > "$CURRENT_DIR/services.current"

ip addr show > "$CURRENT_DIR/network.current"

cp \
"$HOME/config-drift-scanner/app-configs/app-config.yaml" \
"$CURRENT_DIR/app-config.current.yaml"

echo "Current configuration captured at: $CURRENT_DIR"
