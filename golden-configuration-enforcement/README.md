# Golden Configuration Enforcement Platform

## What This Does

This platform implements automated configuration governance using golden configuration standards. It validates infrastructure configurations against approved baselines, detects configuration drift, identifies security violations, and blocks non-compliant deployments before they reach production environments.

The solution combines configuration validation, security enforcement, audit logging, compliance reporting, and deployment gate controls. It demonstrates Infrastructure as Code governance and compliance automation practices used by modern Platform Engineering, DevOps, DevSecOps, and SRE teams.

## Architecture

+---------------------------+
| Golden Configuration Repo |
+------------+--------------+
             |
             v
+---------------------------+
| Configuration Validator   |
| (Python Enforcement)      |
+------------+--------------+
             |
             v
+---------------------------+
| Drift Detection Engine    |
| DeepDiff Comparison       |
+------------+--------------+
             |
      +------+------+
      |             |
      v             v
+-----------+   +-----------+
| Compliant |   | Violations|
| Config    |   | Detected  |
+-----------+   +-----+-----+
                    |
                    v
          +------------------+
          | Deployment Block |
          +------------------+
                    |
                    v
          +------------------+
          | Audit Logs       |
          | Compliance Stats |
          +------------------+

## Prerequisites

- Ubuntu Linux
- Python 3.10+
- Git
- PyYAML
- DeepDiff
- JSON Schema

## Setup & Installation

python3 -m venv .venv

source .venv/bin/activate

pip install pyyaml deepdiff jsonschema

## How to Reproduce

1. Create golden configuration baselines.
2. Create current configurations.
3. Execute config_enforcer.py.
4. Review generated violations.
5. Execute pre_deploy_check.sh.
6. Generate compliance report.
7. Fix violations and re-run validation.

## Tools Used

- Python
- YAML
- JSON Schema
- DeepDiff
- Linux
- Git

## Key Skills Demonstrated

- Configuration Governance
- Infrastructure Compliance
- Security Baseline Enforcement
- Configuration Drift Detection
- Deployment Gate Automation
- Audit Logging
- Python Automation
- DevSecOps Controls

## Real-World Use Case

Organizations operating cloud infrastructure frequently enforce approved baseline configurations for servers, applications, databases, and network devices. This platform prevents unauthorized changes, identifies configuration drift, enforces security policies, and provides compliance evidence required by governance and regulatory frameworks.

## Lessons Learned

- Configuration drift creates operational risk.
- Automated enforcement reduces human error.
- Security validation should occur before deployment.
- Audit trails support compliance investigations.
- Golden configuration repositories simplify standardization.

## Troubleshooting Log

- Implemented complete validation logic from starter code.
- Added deployment blocking workflow.
- Added JSON schema validation.
- Added DeepDiff comparison engine.
- Added security violation detection.
- Improved Ubuntu 24.04 Python package installation workflow.
