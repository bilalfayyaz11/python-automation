# Resilient HTTP Client Library

## What This Does

This implementation builds a production-ready HTTP client wrapper for Python applications that need reliable communication with external APIs and services. It adds retry logic, exponential backoff, timeout enforcement, retryable HTTP status handling, and optional circuit breaker protection.

The client is designed for environments where network failures, temporary service outages, rate limits, DNS issues, and slow responses are expected. Instead of failing immediately, it retries safely, waits progressively longer between attempts, and prevents repeated calls to unhealthy services through circuit breaker protection.

## Architecture

```text
+--------------------------------------------------+
|              Python Application                  |
+----------------------+---------------------------+
                       |
                       v
+--------------------------------------------------+
|          Resilient HTTP Client Library            |
|  GET | POST | Timeout | Retry Classification      |
+----------------------+---------------------------+
                       |
        +--------------+--------------+
        |                             |
        v                             v
+----------------------+      +----------------------+
| Exponential Backoff  |      | Circuit Breaker      |
| 1s -> 2s -> 4s       |      | CLOSED / OPEN / HALF |
+----------------------+      +----------------------+
        |                             |
        +--------------+--------------+
                       |
                       v
+--------------------------------------------------+
|              External HTTP Service                |
| APIs | Microservices | Cloud Endpoints            |
+--------------------------------------------------+
```

## Prerequisites

* Ubuntu 24.04 or compatible Linux distribution
* Python 3.12+
* python3-pip
* python3-venv
* Git
* Internet access
* Basic understanding of HTTP, REST APIs, exceptions, and Python classes

## Setup & Installation

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git tree curl dnsutils

mkdir -p ~/resilient-http-client
cd ~/resilient-http-client

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install requests
```

## How to Reproduce

```bash
git clone https://github.com/bilalfayyaz11/python-automation.git
cd python-automation/resilient-http-client

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install requests

python verify.py
python test_client.py
python test_advanced.py
```

## Tools Used

* Python 3.12
* Requests
* Git
* Virtual Environments
* HTTPBin
* Circuit Breaker Pattern
* Exponential Backoff
* Timeout Handling

## Key Skills Demonstrated

* Resilient API client design
* Retry logic implementation
* Exponential backoff strategy
* Timeout enforcement
* HTTP error classification
* Circuit breaker implementation
* Session-based HTTP communication
* Production-style exception handling
* Distributed systems reliability patterns
* Cloud automation support patterns

## Real-World Use Case

This client pattern is used in microservices, DevOps automation, monitoring tools, cloud infrastructure scripts, CI/CD systems, and API integrations where network reliability cannot be guaranteed. Instead of allowing temporary service failures to break automation immediately, the client applies controlled retries, backoff delays, and circuit breaker protection to improve stability and prevent cascading failures.

## Lessons Learned

* Network failures are normal and must be handled intentionally.
* Exponential backoff prevents repeated requests from overwhelming struggling services.
* Timeout settings are essential because network calls should never wait forever.
* Circuit breakers protect systems by stopping repeated calls to unhealthy dependencies.
* POST retries require extra care because repeated requests may create duplicate actions.

## Troubleshooting Log

### Ubuntu 24.04 Python Package Management

Issue:

Direct package installation with `pip3 install requests` can conflict with Ubuntu externally managed Python behavior.

Fix:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

### Import Errors

Issue:

Python cannot import `resilient_client` or `circuit_breaker`.

Fix:

Run commands from the project root:

```bash
cd ~/resilient-http-client
source .venv/bin/activate
python verify.py
```

### Network Timeout Issues

Issue:

Requests timeout too quickly or fail due to slow network response.

Fix:

Increase timeout when creating the client:

```python
client = ResilientHTTPClient(max_retries=3, base_timeout=10)
```

### Circuit Breaker Not Opening

Issue:

Circuit breaker does not transition to OPEN.

Fix:

Reduce retry count and repeatedly call a failing endpoint until the failure threshold is reached.

```python
client = ResilientHTTPClient(
    max_retries=1,
    base_timeout=1,
    use_circuit_breaker=True,
)
```

### Exponential Backoff Verification

Expected backoff sequence:

```text
Attempt 0: 1.0s
Attempt 1: 2.0s
Attempt 2: 4.0s
Attempt 3: 8.0s
```
