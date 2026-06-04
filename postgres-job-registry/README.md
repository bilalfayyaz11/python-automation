# PostgreSQL Job Registry with Python Lifecycle Management

## What This Does

This implementation provides a PostgreSQL-backed job registry for tracking automation job lifecycle events. It stores job metadata, execution status, timestamps, structured result data, and failure messages in a relational database.

The system models the same lifecycle pattern used by production schedulers, background workers, CI/CD systems, and workflow orchestration platforms.

It gives engineering teams a durable audit trail for automation activity, making it easier to monitor execution history, investigate failures, and analyze job performance over time.

## Architecture

```text
+-----------------------------+
|      Python Test Runner      |
|    test_job_registry.py      |
+--------------+--------------+
               |
               | Calls lifecycle methods
               v
+-----------------------------+
|      Job Manager Layer       |
|       job_manager.py         |
+--------------+--------------+
               |
               | SQL transactions
               v
+-----------------------------+
|        PostgreSQL            |
|      job_registry DB         |
+--------------+--------------+
               |
               | Stores
               v
+-----------------------------+
|          jobs Table          |
| status | timestamps | JSONB |
+-----------------------------+
```

## Prerequisites

* Ubuntu 24.04 or later
* PostgreSQL
* PostgreSQL contrib package
* Python 3.12+
* Python virtual environment support
* pip
* psycopg2-binary
* Git

## Setup & Installation

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib python3-pip python3-venv tree

sudo systemctl start postgresql
sudo systemctl enable postgresql

mkdir -p ~/postgres-job-registry
cd ~/postgres-job-registry

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install psycopg2-binary
```

## How to Reproduce

### Configure PostgreSQL

```bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'labpassword';"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'job_registry';" | grep -q 1 || \
sudo -u postgres createdb job_registry
```

### Apply Schema

```bash
sudo -u postgres psql -d job_registry -f schema.sql
```

### Run Lifecycle Tests

```bash
source .venv/bin/activate

chmod +x test_job_registry.py

python3 test_job_registry.py
```

### Verify Stored Records

```bash
sudo -u postgres psql -d job_registry -c "SELECT job_id, job_name, status, created_at FROM jobs ORDER BY job_id;"

sudo -u postgres psql -d job_registry -c "SELECT job_id, job_name, started_at, completed_at, ROUND(EXTRACT(EPOCH FROM (completed_at - started_at))::numeric, 2) AS duration_seconds FROM jobs WHERE status IN ('completed', 'failed') ORDER BY job_id;"

sudo -u postgres psql -d job_registry -c "SELECT job_id, job_name, result_data FROM jobs WHERE status = 'completed' ORDER BY job_id;"

sudo -u postgres psql -d job_registry -c "SELECT job_id, job_name, error_message FROM jobs WHERE status = 'failed' ORDER BY job_id;"
```

## Tools Used

* Python 3.12
* PostgreSQL
* SQL
* JSONB
* psycopg2
* Bash
* systemd
* Python virtual environments

## Key Skills Demonstrated

* PostgreSQL schema design for automation metadata
* SQL constraints for lifecycle state control
* Indexed database design for operational queries
* Python database integration using psycopg2
* Transaction handling with commit and rollback behavior
* JSONB result persistence
* Job lifecycle tracking across pending, running, completed, and failed states
* Timestamp-based duration calculation
* Failure analysis through stored error messages

## Real-World Use Case

A system like this is used inside deployment platforms, workflow engines, background job processors, ETL systems, incident automation tools, and CI/CD pipelines. Whenever an organization runs automated work, it needs a reliable way to record what ran, when it started, when it finished, whether it succeeded, what it produced, and why it failed. This implementation provides that foundation using PostgreSQL and Python.

## Lessons Learned

* Lifecycle state should be controlled using explicit status values instead of free-form text.
* JSONB is useful for storing flexible job results without redesigning the schema for every output type.
* Database transactions are necessary to avoid partially written job states.
* Indexes on status, job name, and creation time make operational queries faster.
* Duration analysis requires reliable start and completion timestamps.

## Troubleshooting Log

### Missing PostgreSQL Installation

Issue:
The environment did not include PostgreSQL or the `psql` client.

Resolution:
Installed `postgresql` and `postgresql-contrib`, then started and enabled the service with systemd.

### Missing pip

Issue:
The environment included Python but did not include `pip3`.

Resolution:
Installed `python3-pip` and used a virtual environment for Python dependency isolation.

### System Python Package Risk

Issue:
Installing Python packages globally on Ubuntu 24.04 can cause dependency conflicts.

Resolution:
Created a dedicated `.venv` and installed `psycopg2-binary` inside it.

### Incomplete SQL Schema

Issue:
The starter SQL only defined `job_id` and `job_name`, leaving core lifecycle fields as placeholders.

Resolution:
Implemented status constraints, timestamp columns, JSONB result storage, error tracking, and query indexes.

### Empty Python Manager Methods

Issue:
The starter Python class contained placeholder methods that would not insert or update job records.

Resolution:
Implemented full job lifecycle methods with SQL transactions, rollback behavior, status checks, and result retrieval.
