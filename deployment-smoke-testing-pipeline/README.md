# Automated Deployment Smoke Testing Pipeline

## What This Does

This implementation provides an automated deployment validation pipeline for web applications using health checks, API verification, response-time testing, deployment automation, reporting, and failure notification mechanisms.

The solution validates application availability immediately after deployment and prevents broken releases from progressing further in the delivery process.

The pipeline combines deployment execution, endpoint verification, performance validation, and reporting into a repeatable workflow suitable for CI/CD integration.

This approach reduces deployment risk and provides rapid operational feedback after application releases.

## Architecture

+--------------------------------------------------+
|                Deployment Pipeline               |
+--------------------------------------------------+
                      |
                      v
+--------------------------------------------------+
|                 deploy.sh                        |
|          Application Deployment Stage           |
+--------------------------------------------------+
                      |
                      v
+--------------------------------------------------+
|              Node.js Web Service                |
|                Port 3000                        |
+--------------------------------------------------+
        |                 |                 |
        v                 v                 v
   /health          /api/data        /api/status
        |                 |                 |
        +-----------------+-----------------+
                          |
                          v
+--------------------------------------------------+
|              Smoke Test Suite                    |
|  Health Check | API Check | Status Check         |
|  Response Time Validation                        |
+--------------------------------------------------+
                          |
                          v
+--------------------------------------------------+
|           Reports & Notifications                |
|   Test Reports | Pipeline Logs | Alerts          |
+--------------------------------------------------+

## Prerequisites

- Ubuntu Linux
- Git
- curl
- jq
- Node.js 22+
- npm
- bc
- lsof

## Setup & Installation

sudo apt update

curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -

sudo apt install -y nodejs git curl jq bc lsof

node --version
npm --version

## How to Reproduce

git clone <repository>

cd deployment-smoke-testing-pipeline

chmod +x deploy.sh
chmod +x pipeline_complete.sh
chmod +x tests/*.sh

./deploy.sh

curl http://localhost:3000/health

./tests/smoke_tests_complete.sh

./pipeline_complete.sh

## Tools Used

- Linux
- Bash
- Node.js
- curl
- jq
- Git
- HTTP APIs
- Process Management
- Deployment Automation

## Key Skills Demonstrated

- Deployment automation
- Smoke testing strategy
- Health check implementation
- API validation
- Post-deployment verification
- CI/CD pipeline concepts
- Failure notification handling
- Linux troubleshooting
- Service lifecycle management
- Operational reporting

## Real-World Use Case

Organizations use smoke testing pipelines immediately after deployments to verify that critical services remain operational. This reduces production incidents by detecting failures before users encounter them and provides confidence for continuous delivery practices.

## Lessons Learned

- Fast smoke tests provide rapid deployment feedback.
- Automated validation reduces manual testing effort.
- Health endpoints are essential operational controls.
- Exit codes enable integration with CI/CD systems.
- Deployment verification should occur immediately after release.

## Troubleshooting Log

Issue:
Node.js was not installed.

Resolution:
Installed Node.js 22 LTS using NodeSource repository.

Issue:
Response-time validation requires bc.

Resolution:
Verified bc installation before test execution.

Issue:
Port conflicts may prevent service startup.

Resolution:
Existing Node.js processes are terminated before deployment.

Issue:
Pipeline execution depends on executable permissions.

Resolution:
Applied chmod +x to all scripts before execution.

