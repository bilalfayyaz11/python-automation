# Asynchronous Job Worker Service

## What This Does

This implementation provides a Python-based asynchronous job execution system using a Flask REST API, SQLite-backed job queue, and a polling worker service.

The API stores job requests, exposes job lifecycle endpoints, and allows external systems to create and track automation work. The worker continuously fetches pending jobs, executes backup, cleanup, and reporting operations, then updates each job with success or failure results.

This architecture mirrors how production platforms handle background automation outside the main request-response lifecycle.

## Architecture

```
+----------------------+
| External Client      |
| curl / API Consumer  |
+----------+-----------+
           |
           v
+----------------------+
| Flask REST API       |
| /jobs                |
| /jobs/{id}           |
| /jobs/{id}/status    |
+----------+-----------+
           |
           v
+----------------------+
| SQLite Job Queue     |
| pending              |
| processing           |
| completed            |
| failed               |
+----------+-----------+
           |
           v
+----------------------+
| Worker Service       |
| Polling Engine       |
| Job Executor         |
+----------+-----------+
           |
  +--------+--------+
  |        |        |
  v        v        v
```

Backup   Cleanup   Report

## Prerequisites

* Ubuntu Linux
* Python 3.12+
* python3-pip
* python3-venv
* SQLite3
* curl
* Git

## Setup & Installation

sudo apt update

sudo apt install -y 
python3 
python3-pip 
python3-venv 
sqlite3 
curl 
git

python3 -m venv venv

source venv/bin/activate

pip install flask requests

## How to Reproduce

Create the database:

sqlite3 jobs.db

Create the API:

python3 api_server.py

Verify API:

curl http://localhost:5000/jobs

Start worker:

python3 worker_service.py

Create additional jobs:

curl -X POST http://localhost:5000/jobs

Verify completion:

sqlite3 jobs.db "SELECT id, job_type, status FROM jobs;"

## Tools Used

* Python
* Flask
* Requests
* SQLite
* Linux
* Bash
* REST APIs
* tar
* curl

## Key Skills Demonstrated

* REST API development
* Background worker implementation
* Asynchronous processing patterns
* Job queue architecture
* SQLite integration
* API-driven automation
* Linux systems automation
* Error handling and recovery
* Service orchestration
* Production troubleshooting

## Real-World Use Case

This pattern is widely used in DevOps platforms, CI/CD systems, infrastructure automation tools, monitoring platforms, backup orchestration systems, compliance scanning pipelines, and internal platform engineering services.

Rather than executing long-running operations directly inside a web request, jobs are placed into a queue and processed independently by worker services. This improves reliability, scalability, and user experience.

## Lessons Learned

* Background workers should never block API requests.
* Job state transitions make troubleshooting significantly easier.
* Permission issues are common in automation workflows.
* Directory backups require different handling than file backups.
* Non-zero exit codes do not always indicate true failure.
* Worker services should be resilient to transient errors.

## Troubleshooting Log

Issue:
Backup job failed because destination path was /backup.

Cause:
Normal Linux users cannot write to root-owned directories.

Resolution:
Changed destination path to /tmp/backup.

Issue:
Backup worker initially only handled files.

Cause:
Seeded job attempted to archive /var/log which is a directory.

Resolution:
Added directory archive support using tar.

Issue:
Archive was created successfully but worker still marked job failed.

Cause:
tar returned a warning exit code.

Resolution:
Validated archive existence instead of relying solely on subprocess check=True.

Issue:
Jobs remained in failed state during testing.

Cause:
Worker correctly records failed jobs and does not automatically retry.

Resolution:
Reset status back to pending and reprocessed successfully.

EOF
