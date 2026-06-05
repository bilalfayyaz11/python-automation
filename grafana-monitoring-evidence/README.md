# Grafana Monitoring Dashboards and Evidence Collection

## What This Does

This implementation deploys a complete monitoring and visualization stack using Grafana, Prometheus, and Node Exporter.

The solution collects infrastructure telemetry, stores time-series metrics, visualizes operational health through dashboards, and generates an evidence package suitable for audits, operational reviews, and platform validation.

The environment includes automated dashboard provisioning, Prometheus integration, infrastructure monitoring, dashboard exports, and evidence archival.

This architecture represents a common observability foundation used in production cloud and platform environments.

## Architecture

+------------------------------------------------------+
|                   Linux Host                         |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|                  Node Exporter                       |
|                     Port 9100                        |
|                                                      |
| CPU                                                   |
| Memory                                                |
| Disk                                                  |
| Network                                               |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|                   Prometheus                         |
|                     Port 9090                        |
|                                                      |
| Scrapes Metrics                                      |
| Stores Time Series Data                              |
| Executes PromQL Queries                              |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|                     Grafana                          |
|                     Port 3000                        |
|                                                      |
| System Performance Dashboard                         |
| Monitoring Health Dashboard                          |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|                Evidence Collection                   |
|                                                      |
| Dashboard JSON Exports                               |
| Metrics Summary                                      |
| Audit Documentation                                  |
| Evidence Archive                                     |
+------------------------------------------------------+

## Prerequisites

- Ubuntu Linux
- systemd
- Prometheus
- Grafana
- Node Exporter
- curl
- jq
- stress-ng
- Git

## Setup & Installation

sudo apt update

sudo apt install -y \
curl \
wget \
jq \
stress-ng \
software-properties-common

Install:

- Prometheus
- Node Exporter
- Grafana

Enable services:

sudo systemctl enable prometheus
sudo systemctl enable node_exporter
sudo systemctl enable grafana-server

## How to Reproduce

Start services:

sudo systemctl start prometheus
sudo systemctl start node_exporter
sudo systemctl start grafana-server

Verify:

curl http://localhost:9090/api/v1/targets

Access Grafana:

http://localhost:3000

Configure Prometheus datasource.

Create dashboards:

- System Performance Overview
- Monitoring Health

Export dashboards.

Generate evidence package.

Create archive.

## Tools Used

- Grafana
- Prometheus
- PromQL
- Node Exporter
- Linux
- systemd
- jq
- curl
- stress-ng

## Key Skills Demonstrated

- Monitoring stack deployment
- Grafana dashboard design
- Prometheus integration
- Infrastructure observability
- PromQL querying
- Dashboard provisioning
- Monitoring evidence generation
- Operational reporting
- Metrics validation
- Platform monitoring

## Real-World Use Case

Production infrastructure teams use Grafana dashboards to monitor system performance, identify bottlenecks, investigate incidents, and provide operational visibility across cloud and on-premise environments. Evidence packages are frequently generated for audits, compliance reviews, customer reporting, and internal operational assessments.

## Lessons Learned

- Monitoring is most valuable when paired with meaningful visualizations.
- Prometheus provides flexible metric collection and querying.
- Node Exporter offers rich infrastructure telemetry with minimal configuration.
- Dashboard exports provide reproducible monitoring environments.
- Evidence generation simplifies operational reporting and audits.

## Troubleshooting Log

Issue:
Prometheus and Node Exporter were not installed.

Resolution:
Installed current releases and configured systemd services.

Issue:
Grafana repository installation method in older documentation used deprecated apt-key.

Resolution:
Used modern signed keyring installation method.

Issue:
Dashboards initially contain no meaningful data.

Resolution:
Generated synthetic workload using stress-ng and disk operations.

Issue:
Operational evidence required manual collection.

Resolution:
Automated dashboard exports, metrics summaries, and archive generation.
