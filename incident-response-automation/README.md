
# Incident Response Automation

## What This Does

This implementation provides a controlled incident response environment for simulating, investigating, resolving, and documenting production-style infrastructure failures.

The environment includes service outage simulation, CPU saturation events, disk space exhaustion scenarios, structured operational runbooks, automated drill execution, and incident logging. The goal is to develop repeatable troubleshooting workflows and operational readiness for Linux-based production environments.

This demonstrates practical Site Reliability Engineering (SRE), Platform Engineering, DevOps, and AIOps operational procedures used during real-world infrastructure incidents.

## Architecture

```text
+--------------------------------------------------+
|              Incident Response Operator          |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              Drill Automation Layer              |
|                                                  |
|  execute-drill.sh                                |
|  trigger-service-crash.sh                        |
|  trigger-cpu-spike.sh                            |
|  trigger-disk-full.sh                            |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              Linux Service Layer                 |
|                                                  |
|  Nginx Web Service (Port 8080)                   |
|  PostgreSQL Database Service                     |
|  CPU Monitoring                                  |
|  Memory Monitoring                               |
|  Disk Monitoring                                 |
|  Port Verification                               |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              Incident Documentation              |
|                                                  |
|  incident_logger.py                              |
|  runbook-template.md                             |
|  runbook-service-failure.md                      |
|  runbook-cpu-spike.md                            |
|  runbook-disk-space.md                           |
|  incident-logs/*.json                            |
|  drill-*.log                                     |
+--------------------------------------------------+
```

## Prerequisites

* Ubuntu 24.04
* Git
* Python 3
* Python Pip
* Nginx
* PostgreSQL
* curl
* htop
* sysstat

## Setup & Installation

```bash
sudo apt update

sudo apt install -y \
nginx \
postgresql \
postgresql-contrib \
python3 \
python3-pip \
curl \
htop \
sysstat
```

## How to Reproduce

```bash
cd ~/incident-drill

./execute-drill.sh service

./execute-drill.sh cpu

./execute-drill.sh disk
```

## Tools Used

* Linux
* Ubuntu 24.04
* Bash
* Python 3
* Nginx
* PostgreSQL
* systemd
* journalctl
* curl
* ss
* top
* ps
* df
* du
* Git

## Key Skills Demonstrated

* Incident Response Operations
* Linux Systems Administration
* Production Troubleshooting
* Service Failure Recovery
* Nginx Administration
* PostgreSQL Service Management
* Bash Automation
* Python Automation
* Root Cause Analysis
* Operational Documentation
* Runbook Development
* Platform Reliability Engineering

## Real-World Use Case

Organizations operating customer-facing infrastructure regularly conduct incident response exercises to ensure engineering teams can recover services quickly and safely during outages. This workflow can be used by SRE, Platform Engineering, DevOps, Infrastructure Operations, Cloud Engineering, and AIOps teams to improve operational readiness and reduce Mean Time To Recovery (MTTR).

## Lessons Learned

* Structured runbooks reduce recovery time.
* Capturing system state improves root cause analysis.
* Configuration backups simplify rollback.
* Validation before restart prevents additional outages.
* Controlled simulations reveal operational gaps safely.

## Troubleshooting Log

* Replaced netstat with ss on Ubuntu 24.04.
* Added safe disk usage limits.
* Added Nginx backup before corruption testing.
* Added Nginx configuration validation before restart.
* Added PID tracking for CPU stress cleanup.
  

