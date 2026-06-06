#!/bin/bash
set -e

echo "Generating sample system activity..."

mkdir -p ../output ../logs

logger -t compliance-test "Sample security event: User authentication"
logger -t compliance-test "Sample system event: Service started"
logger -t compliance-test "Sample access event: File accessed"

cat > ../output/sample_config.txt << SAMPLE
Sample System Configuration
Generated: $(date)
Hostname: $(hostname)
Kernel: $(uname -r)
SAMPLE

echo "Sample data generated successfully"
