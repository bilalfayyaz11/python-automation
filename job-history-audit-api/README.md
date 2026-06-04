cat > README.md << 'EOF'

# Queryable Job History Audit API

## What This Does

This service provides a REST API for storing, querying, filtering, and auditing job execution history. It enables engineering teams to track automation activity, deployment events, scheduled operations, and operational workflows through a centralized API.

The implementation supports filtering by status, user, environment, and job name while exposing execution statistics for operational visibility. Comprehensive automated tests ensure API reliability and regression protection.

This pattern is commonly used in CI/CD platforms, DevOps automation systems, platform engineering tooling, and compliance reporting environments where auditability is critical.

## Architecture

+----------------------+
|      API Client      |
| curl / scripts / UI  |
+----------+-----------+
|
v
+----------------------+
|      Flask API       |
|   Route Handlers     |
+----------+-----------+
|
v
+----------------------+
| SQLAlchemy ORM Layer |
+----------+-----------+
|
v
+----------------------+
|    SQLite Database   |
|   Job History Data   |
+----------+-----------+
|
v
+----------------------+
|   Audit & Analytics  |
| Filtering / Stats    |
+----------------------+

## Prerequisites

* Python 3.12+
* pip
* virtualenv
* Git
* Linux environment (Ubuntu, Debian, RHEL, Rocky, CentOS)
* Network access to install Python packages

## Setup & Installation

```bash
python3 -m venv venv
source venv/bin/activate

pip install flask flask-sqlalchemy pytest pytest-flask pytest-cov requests
```

## How to Reproduce

Clone repository:

```bash
git clone https://github.com/bilalfayyaz11/python-automation.git
cd python-automation/job-history-audit-api
```

Create environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Populate database:

```bash
python3 populate_data.py
```

Start API:

```bash
python3 run.py
```

Run tests:

```bash
pytest tests/ -v
```

Generate coverage report:

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## Tools Used

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* Pytest
* Pytest-Flask
* Pytest-Cov
* REST API
* Git
* Linux

## Key Skills Demonstrated

* REST API design and implementation
* Database modeling with SQLAlchemy
* Application factory architecture
* API filtering and query handling
* CRUD endpoint development
* Automated testing strategy
* Test-driven validation
* Audit trail implementation
* Operational monitoring foundations
* Backend troubleshooting and debugging

## Real-World Use Case

Organizations running CI/CD pipelines, scheduled maintenance jobs, infrastructure automation, backup systems, and deployment workflows require a historical record of every execution. This API provides a searchable audit trail that allows operations teams to investigate failures, verify successful deployments, analyze execution patterns, and satisfy compliance requirements.

## Lessons Learned

* API filtering becomes significantly easier when query construction is modular.
* Automated tests rapidly identify regressions during feature additions.
* Audit data models should be designed before endpoint implementation.
* Statistics endpoints provide operational visibility with minimal complexity.
* Application factory patterns simplify testing and configuration management.

## Troubleshooting Log

* Implemented missing model serialization logic.
* Added database initialization inside Flask application factory.
* Registered Blueprint routes to prevent endpoint discovery failures.
* Implemented CRUD operations for job history records.
* Added dynamic filtering by status, environment, user, and job name.
* Implemented statistics aggregation queries.
* Created automated database seeding functionality.
* Added comprehensive API test coverage.
* Installed missing pip dependency on Ubuntu 24.04 environment.
  EOF

