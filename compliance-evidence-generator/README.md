# Compliance Evidence Generator

## What This Does

This implementation provides an automated compliance evidence generator for regulated infrastructure environments.

The system collects Linux system evidence, access activity, configuration snapshots, and security-related events, then generates structured JSON, HTML, and CSV reports.

It also creates audit logs that record every evidence collection and report generation event, making the workflow traceable and reviewable.

This type of automation is useful for DevOps, SRE, Platform Engineering, Cybersecurity, and GRC teams that need repeatable compliance evidence for audits and internal controls.

## Architecture

    +-----------------------------+
    | Linux System Sources        |
    | journalctl, systemctl, last |
    | ip addr, packages, users    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Evidence Collector          |
    | evidence_collector.py       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Compliance Workflow         |
    | compliance_workflow.py      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Report Generator            |
    | JSON, HTML, CSV             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Audit Logger                |
    | audit.log, audit.json       |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python venv
- Python pip
- Git
- jq
- curl
- Linux systemd tools

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv jq git curl

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pyyaml jinja2 python-dateutil

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Generate sample system activity:

cd scripts

./generate_sample_data.sh

Run the compliance workflow:

python3 compliance_workflow.py

Verify generated reports:

cd ..

ls -lh output/

jq '.report_metadata' output/compliance_report.json

jq '.evidence_summary' output/compliance_report.json

Review audit logs:

tail -10 logs/audit.log

cat logs/audit.log | grep "evidence_collection" | wc -l

cat logs/audit.log | grep "report_generation" | wc -l

## Tools Used

- Python 3
- PyYAML
- Jinja2
- python-dateutil
- jq
- Bash
- Linux
- systemd
- journalctl
- JSON
- YAML
- CSV
- HTML

## Key Skills Demonstrated

- Compliance evidence automation
- Linux evidence collection
- Audit trail generation
- Structured logging
- JSON report generation
- HTML report generation
- CSV report generation
- Python workflow orchestration
- System command automation
- Defensive error handling
- Configuration-driven automation
- GRC support tooling

## Real-World Use Case

Regulated organizations need repeatable evidence showing system activity, access history, configuration state, and security-relevant events. This system automates the first layer of evidence collection and report generation so engineering and compliance teams can produce consistent artifacts for internal reviews, control validation, and external audits.

## Lessons Learned

- Compliance automation requires both evidence collection and audit logging.
- System commands can return empty or partial results in fresh cloud environments, so graceful handling is important.
- JSON is useful for machine-readable audit artifacts, while HTML and CSV support human review.
- Configuration files make the workflow easier to adapt across frameworks and environments.
- Auditability improves when every collection and reporting action is logged.

## Troubleshooting Log

Issue:
pip3 was missing from the Ubuntu environment.

Resolution:
Installed python3-pip through apt before creating the Python environment.

Issue:
Some access log commands can return empty results on fresh cloud systems.

Resolution:
Implemented command execution with graceful warning handling instead of hard failure.

Issue:
Firewall command compatibility can vary across modern Ubuntu systems.

Resolution:
Used iptables first and added nftables fallback support.

Issue:
Python cache directories were generated during execution.

Resolution:
Removed __pycache__ before GitHub push and added .gitignore rules.

Issue:
Virtual environment files should not be pushed to GitHub.

Resolution:
Removed venv before push and excluded it in .gitignore.
