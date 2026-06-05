# Structured Logging and Correlation ID Traceability

## What This Does

This implementation builds two Python microservices with structured JSON logging and correlation ID propagation across service boundaries.

Each incoming request receives a correlation ID, either from the request header or from a generated UUID. That same ID is passed from the main order service to the downstream inventory service, allowing engineers to trace the full request lifecycle across multiple services.

The system also includes a log analysis utility that groups log entries by correlation ID, making debugging faster and more reliable in distributed environments.

## Architecture

+------------------------------------------------------+
|                    Client Request                    |
|        X-Correlation-ID header or auto UUID          |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|              Service A: Order API                    |
|                  Flask on Port 5000                  |
|                                                      |
|  /api/users                                          |
|  /api/orders                                         |
|  /api/orders/full                                    |
+------------------------------------------------------+
                          |
                          | Propagates X-Correlation-ID
                          v
+------------------------------------------------------+
|            Service B: Inventory API                  |
|                  Flask on Port 5001                  |
|                                                      |
|  /api/inventory/check                                |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|              Structured JSON Logs                    |
|                                                      |
|  service_a.log                                       |
|  service_b.log                                       |
|  correlation_id                                      |
|  timestamp                                           |
|  log level                                           |
|  service name                                        |
|  message                                             |
+------------------------------------------------------+
                          |
                          v
+------------------------------------------------------+
|              Log Analysis Utility                    |
|        Groups request flow by correlation ID         |
+------------------------------------------------------+

## Prerequisites

- Ubuntu Linux
- Python 3.12+
- python3-pip
- python3-venv
- Flask
- python-json-logger
- requests
- curl
- Git

## Setup & Installation

sudo apt update
sudo apt install -y python3 python3-pip python3-venv git curl

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install flask python-json-logger requests

## How to Reproduce

git clone <repository-url>
cd structured-logging-correlation

python3 -m venv venv
source venv/bin/activate

pip install flask python-json-logger requests

python app.py > service_a.log 2>&1 &
python service_b.py > service_b.log 2>&1 &

sleep 3

curl http://localhost:5000/api/users

curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"amount":99.99}'

curl -X POST http://localhost:5000/api/orders/full \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID:test-12345" \
  -d '{"product_id":"prod-001","user_id":1}'

python analyze_logs.py service_a.log
python analyze_logs.py service_b.log

## Tools Used

- Python
- Flask
- python-json-logger
- requests
- JSON logging
- HTTP APIs
- Bash
- curl
- Linux process management

## Key Skills Demonstrated

- Structured application logging using JSON format
- Correlation ID generation and propagation
- Distributed request tracing across services
- Microservice observability fundamentals
- API request validation and error handling
- Log analysis and debugging workflows
- Python service development
- Production-style troubleshooting patterns

## Real-World Use Case

In a production microservices environment, one user request may pass through multiple services such as authentication, orders, inventory, billing, and notifications. Without correlation IDs, debugging failures across these services becomes slow and painful. This implementation demonstrates how platform, DevOps, and SRE teams trace request flow end-to-end using consistent structured logs.

## Lessons Learned

- Correlation IDs make distributed debugging significantly easier.
- JSON logs are easier to parse, search, and forward into centralized logging systems.
- Request headers are a simple and effective way to propagate trace context.
- Logging must include enough context to support real incident investigation.
- Development servers are useful for validation, but production should use a proper WSGI server.

## Troubleshooting Log

Issue:
pip3 was not installed in the fresh Ubuntu environment.

Resolution:
Installed python3-pip and python3-venv before creating the virtual environment.

Issue:
Flask and python-json-logger were missing.

Resolution:
Created an isolated virtual environment and installed Flask, python-json-logger, and requests.

Issue:
The original implementation contained TODO placeholders instead of working logic.

Resolution:
Implemented complete JSON logger configuration, correlation ID middleware, contextual logging, downstream service propagation, and log analysis.

Issue:
Werkzeug framework logs may show null correlation_id.

Resolution:
Application-level logs correctly include correlation IDs. Framework startup and access logs are not part of the request context.
