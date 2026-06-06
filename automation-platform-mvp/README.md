# Automation Platform MVP

## What This Does

This implementation provides a functional automation platform MVP with a REST API, CLI client, policy engine, Redis message broker, and Celery worker system.

The platform accepts automation requests, validates them against centralized policy rules, queues approved tasks for asynchronous execution, processes them in background workers, and stores task status in Redis.

It supports backup, deploy, and cleanup automation workflows through both HTTP API and command-line interfaces.

This architecture demonstrates the foundation of a real internal developer platform, DevOps automation service, or AIOps orchestration layer.

## Architecture

    +-----------------------------+
    | User / Operator             |
    | CLI or API Request          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | CLI Client                  |
    | cli/automation_cli.py       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Flask REST API              |
    | api/automation_api.py       |
    | /health                     |
    | /api/tasks                  |
    | /api/tasks/<task_id>        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Policy Engine               |
    | policies/policy_engine.py   |
    | Task Type Validation        |
    | Required Field Validation   |
    | Timeout Policy Enforcement  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Redis                       |
    | Broker + Task Metadata      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Celery Worker               |
    | workers/task_worker.py      |
    | Backup / Deploy / Cleanup   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Logs and Task Results       |
    | logs/api_events.log         |
    | logs/worker_events.log      |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python venv
- Python pip
- Redis Server
- curl
- jq
- Git
- Bash

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv redis-server curl jq git

sudo systemctl enable redis-server

sudo systemctl restart redis-server

redis-cli ping

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install flask redis celery click pyyaml requests

## How to Reproduce

Start the platform:

./start_platform.sh

Verify Redis:

redis-cli ping

Verify API health:

curl -s http://localhost:5000/health | jq

Submit a backup task:

python3 cli/automation_cli.py submit \
  --type backup \
  --params '{"path": "/data", "destination": "/backup"}' \
  --priority high

Submit a deploy task:

curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type": "deploy", "parameters": {"service": "web-app", "version": "1.2.3"}, "priority": "high"}' | jq

Submit cleanup tasks:

for i in {1..3}; do
  python3 cli/automation_cli.py submit \
    --type cleanup \
    --params "{\"target\": \"temp-$i\"}" \
    --priority low
done

List all tasks:

python3 cli/automation_cli.py list

Check completed tasks:

python3 cli/automation_cli.py list --status completed

Check Redis task records:

redis-cli KEYS "task:*"

Review worker execution logs:

cat logs/worker_events.log

Stop the platform:

./stop_platform.sh

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Check API and Redis connectivity |
| POST | /api/tasks | Submit a new automation task |
| GET | /api/tasks/<task_id> | Retrieve task status and result |
| GET | /api/tasks | List tasks with optional filters |

## Supported Task Types

| Task Type | Required Parameters | Purpose |
|---|---|---|
| backup | path, destination | Simulates backup automation |
| deploy | service, version | Simulates deployment automation |
| cleanup | target | Simulates cleanup automation |

## Tools Used

- Python 3
- Flask
- Redis
- Celery
- Click
- PyYAML
- requests
- Bash
- curl
- jq
- Linux systemd

## Key Skills Demonstrated

- REST API development
- CLI tooling
- Redis-backed task queues
- Celery worker orchestration
- Asynchronous background processing
- Policy-based task validation
- Automation workflow design
- Task lifecycle tracking
- Distributed component integration
- Platform engineering architecture
- DevOps automation patterns
- Operational logging

## Real-World Use Case

Internal platform teams often need a controlled way to expose automation workflows to engineers and operators. This platform demonstrates how requests can enter through an API or CLI, pass through centralized policy validation, move into an asynchronous execution queue, and then be processed by background workers while status remains queryable. The same pattern is used in deployment platforms, backup orchestration tools, infrastructure automation systems, and AIOps remediation workflows.

## Lessons Learned

- Redis provides a lightweight and effective broker for asynchronous automation workflows.
- Policy engines centralize validation and prevent unsafe or malformed tasks from reaching workers.
- Separating API, CLI, worker, and policy components makes the platform easier to extend.
- Persistent task metadata makes automation workflows observable and easier to troubleshoot.
- Startup and shutdown scripts improve operational control during local platform testing.

## Troubleshooting Log

Issue:
pip3 was missing from the Ubuntu environment.

Resolution:
Installed python3-pip before creating the virtual environment.

Issue:
Redis was not installed in the fresh environment.

Resolution:
Installed redis-server, enabled the service, restarted it, and verified connectivity with redis-cli ping.

Issue:
The starter implementation contained TODO placeholders for the policy engine, API, CLI, and worker.

Resolution:
Implemented all core components fully with validation, task queuing, status tracking, and worker execution.

Issue:
The original workflow referenced Celery logs but did not configure log output.

Resolution:
Redirected API and worker process output into logs/api.log and logs/celery.log.

Issue:
Background services needed controlled shutdown before GitHub preparation.

Resolution:
Created stop_platform.sh and removed active PID files from the repository.

Issue:
Python cache and virtual environment files were generated during execution.

Resolution:
Removed venv and __pycache__ before GitHub push and added .gitignore rules.
