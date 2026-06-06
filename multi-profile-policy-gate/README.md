# Multi-Profile Policy Gate

## What This Does

This implementation provides a multi-profile policy enforcement gateway for systems that need to operate across different industry compliance contexts.

The gateway loads Healthcare, Finance, and Retail policy profiles from YAML configuration files, dynamically switches the active profile through an HTTP API, and enforces different rule sets based on the active business context.

It exposes REST endpoints for profile discovery, runtime profile switching, service health checks, and policy enforcement decisions.

This pattern is useful for SaaS platforms, API gateways, internal developer platforms, and multi-tenant systems where different customers or workloads require different compliance rules.

## Architecture

    +-----------------------------+
    | Client / Service Request    |
    | JSON payload                |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | API Gateway                 |
    | api_gateway.py              |
    | /health                     |
    | /profiles                   |
    | /status                     |
    | /switch-profile             |
    | /enforce                    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Policy Gate Engine          |
    | policy_gate.py              |
    | Rule Evaluation             |
    | Violation Detection         |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Active Profile Manager      |
    | config_manager.py           |
    | config/active_profile.json  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | YAML Policy Profiles        |
    | healthcare.yaml             |
    | finance.yaml                |
    | retail.yaml                 |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python venv
- Python pip
- curl
- jq
- Git
- Bash

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv curl jq git

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pyyaml requests

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Start the policy gate API server:

python3 api_gateway.py

In another terminal, verify service health:

curl -s http://localhost:8080/health | jq

List available profiles:

curl -s http://localhost:8080/profiles | jq

Switch to the healthcare profile:

curl -s -X POST http://localhost:8080/switch-profile \
  -H "Content-Type: application/json" \
  -d '{"profile": "healthcare"}' | jq

Submit a non-compliant healthcare request:

curl -s -X POST http://localhost:8080/enforce \
  -H "Content-Type: application/json" \
  -d '{"data_type":"PHI","encrypted":false,"access_logged":true,"retention_days":1200}' | jq

Submit a compliant healthcare request:

curl -s -X POST http://localhost:8080/enforce \
  -H "Content-Type: application/json" \
  -d '{"data_type":"PHI","encrypted":true,"access_logged":true,"retention_days":1200}' | jq

Run dynamic profile switching verification:

./verify_switching.sh

Run full policy enforcement verification:

./verify_policy_gate.sh

Run the Python test client:

python3 test_client.py

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Verify service health |
| GET | /profiles | List available policy profiles |
| GET | /status | Show active profile and enabled rules |
| POST | /switch-profile | Dynamically switch active policy profile |
| POST | /enforce | Enforce active profile rules against request data |

## Policy Profiles

| Profile | Industry Context | Key Rules |
|---|---|---|
| Healthcare | HIPAA-style protected health information controls | Data encryption, access logging, data retention |
| Finance | PCI-DSS-style cardholder data controls | Data encryption, network segmentation, access control |
| Retail | General commerce customer data controls | Data encryption, rate limiting |

## Tools Used

- Python 3
- PyYAML
- requests
- http.server
- YAML
- JSON
- curl
- jq
- Bash
- Linux

## Key Skills Demonstrated

- Policy-as-code implementation
- Dynamic policy profile switching
- REST API development
- YAML-driven configuration management
- Compliance rule modeling
- Multi-tenant enforcement patterns
- DevSecOps control automation
- Runtime governance enforcement
- JSON API testing
- Defensive request validation
- Platform engineering workflow design

## Real-World Use Case

A SaaS platform may serve healthcare, finance, and retail customers through the same core application, but each customer type may require different compliance behavior. A multi-profile policy gate allows the platform to switch enforcement rules dynamically based on the active tenant or workload context. This reduces duplicated infrastructure while preserving compliance boundaries and centralized governance.

## Lessons Learned

- Configuration-driven policy profiles make enforcement behavior easier to change without modifying core code.
- Runtime profile switching is useful for multi-tenant systems with different regulatory contexts.
- API-based policy gates are easier to integrate into microservices, CI/CD systems, and internal platforms.
- Rule evaluation should return clear violation details so downstream systems can explain why a request was blocked.
- Profile state should be persisted so the service can restore the active policy context after restart.

## Troubleshooting Log

Issue:
pip3 was missing from the Ubuntu environment.

Resolution:
Installed python3-pip before creating the Python virtual environment.

Issue:
The starter files contained TODO placeholders instead of working logic.

Resolution:
Implemented the complete policy engine, configuration manager, API gateway, and test client.

Issue:
The requests package was required by the test client but not installed by the original setup.

Resolution:
Installed requests inside the virtual environment.

Issue:
The API server could remain running in the background after verification.

Resolution:
Stored the process ID in logs/api_gateway.pid and stopped it before preparing the repository.

Issue:
Python cache and virtual environment directories were generated during execution.

Resolution:
Removed __pycache__ and venv before GitHub push and added .gitignore rules.
