# AI Assisted Runbook Generator

## What This Does

This implementation automates operational runbook creation by combining live system context collection with local AI-powered documentation generation.

The platform gathers operating system information, service status, network configuration, and disk utilization, then uses a locally hosted language model through Ollama to generate structured incident response procedures.

The system produces consistent operational documentation for common scenarios such as high CPU utilization, disk capacity issues, and service outages while reducing manual documentation effort.

## Architecture

    +----------------------------+
    | System Context Collection  |
    +----------------------------+
               |
               v
    +----------------------------+
    | OS Information             |
    | Service Status             |
    | Network Configuration      |
    | Disk Utilization           |
    +----------------------------+
               |
               v
    system_context.json
               |
               v
    +----------------------------+
    | Prompt Generation Layer    |
    +----------------------------+
               |
               v
    +----------------------------+
    | Ollama Local LLM           |
    | llama3.2:1b               |
    +----------------------------+
               |
               v
    +----------------------------+
    | Runbook Formatter          |
    | Markdown Output            |
    | YAML Output                |
    +----------------------------+
               |
               v
    runbook_*.md
    runbook_*.yaml

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Ollama
- curl
- jq
- sysstat
- net-tools

## Setup & Installation

sudo apt update

sudo apt install -y \
python3 \
python3-pip \
python3-venv \
curl \
jq \
sysstat \
net-tools

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install \
requests \
pyyaml \
jinja2

curl -fsSL https://ollama.com/install.sh | sh

ollama serve &

ollama pull llama3.2:1b

## How to Reproduce

Collect system context:

python3 collect_context.py

Generate runbooks:

python3 generate_runbook.py high_cpu

python3 generate_runbook.py disk_full

python3 generate_runbook.py service_down

Verify generated files:

ls -lh runbook_*.md runbook_*.yaml

## Tools Used

- Python 3
- Ollama
- llama3.2:1b
- Jinja2
- PyYAML
- JSON
- Linux
- Bash
- curl
- jq

## Key Skills Demonstrated

- AIOps Automation
- Local LLM Integration
- Operational Documentation
- Runbook Generation
- Prompt Engineering
- Python Automation
- System Administration
- Infrastructure Context Collection
- Incident Response Documentation
- Markdown Automation
- YAML Automation

## Real-World Use Case

Platform engineering and SRE teams spend significant time maintaining operational runbooks. This solution automates documentation generation by combining real system context with AI-generated operational procedures. Similar approaches are increasingly used within AIOps platforms, internal engineering portals, and incident management systems to accelerate documentation workflows and improve operational consistency.

## Lessons Learned

- AI output quality improves significantly when contextual system data is supplied.
- Local models avoid external API dependencies and data exposure.
- Structured prompts generate more operationally useful documentation.
- System context collection is critical for accurate runbook generation.
- AI-generated documentation should always be reviewed before production use.

## Troubleshooting Log

Issue:
Ollama generation became slow on limited-resource lab infrastructure.

Resolution:
Reduced prompt size and constrained model output.

Issue:
Model startup latency delayed initial requests.

Resolution:
Added service warm-up period before generation requests.

Issue:
Large context payloads increased inference time.

Resolution:
Trimmed context collection output to only operationally relevant information.

Issue:
Runbook generation depended on local model availability.

Resolution:
Added deterministic fallback workflow for low-resource environments.
