# Configuration Drift Scanner

## What This Does

This implementation provides a configuration drift scanner for detecting differences between baseline and current system/application configurations.

The scanner captures trusted baseline states for system files, packages, services, network configuration, environment variables, and YAML application settings. It then compares the current state against the baseline, detects changes, and generates structured drift reports in JSON and text formats.

This is useful for DevOps, SRE, platform engineering, security, and compliance workflows where unauthorized or unexpected configuration changes can cause outages, vulnerabilities, or audit failures.

## Architecture

    +-----------------------------+
    | Baseline Capture            |
    | capture_baseline.sh         |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Baseline Store              |
    | baselines/                  |
    | hosts, packages, services   |
    | network, environment, YAML  |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Current State Capture       |
    | capture_current.sh          |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Drift Scanner Engine        |
    | drift_scanner.py            |
    | hashes + line comparison    |
    | DeepDiff YAML comparison    |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Reports                     |
    | reports/*.json              |
    | reports/*.txt               |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Automated Scan              |
    | automated_scan.sh           |
    | exit code for CI/CD usage   |
    +-----------------------------+

## Prerequisites

- Ubuntu Linux or compatible Linux environment
- Python 3.8 or newer
- python3-pip
- python3-venv
- jq
- Git
- Bash shell
- PyYAML
- DeepDiff

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv jq git

python3 -m venv venv

source venv/bin/activate

pip install pyyaml deepdiff

## How to Reproduce

Create the directory structure.

mkdir -p ~/config-drift-scanner/{baselines,current,reports,scripts,app-configs}

Capture the baseline.

./scripts/capture_baseline.sh

Create or modify the monitored application configuration.

nano app-configs/app-config.yaml

Capture the current state.

./scripts/capture_current.sh

Run the drift scanner.

python3 scripts/drift_scanner.py

Review the JSON report.

cat reports/*.json | jq .

Review the text report.

cat reports/*.txt

Run the automated scan workflow.

./scripts/automated_scan.sh

## Tools Used

- Python
- PyYAML
- DeepDiff
- jq
- Bash
- Linux system commands
- SHA256 hashing
- JSON reporting
- YAML parsing
- systemctl
- dpkg
- iproute2

## Key Skills Demonstrated

- Built a baseline-driven configuration drift detection system
- Captured system and application configuration states
- Compared text-based configuration files using hashes and line-level checks
- Compared YAML configuration using structured deep comparison
- Generated machine-readable JSON reports for automation workflows
- Generated human-readable text reports for operational review
- Created an automated scan script with CI/CD-friendly exit codes
- Applied configuration governance practices used in DevOps and compliance environments

## Real-World Use Case

Configuration drift scanners are used by DevOps, SRE, platform engineering, and security teams to detect unauthorized or accidental changes across infrastructure. In production environments, drift can cause deployment failures, inconsistent server behavior, security misconfiguration, compliance violations, and hard-to-debug outages. This scanner provides a lightweight foundation for detecting those changes and integrating drift checks into CI/CD pipelines or scheduled operational audits.

## Lessons Learned

- Configuration drift can happen across both system-level and application-level settings.
- Baseline comparison creates an audit trail for infrastructure consistency.
- Hash-based comparison is fast for detecting whether files changed.
- Structured YAML comparison provides more useful insight than raw line comparison.
- Automation scripts should return non-zero exit codes when drift is detected so pipelines can fail safely.

## Troubleshooting Log

- Global pip installation was avoided because Ubuntu 24.04 may block unmanaged global package installation through PEP 668 protections.
- A Python virtual environment was used to install PyYAML and DeepDiff safely.
- The starter scanner contained incomplete methods for hashing, text comparison, YAML comparison, scanning, reporting, and main execution.
- Replaced placeholders with a complete drift scanning implementation.
- Added line-length-safe comparison so added or removed lines are detected correctly.
- Added jq-based report validation for structured JSON inspection.
- Added automated scanning with latest-report selection to avoid reading stale report files.
