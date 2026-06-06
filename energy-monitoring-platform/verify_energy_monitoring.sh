#!/bin/bash

echo "=== Energy Monitoring Verification ==="
echo

echo "1. Checking InfluxDB status..."
systemctl is-active influxdb && echo "✓ InfluxDB running" || echo "✗ InfluxDB not running"

echo "2. Checking Telegraf status..."
systemctl is-active telegraf && echo "✓ Telegraf running" || echo "✗ Telegraf not running"

echo "3. Checking Kapacitor status..."
systemctl is-active kapacitor && echo "✓ Kapacitor running" || echo "✗ Kapacitor not running"

echo "4. Checking energy simulator..."
pgrep -f energy_simulator.sh > /dev/null && echo "✓ Energy simulator running" || echo "✗ Energy simulator not running"

echo "5. Checking data source..."
RECORD_COUNT=$(wc -l < /var/log/energy_data.log)
[ "$RECORD_COUNT" -gt 10 ] && echo "✓ Energy data generated ($RECORD_COUNT records)" || echo "✗ Insufficient data"

echo "6. Checking alert log..."
[ -f /var/log/kapacitor/energy_alerts.log ] && echo "✓ Alert log exists" || echo "✗ Alert log missing"

echo
echo "=== Verification Complete ==="
