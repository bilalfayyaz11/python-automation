# Retail Deployment Safety and Automated Rollback Platform

## What This Does

This implementation provides a deployment safety platform for customer-facing retail applications. It builds a Flask-based retail API, packages it with Docker, deploys new versions through health and readiness gates, and automatically prevents faulty versions from reaching production.

The system validates candidate releases before promotion, checks application health, confirms readiness, and preserves rollback capability if a deployment fails. This pattern reduces release risk and protects revenue-generating systems from broken deployments.

This type of deployment gate is commonly used by DevOps, SRE, Platform Engineering, and Release Engineering teams to protect production environments.

## Architecture

    +-----------------------------+
    | Retail Application Source   |
    | Flask API                   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Docker Image Build          |
    | retail-app:1.0.0            |
    | retail-app:2.0.0            |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Candidate Deployment        |
    | Port 5001                   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Deployment Gates            |
    | /health Check               |
    | /ready Check                |
    +-------------+---------------+
                  |
          +-------+-------+
          |               |
          v               v
    +------------+   +----------------+
    | Promote to |   | Rollback /     |
    | Production |   | Reject Release |
    | Port 5000  |   | Failed Version |
    +------------+   +----------------+
          |
          v
    +-----------------------------+
    | Production Retail API       |
    | Customer-Facing Service     |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04 LTS
- Docker
- Python 3
- Python virtual environments
- pip
- Git
- curl
- tree
- lsof

## Setup & Installation

sudo apt update

sudo apt install -y docker.io python3-pip python3-venv git curl tree lsof

sudo systemctl enable docker

sudo systemctl start docker

sudo usermod -aG docker $USER

newgrp docker

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install flask requests pyyaml

## How to Reproduce

Build the healthy retail image:

cd app

docker build -t retail-app:1.0.0 .

cd ..

Build the faulty retail image:

cd app

docker build -t retail-app:2.0.0 -f - . <<DOCKERFILE
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask requests
COPY retail_app_faulty.py retail_app.py
ENV APP_VERSION=2.0.0
EXPOSE 5000
CMD ["python", "retail_app.py"]
DOCKERFILE

cd ..

Deploy healthy version:

python3 deployment-scripts/deploy_with_gate.py 1.0.0

Verify production:

curl http://localhost:5000/health

curl http://localhost:5000/

Attempt faulty deployment:

python3 deployment-scripts/deploy_with_gate.py 2.0.0

Verify stable version remains active:

curl http://localhost:5000/

Inspect containers:

docker ps -a

## Tools Used

- Python 3
- Flask
- Requests
- PyYAML
- Docker
- Bash
- Linux
- curl
- Git
- Systemd

## Key Skills Demonstrated

- Deployment safety engineering
- Health-gated release automation
- Readiness validation
- Docker-based application deployment
- Automatic rollback workflows
- Release failure detection
- Production protection controls
- Python automation
- Platform engineering practices
- SRE-style reliability patterns
- CI/CD deployment logic
- Operational risk reduction

## Real-World Use Case

Retail and e-commerce systems cannot afford broken deployments because customer-facing outages directly impact revenue, checkout flow, order processing, and customer trust. This deployment safety platform demonstrates how release gates can validate a new version before production promotion and automatically reject unhealthy versions before they affect users.

## Lessons Learned

- Deployment success should never be assumed after a container starts.
- Health checks verify that the service process is alive and responding.
- Readiness checks confirm that the service is prepared to handle traffic.
- Candidate deployments reduce risk by testing new versions before production promotion.
- Rollback logic must preserve a known-good version before replacing production.

## Troubleshooting Log

Issue:
Docker was not installed in the fresh Ubuntu environment.

Resolution:
Installed Docker through apt and enabled the Docker service with systemd.

Issue:
pip3 was missing from the environment.

Resolution:
Installed python3-pip and used a Python virtual environment for dependencies.

Issue:
Global pip installation is not reliable on Ubuntu 24.04.

Resolution:
Created and activated a virtual environment before installing Flask, Requests, and PyYAML.

Issue:
The original Dockerfile used an older Python base image.

Resolution:
Updated the Docker base image to python:3.12-slim.

Issue:
The first deployment attempt failed because retail-app:1.0.0 was not built locally.

Resolution:
Rebuilt the healthy Docker image before running the deployment gate.

Issue:
The initial deployment script validated the candidate container but did not promote it to production.

Resolution:
Replaced the script with a production-grade candidate promotion workflow that validates on port 5001 and promotes the stable version to port 5000.

Issue:
A verification check returned empty because no container was listening on port 5000.

Resolution:
Confirmed container state with docker ps, redeployed version 1.0.0, and verified production health on port 5000.
