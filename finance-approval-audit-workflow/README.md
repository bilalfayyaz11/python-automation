# Finance Approval Audit Workflow

## What This Does

This implementation provides a configurable finance approval workflow that enforces approval gates for budget-sensitive operational requests.

The system uses YAML-based approval rules to decide whether a request should be auto-approved or routed through a multi-approver control process. It persists request state, records approval decisions, rejects unauthorized approvers, and writes compliance-focused audit events in JSONL format.

This type of workflow is useful for teams that need financial governance before cloud deployments, infrastructure provisioning, procurement actions, or high-cost operational changes are allowed to proceed.

## Architecture

    +-----------------------------+
    | Finance Request CLI         |
    | workflows/approval_cli.py   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Approval Rule Configuration |
    | config/approval_rules.yaml  |
    | Thresholds + Approvers      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Approval Engine             |
    | workflows/approval_engine.py|
    | Gate Selection              |
    | Authorization Checks        |
    | State Persistence           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Audit Logging Layer         |
    | workflows/audit_logger.py   |
    | JSONL Event Records         |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Audit Query Interface       |
    | workflows/audit_query.py    |
    | Filtering + Reports         |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Compliance Artifacts        |
    | approval_state.json         |
    | logs/audit.log              |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3.12
- Python pip
- Python virtual environments
- Git
- tree
- PyYAML
- GitPython
- Bash shell access

## Setup & Installation

sudo apt update

sudo apt install -y python3-pip python3-venv git tree

mkdir -p ~/finance-approval-lab

cd ~/finance-approval-lab

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install pyyaml gitpython

## How to Reproduce

Activate the Python environment:

source ~/finance-approval-lab/venv/bin/activate

Move into the workflow directory:

cd ~/finance-approval-lab/approval-system

Validate the YAML policy configuration:

python3 -c "import yaml; yaml.safe_load(open('config/approval_rules.yaml')); print('YAML configuration valid')"

Create a request that requires approval:

python3 workflows/approval_cli.py request \
  --request-id REQ001 \
  --amount 2000 \
  --requester dev_user \
  --description "Infrastructure deployment"

Check request status:

python3 workflows/approval_cli.py status --request-id REQ001

Record the first approval:

python3 workflows/approval_cli.py approve \
  --request-id REQ001 \
  --approver finance_manager

Record the second approval:

python3 workflows/approval_cli.py approve \
  --request-id REQ001 \
  --approver team_lead

Review final request status:

python3 workflows/approval_cli.py status --request-id REQ001

Query audit events:

python3 workflows/audit_query.py --days 1

Generate audit summary report:

python3 workflows/audit_query.py --report --days 7

Run the complete validation script:

./test_approval_flow.sh

Inspect generated state and audit files:

python3 -m json.tool approval_state.json

cat logs/audit.log

tree ~/finance-approval-lab/approval-system

## Tools Used

- Python 3.12
- PyYAML
- GitPython
- argparse
- JSON
- JSONL
- YAML
- Bash
- Git
- Linux
- tree

## Key Skills Demonstrated

- Approval workflow automation
- YAML-driven governance policy configuration
- Financial control gate implementation
- Threshold-based authorization logic
- Multi-approver workflow design
- Persistent state management
- JSONL audit logging
- Compliance evidence generation
- CLI tool development
- DevOps governance automation
- FinOps control workflow design
- Regulated-environment operational controls

## Real-World Use Case

Cloud and platform teams often need approval controls before executing cost-impacting actions such as provisioning large infrastructure, increasing service capacity, deploying paid resources, or approving procurement-related operational changes. This workflow demonstrates how a company can enforce financial approval rules automatically, preserve decision history, and generate audit evidence for compliance reviews. It can be adapted into CI/CD pipelines, infrastructure-as-code workflows, internal developer platforms, or FinOps governance systems.

## Lessons Learned

- Approval systems need persistent state so requests and decisions survive beyond a single command execution.
- YAML is effective for managing policy rules because finance and engineering teams can review thresholds and approver lists clearly.
- JSONL audit logs are better than plain JSON arrays for append-only compliance logging.
- Authorization checks must reject unauthorized approvers and record that rejection for investigation.
- Generated Python cache files should be excluded from portfolio repositories because they are runtime artifacts, not source code.

## Troubleshooting Log

Issue:
The original setup used global pip installation, which can fail on Ubuntu 24.04 due to externally managed Python environments.

Resolution:
Created a Python virtual environment and installed PyYAML and GitPython inside the isolated environment.

Issue:
The original implementation files contained TODO placeholders and could not run as written.

Resolution:
Implemented the approval engine, audit logger, CLI interface, audit query tool, state persistence, and validation script.

Issue:
The lab suggested formatting audit logs with python3 -m json.tool, but append-only audit logs contain multiple JSON records and are not one valid JSON document.

Resolution:
Used JSONL format for audit logging and created an audit query tool to parse and report events cleanly.

Issue:
Python generated __pycache__ files during script execution.

Resolution:
Added a .gitignore file and removed generated cache files from Git tracking.

Issue:
Approval state needed safe updates during request and approval operations.

Resolution:
Implemented atomic state writes using a temporary file and os.replace.
