# Energy Monitoring Platform with Real-Time Threshold Detection

## What This Does

This implementation provides a complete energy monitoring and alerting platform using Telegraf, InfluxDB, and Kapacitor.

The platform continuously generates simulated energy consumption metrics, ingests them into a time-series database, and evaluates real-time threshold rules to identify abnormal energy usage patterns.

The solution demonstrates how modern observability systems collect telemetry, store historical measurements, perform stream processing, and trigger automated alerts when operational thresholds are exceeded.

This architecture is commonly used by DevOps, SRE, Platform Engineering, Data Center Operations, and AIOps teams to monitor infrastructure utilization, power consumption, environmental metrics, and operational anomalies.

## Architecture

    +---------------------------------------------------+
    | Energy Simulator                                  |
    | energy_simulator.sh                               |
    +----------------------+----------------------------+
                           |
                           v
    +---------------------------------------------------+
    | Energy Data Source                                |
    | /var/log/energy_data.log                          |
    +----------------------+----------------------------+
                           |
                           v
    +---------------------------------------------------+
    | Telegraf                                           |
    | Metrics Collection Agent                           |
    | CPU / Memory / DiskIO / System / Energy Metrics    |
    +----------------------+----------------------------+
                           |
                           v
    +---------------------------------------------------+
    | InfluxDB 2                                         |
    | Time-Series Database                               |
    | Bucket: energy_metrics                             |
    +----------------------+----------------------------+
                           |
                           v
    +---------------------------------------------------+
    | Kapacitor                                          |
    | Stream Processing Engine                           |
    | Threshold Evaluation                               |
    | Warning > 100W                                     |
    | Critical > 120W                                    |
    +----------------------+----------------------------+
                           |
                           v
    +---------------------------------------------------+
    | Alert Output                                       |
    | /var/log/kapacitor/energy_alerts.log               |
    +---------------------------------------------------+

## Prerequisites

- Ubuntu 24.04
- Git
- wget
- curl
- bc
- tree
- InfluxDB 2.x
- Influx CLI
- Telegraf
- Kapacitor
- systemd

## Setup & Installation

Install base dependencies:

sudo apt update

sudo apt install -y wget curl bc tree

Install InfluxDB manually:

wget https://download.influxdata.com/influxdb/releases/influxdb2-2.9.1_linux_amd64.tar.gz

tar xvfz influxdb2-2.9.1_linux_amd64.tar.gz

sudo cp influxdb2-2.9.1/influxd /usr/local/bin/

Install Influx CLI:

wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.8.0-linux-amd64.tar.gz

tar xvzf influxdb2-client-2.8.0-linux-amd64.tar.gz

sudo cp influx /usr/local/bin/

Install Telegraf:

wget https://dl.influxdata.com/telegraf/releases/telegraf_1.38.4-1_amd64.deb

sudo dpkg -i telegraf_1.38.4-1_amd64.deb

Install Kapacitor:

wget https://dl.influxdata.com/kapacitor/releases/kapacitor_1.7.6-1_amd64.deb

sudo dpkg -i kapacitor_1.7.6-1_amd64.deb

## How to Reproduce

Create the InfluxDB system service:

sudo useradd --system --home /var/lib/influxdb --shell /usr/sbin/nologin influxdb 2>/dev/null || true

sudo mkdir -p /var/lib/influxdb /var/log/influxdb

sudo chown -R influxdb:influxdb /var/lib/influxdb /var/log/influxdb

sudo tee /etc/systemd/system/influxdb.service > /dev/null << 'SERVICE'
[Unit]
Description=InfluxDB 2 Time-Series Database
After=network-online.target
Wants=network-online.target

[Service]
User=influxdb
Group=influxdb
ExecStart=/usr/local/bin/influxd --engine-path /var/lib/influxdb/engine --bolt-path /var/lib/influxdb/influxd.bolt
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload

sudo systemctl enable influxdb

sudo systemctl start influxdb

Initialize InfluxDB:

influx setup \
  --host http://localhost:8086 \
  --username admin \
  --password adminpassword123 \
  --org energyorg \
  --bucket energy_metrics \
  --retention 168h \
  --force

Create the energy simulator:

sudo tee /usr/local/bin/energy_simulator.sh > /dev/null << 'SCRIPT'
#!/bin/bash

LOG_FILE="/var/log/energy_data.log"
touch "$LOG_FILE"
chmod 666 "$LOG_FILE"

while true; do
    POWER_WATTS=$((50 + RANDOM % 100))
    VOLTAGE=$((110 + RANDOM % 15))
    CURRENT=$(echo "scale=3; $POWER_WATTS / $VOLTAGE" | bc)
    TIMESTAMP=$(date +%s%N)

    echo "energy_consumption,location=datacenter,rack=A1 power_watts=${POWER_WATTS}i,voltage=${VOLTAGE}i,current=${CURRENT} ${TIMESTAMP}" >> "$LOG_FILE"

    sleep 5
done
SCRIPT

sudo chmod +x /usr/local/bin/energy_simulator.sh

nohup sudo /usr/local/bin/energy_simulator.sh > /tmp/energy_simulator.log 2>&1 &

Configure Telegraf:

sudo systemctl restart telegraf

Verify ingestion:

influx query '
from(bucket: "energy_metrics")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "energy_consumption")
  |> limit(n: 5)
' --host http://localhost:8086

Create the threshold detection rule:

kapacitor define energy_alert \
  -tick energy_threshold_alert.tick \
  -type stream \
  -dbrp energy_metrics.autogen

kapacitor enable energy_alert

Verify threshold task execution:

kapacitor list tasks

## Tools Used

- Linux
- Bash
- InfluxDB 2.9.1
- Influx CLI
- Telegraf 1.38.4
- Kapacitor 1.7.6
- systemd
- Time-Series Databases
- Stream Processing
- Observability Tooling

## Key Skills Demonstrated

- Time-series database administration
- Metrics ingestion pipeline design
- Telemetry collection
- Telegraf configuration
- InfluxDB bucket management
- Kapacitor stream processing
- Threshold-based monitoring
- Infrastructure observability
- AIOps foundations
- Service troubleshooting
- Linux operations
- Monitoring architecture design

## Real-World Use Case

Organizations operating cloud infrastructure, edge computing systems, manufacturing facilities, smart buildings, or data centers often need continuous visibility into energy consumption and operational metrics. This architecture provides a scalable approach for collecting measurements, storing historical telemetry, identifying abnormal patterns, and generating alerts before resource utilization becomes a business risk. Similar monitoring pipelines are commonly deployed in enterprise observability platforms and SRE environments.

## Lessons Learned

- Direct vendor repositories may not always support the latest Linux distribution releases.
- Manual binary installation can be required when package repositories lag behind operating system releases.
- Token-based authentication must be configured correctly between InfluxDB and dependent services.
- Stream processing pipelines require validation of ingestion, task execution, and alert output paths.
- End-to-end verification is essential because service health alone does not prove the full monitoring pipeline is working.

## Troubleshooting Log

Issue:
InfluxData Ubuntu Noble repository returned HTTP 404 errors.

Resolution:
Removed the broken repository configuration and used direct package and binary installation methods.

Issue:
InfluxDB package URLs referenced in the original instructions were outdated or unavailable.

Resolution:
Installed InfluxDB using the current Linux tarball and manually placed the executable in /usr/local/bin.

Issue:
InfluxDB service failed with status 203/EXEC.

Resolution:
Located the actual influxd binary and copied it manually into /usr/local/bin with executable permissions.

Issue:
Kapacitor failed with HTTP 401 authorization errors.

Resolution:
Configured InfluxDB token authentication and disabled startup subscription linking for compatibility with the InfluxDB 2.x setup.

Issue:
Kapacitor task executed but the alert file was not immediately generated.

Resolution:
Validated ingestion, task execution, threshold configuration, and forced high-value test data for stream evaluation.

Issue:
Legacy netstat verification was unsuitable for the modern Ubuntu environment.

Resolution:
Used ss -tlnp for service port validation.
