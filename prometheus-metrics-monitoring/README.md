# Prometheus Metrics Instrumentation and Monitoring

## What This Does

This implementation instruments a Python Flask application with Prometheus metrics and exposes operational telemetry through a dedicated metrics endpoint.

The solution tracks request volume, request latency, active connections, and application health using Prometheus Counters, Histograms, and Gauges.

Prometheus continuously scrapes the application and stores time-series metrics that can be queried using PromQL for monitoring, troubleshooting, and performance analysis.

This forms the foundation of modern observability platforms used in cloud-native environments.

## Architecture

+------------------------------------------------------+
|                    Client Traffic                    |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|            Flask Application (Port 8000)            |
|                                                      |
|  /                                                   |
|  /api/data                                           |
|  /health                                             |
|  /metrics                                            |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|             Prometheus Client Library                |
|                                                      |
|  Counter                                              |
|  Histogram                                            |
|  Gauge                                                |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|               Prometheus Server                      |
|                    Port 9090                         |
|                                                      |
|  Scrapes /metrics every 15 seconds                   |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|                 PromQL Queries                       |
|                 Monitoring                           |
|                 Capacity Planning                    |
|                 Troubleshooting                      |
+------------------------------------------------------+

## Prerequisites

- Ubuntu Linux
- Python 3.12+
- python3-pip
- python3-venv
- Prometheus
- Flask
- prometheus-client
- curl
- wget
- Git

## Setup & Installation

sudo apt update

sudo apt install -y \
python3-pip \
python3-venv \
curl \
wget

python3 -m venv venv

source venv/bin/activate

pip install flask prometheus-client

## How to Reproduce

source venv/bin/activate

python app.py

curl http://localhost:8000/

curl http://localhost:8000/api/data

curl http://localhost:8000/health

curl http://localhost:8000/metrics

sudo systemctl start prometheus

curl http://localhost:9090/api/v1/targets

## Tools Used

- Prometheus
- PromQL
- Python
- Flask
- prometheus-client
- Linux
- systemd
- curl
- Bash

## Key Skills Demonstrated

- Application instrumentation
- Prometheus deployment and configuration
- Metrics collection and exposure
- Counter, Histogram, and Gauge implementation
- PromQL querying
- Service monitoring
- Observability engineering
- Platform monitoring fundamentals
- Performance measurement
- Production telemetry collection

## Real-World Use Case

Production applications expose Prometheus metrics to provide visibility into performance, latency, throughput, and system health. Platform and SRE teams use these metrics to build dashboards, create alerts, identify bottlenecks, and maintain service reliability at scale.

## Lessons Learned

- Metrics must be instrumented directly within application code.
- Histograms provide latency distribution information.
- Counters are ideal for tracking cumulative events.
- Gauges are useful for real-time state measurements.
- PromQL enables powerful analysis of time-series telemetry.

## Troubleshooting Log

Issue:
Prometheus binaries were not installed in the environment.

Resolution:
Downloaded and installed Prometheus and promtool manually.

Issue:
Python dependencies were missing.

Resolution:
Installed Flask and prometheus-client inside a virtual environment.

Issue:
Metrics were not visible until traffic was generated.

Resolution:
Created synthetic load and verified metric collection through scraping.

Issue:
Original lab referenced an outdated Prometheus release.

Resolution:
Installed the latest available Prometheus release instead of the hardcoded older version.
