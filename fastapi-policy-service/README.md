# FastAPI Status and Policy Service

## What This Does

This implementation builds a FastAPI-based operational service that exposes system health, resource status, policy rules, and request validation endpoints. It monitors CPU, memory, and disk usage, validates incoming request metadata, enforces configurable policy rules, and logs HTTP activity through middleware.

The service demonstrates how internal platform APIs can centralize health checks, policy enforcement, and operational visibility. This type of service is useful for platform engineering, DevOps automation, API gateway support, and internal control-plane tooling.

## Architecture

```text
+--------------------------------------------------+
|                 API Consumer                      |
| curl | Python Client | Internal Service           |
+----------------------+---------------------------+
                       |
                       v
+--------------------------------------------------+
|              FastAPI Application                  |
| /health | /status | /policy/check                |
| /policies | /limits                              |
+----------------------+---------------------------+
                       |
        +--------------+--------------+
        |                             |
        v                             v
+----------------------+      +----------------------+
| System Monitoring    |      | Policy Enforcement   |
| CPU | Memory | Disk  |      | Size | Method | Rate |
+----------------------+      +----------------------+
        |                             |
        +--------------+--------------+
                       |
                       v
+--------------------------------------------------+
|              Structured JSON Responses            |
| Health | Metrics | Allow/Deny Decisions           |
+--------------------------------------------------+
```

## Prerequisites

- Ubuntu 24.04 or compatible Linux distribution
- Python 3.12+
- python3-pip
- python3-venv
- Git
- curl
- jq
- FastAPI
- Uvicorn
- Pydantic
- psutil

## Setup & Installation

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git tree curl jq lsof

mkdir -p ~/fastapi-policy-service
cd ~/fastapi-policy-service

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install fastapi uvicorn pydantic psutil requests
```

## How to Reproduce

```bash
git clone https://github.com/bilalfayyaz11/python-automation.git
cd python-automation/fastapi-policy-service

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install fastapi uvicorn pydantic psutil requests

uvicorn main:app --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
curl http://localhost:8000/health | jq
curl http://localhost:8000/status | jq
curl http://localhost:8000/policies | jq
curl http://localhost:8000/limits | jq
```

Policy validation example:

```bash
curl -X POST http://localhost:8000/policy/check \
  -H "Content-Type: application/json" \
  -d '{
    "request_size": 1024,
    "method": "GET",
    "user_id": "user123",
    "request_count": 1
  }' | jq
```

## API Endpoints

| Endpoint | Method | Purpose |
|-----------|----------|----------|
| `/` | GET | Basic service health check |
| `/health` | GET | Health response with timestamp |
| `/status` | GET | CPU, memory, disk, and status metrics |
| `/policy/check` | POST | Validate request metadata against configured policies |
| `/policies` | GET | List active policy rules |
| `/limits` | GET | Show configured resource thresholds |

## Tools Used

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- psutil
- curl
- jq
- Git
- Virtual Environments

## Key Skills Demonstrated

- REST API development with FastAPI
- Pydantic request and response validation
- System resource monitoring
- Policy enforcement logic
- Middleware-based request logging
- Structured JSON API responses
- Operational health endpoint design
- Internal platform service design
- API testing with curl and jq
- Production-style service organization

## Real-World Use Case

This service pattern is used in internal platform engineering environments where teams need operational APIs for service health, policy validation, and system status visibility. Similar patterns appear in API gateways, service meshes, Kubernetes operators, internal control planes, and DevOps automation systems that need to validate requests and expose machine-readable health signals.

## Lessons Learned

- FastAPI makes it efficient to build typed operational APIs.
- Pydantic models improve request validation and response consistency.
- Middleware is useful for logging and cross-cutting request behavior.
- System metrics can be exposed safely through dedicated status endpoints.
- In-memory rate tracking works for a single-instance demo but should be replaced with Redis or another shared datastore in production.

## Troubleshooting Log

### Ubuntu 24.04 Python Package Management

Issue:

Direct global installation of Python packages can conflict with Ubuntu externally managed Python behavior.

Fix:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic psutil requests
```

### Service Port Already in Use

Issue:

FastAPI cannot start because port 8000 is already occupied.

Fix:

```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Import Errors

Issue:

Application fails because dependencies are missing.

Fix:

```bash
source .venv/bin/activate
pip install --upgrade fastapi uvicorn pydantic psutil requests
```

### System Metrics Not Displaying

Issue:

The `/status` endpoint fails or returns missing metrics.

Fix:

```bash
python3 -c "import psutil; print(psutil.cpu_percent())"
```

### API Testing

Verified endpoints:

```bash
curl http://localhost:8000/health | jq
curl http://localhost:8000/status | jq
curl http://localhost:8000/policies | jq
curl http://localhost:8000/limits | jq
```

Verified valid policy response:

```json
{
  "allowed": true,
  "reason": "Request satisfies all configured policies",
  "policy_name": "all_policies"
}
```

Verified invalid policy response:

```json
{
  "allowed": false,
  "policy_name": "max_request_size"
}
```

## Future Enhancements

- Redis-backed distributed rate limiting
- JWT authentication and authorization
- Prometheus metrics integration
- OpenTelemetry tracing
- Persistent audit logging
- Role-based access control (RBAC)
- Configuration management via environment variables
- Kubernetes deployment manifests
- Docker containerization
- CI/CD pipeline integration

## Portfolio Value

This project demonstrates practical backend engineering and platform engineering skills through API development, request validation, policy enforcement, middleware implementation, health monitoring, and operational service design. It closely resembles internal services commonly built for cloud platforms, DevOps environments, and microservice ecosystems.

