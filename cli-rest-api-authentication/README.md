# Python CLI REST API Integration and Token Authentication

## What This Does

This implementation provides a command-line interface that interacts with a REST API using Bearer token authentication. The solution performs health checks, retrieves user information, validates authentication credentials, and securely stores access tokens for future use.

The application demonstrates how Python automation tools communicate with backend services using HTTP requests while handling authentication, response parsing, and operational failures gracefully.

This pattern is commonly used when integrating with cloud provider APIs, monitoring systems, infrastructure platforms, CI/CD services, and internal engineering tools.

## Architecture

```text
+----------------------+
|     CLI Client       |
|    user_cli.py       |
+----------+-----------+
           |
           | HTTP Requests
           |
           v
+----------------------+
|      REST API        |
|    api_server.py     |
+----------+-----------+
           |
           |
           v
+----------------------+
|    User Dataset      |
|  In-Memory Storage   |
+----------------------+

Authentication Flow

CLI
 |
 | Bearer Token
 v
REST API
 |
 | Token Validation
 v
Protected Endpoints
```

## Prerequisites

* Ubuntu 24.04 or later
* Python 3.12+
* pip
* Python virtual environment support
* Git
* Network access to API endpoint

## Setup & Installation

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv

mkdir -p ~/python-api-automation
cd ~/python-api-automation

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install requests click tabulate flask flask-httpauth
```

## How to Reproduce

### Start API Server

```bash
source .venv/bin/activate
python api_server.py
```

### Test Health Endpoint

```bash
python user_cli.py health
```

### Authenticate

```bash
python user_cli.py login dev-token-12345
```

### List Users

```bash
python user_cli.py list-users
```

### Retrieve User

```bash
python user_cli.py get-user 2
```

### Check Authentication Status

```bash
python user_cli.py whoami
```

### Logout

```bash
python user_cli.py logout
```

## Tools Used

* Python 3.12
* Flask
* Flask-HTTPAuth
* Requests
* Click
* Tabulate
* Virtual Environment (venv)
* REST APIs
* JSON

## Key Skills Demonstrated

* REST API integration using Python
* Bearer token authentication
* Secure credential storage
* Command-line application development
* HTTP request handling
* JSON response parsing
* Error handling and exception management
* User-friendly output formatting
* API validation workflows

## Real-World Use Case

Engineering teams frequently build internal command-line utilities that interact with cloud platforms, Kubernetes clusters, monitoring systems, deployment pipelines, and security platforms. This implementation demonstrates the same workflow used when automating interactions with AWS APIs, Azure services, GitHub APIs, ServiceNow integrations, and enterprise operational tooling.

## Lessons Learned

* Token authentication should always be validated before storage.
* HTTP status codes must be handled explicitly for reliable automation.
* User-facing error messages significantly improve operational usability.
* Virtual environments prevent dependency conflicts.
* Structured CLI frameworks simplify future feature expansion.

## Troubleshooting Log

### Authentication Failure

Issue:
Invalid token caused API authorization failure.

Resolution:
Implemented explicit HTTP 401 detection and user-friendly error messaging.

### Missing Python Packages

Issue:
Required dependencies were unavailable in the base environment.

Resolution:
Installed requests, click, tabulate, flask, and flask-httpauth inside an isolated virtual environment.

### API Connectivity Failures

Issue:
CLI cannot operate if backend service is unavailable.

Resolution:
Added connection exception handling and graceful termination logic.

### Token Persistence

Issue:
Authentication credentials needed to persist between executions.

Resolution:
Implemented local token storage with restricted file permissions (0600).

