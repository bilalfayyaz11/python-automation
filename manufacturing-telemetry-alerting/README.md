# Manufacturing Telemetry Collection and Downtime Alerting Platform

## What This Does

This implementation provides a manufacturing telemetry platform that continuously collects equipment metrics, stores them in a time-series database, detects equipment downtime, and generates automated alerts when failures occur.

The platform simulates industrial equipment such as CNC machines, streams operational telemetry into InfluxDB, analyzes equipment health in near real time, and creates alert records whenever abnormal conditions are detected.

The solution demonstrates a production-style monitoring architecture commonly used in manufacturing operations, industrial IoT deployments, plant-floor observability systems, and predictive maintenance initiatives.

## Architecture

    +-----------------------------------+
    | Manufacturing Equipment           |
    | CNC Machines / Industrial Assets  |
    +----------------+------------------+
                     |
                     v
    +-----------------------------------+
    | Telemetry Simulator               |
    | equipment_simulator.py            |
    |                                   |
    | Temperature                       |
    | Pressure                          |
    | Speed                             |
    | Status                            |
    +----------------+------------------+
                     |
                     v
    +-----------------------------------+
    | InfluxDB Time-Series Database     |
    | Bucket: manufacturing             |
    +----------------+------------------+
                     |
                     v
    +-----------------------------------+
    | Downtime Monitor                  |
    | downtime_monitor.py               |
    |                                   |
    | Status Validation                 |
    | Telemetry Availability Checks     |
    | Downtime Detection                |
    +----------------+------------------+
                     |
                     v
    +-----------------------------------+
    | Alerting Layer                    |
    | /tmp/manufacturing_alerts.log     |
    | alert_webhook.py                  |
    +----------------+------------------+
                     |
                     v
    +-----------------------------------+
    | Operations Team                   |
    | Incident Response                 |
    | Production Monitoring             |
    +-----------------------------------+

## Prerequisites

- Ubuntu 24.04 LTS
- Python 3.12+
- Python virtual environments
- InfluxDB 2.x
- Influx CLI
- Telegraf
- Git
- tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree curl wget net-tools

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install influxdb-client requests

## How to Reproduce

Create telemetry environment:

source venv/bin/activate

source .env

Run equipment simulator:

python3 equipment_simulator.py

Run downtime monitor:

python3 downtime_monitor.py

Run webhook receiver:

python3 alert_webhook.py

Query telemetry:

influx query '
from(bucket: "manufacturing")
  |> range(start: -10m)
'

Monitor alerts:

tail -f /tmp/manufacturing_alerts.log

## Tools Used

- Python 3
- InfluxDB 2.x
- Influx CLI
- Telegraf
- InfluxDB Client SDK
- Requests
- Linux
- Bash
- Systemd
- HTTP
- JSON
- Git

## Key Skills Demonstrated

- Manufacturing telemetry collection
- Industrial monitoring design
- Time-series database management
- InfluxDB administration
- Equipment health monitoring
- Downtime detection automation
- Alerting system development
- Industrial IoT architecture
- Operations monitoring
- Python automation engineering
- Incident detection workflows
- Production observability

## Real-World Use Case

Manufacturing facilities rely on continuous telemetry streams from production equipment to maximize uptime and reduce operational losses. Equipment failures can halt production lines and create significant financial impact. This implementation demonstrates how telemetry collection, centralized storage, automated monitoring, and alerting can be combined into a scalable observability platform that enables operations teams to identify and respond to failures rapidly.

## Lessons Learned

- Telemetry pipelines require reliable time-series storage.
- Downtime detection depends on both status monitoring and missing-data detection.
- Alert cooldown logic is essential to prevent alert storms.
- InfluxDB provides efficient storage for industrial telemetry workloads.
- Manufacturing monitoring systems benefit from structured alert workflows.

## Troubleshooting Log

Issue:
InfluxData repository signing failed during package installation.

Resolution:
Reconfigured repository key management and installed supported packages for Ubuntu.

Issue:
Original lab instructions referenced legacy InfluxDB database creation commands.

Resolution:
Migrated implementation to InfluxDB 2.x bucket-based architecture.

Issue:
Telemetry queries initially returned no results.

Resolution:
Verified bucket configuration, token permissions, and simulator writes.

Issue:
Alert generation can become noisy during prolonged outages.

Resolution:
Implemented alert cooldown tracking to suppress duplicate alerts.

Issue:
Industrial telemetry simulations require realistic operating ranges.

Resolution:
Implemented controlled ranges for temperature, pressure, speed, and equipment status.
