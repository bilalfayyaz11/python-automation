# Grafana Dashboard Evidence Report

## System Information

- Date: Fri Jun  5 21:18:15 UTC 2026
- Hostname: ip-172-31-10-176
- Operating System: Ubuntu 24.04.3 LTS
- Grafana Version: Version 13.0.2 (commit: 3fcdbc5a, branch: release-13.0.2)
- Prometheus Version: prometheus, version 3.12.0 (branch: HEAD, revision: 9f27dffc1f93ca23287972f632025879f2d1c658)
- Node Exporter Version: node_exporter, version 1.11.1 (branch: HEAD, revision: 0dd664dece3f8319f6bec5a221acd2c7ad13a23d)

## Monitoring Stack

This system runs a complete infrastructure monitoring stack using Grafana, Prometheus, and Node Exporter.

Prometheus collects metrics from itself and from Node Exporter. Node Exporter exposes system-level Linux metrics including CPU, memory, disk, filesystem, and network telemetry. Grafana uses Prometheus as a data source and visualizes those metrics through operational dashboards.

## Dashboards Created

### System Performance Overview

Panels:

- CPU Usage (%)
- Memory Usage
- Disk Usage by Mount Point
- Network Traffic

Dashboard URL:

http://172.31.10.176:3000/d/system-performance-overview

### Monitoring Health

Panels:

- Monitoring Targets Status
- Prometheus Query Rate

Dashboard URL:

http://172.31.10.176:3000/d/monitoring-health

## Data Source

- Name: Prometheus
- Type: Prometheus
- URL: http://localhost:9090
- Access Mode: Proxy
- Status: Connected

## Prometheus Targets

```json
{
  "job": "node",
  "health": "up",
  "scrapeUrl": "http://localhost:9100/metrics"
}
{
  "job": "prometheus",
  "health": "up",
  "scrapeUrl": "http://localhost:9090/metrics"
}
```

## Service Status

```text
node_exporter: active
prometheus: active
grafana-server: active
```

## Metrics Summary

- Active Targets: 2
- Dashboard Count: 2
- Memory Used: 1.5Gi
- Disk Usage Root: 34%

## Evidence Files

- dashboard-evidence.md
- system-performance-dashboard.json
- monitoring-health-dashboard.json
- system-performance-dashboard-export.json
- monitoring-health-dashboard-export.json
- metrics-summary.txt
