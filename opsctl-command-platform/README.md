# Operational CLI Platform with Configuration Management

## What This Does

This implementation provides a modular command-line platform for operational workflows and system administration tasks. The solution includes command routing, deployment simulation, status inspection, and persistent configuration management using a structured Python package architecture.

The platform demonstrates how operational tooling can be organized into reusable command modules while maintaining a consistent user experience through standardized argument parsing and command execution patterns.

The architecture is designed to support future expansion with additional operational commands, automation workflows, API integrations, and infrastructure management capabilities.

## Architecture

```text
+----------------------+
|      User CLI        |
|     opsctl ...       |
+----------+-----------+
           |
           v
+----------------------+
|   Argument Parser    |
|      argparse        |
+----------+-----------+
           |
           v
+----------------------+
|   Command Router     |
|      cli.py          |
+-----+--------+-------+
      |        |
      |        |
      v        v
+---------+ +---------+ +---------+
| Status  | | Deploy  | | Config  |
| Command | | Command | | Command |
+---------+ +---------+ +---------+
      |        |            |
      |        |            |
      v        v            v
+--------------------------------+
|      Helper Utilities          |
| Validation / Output Formatting |
+--------------------------------+
                 |
                 v
+--------------------------------+
| Persistent JSON Configuration  |
| ~/.opsctl/config.json          |
+--------------------------------+
```

## Prerequisites

* Ubuntu 24.04 LTS or compatible Linux distribution
* Python 3.8 or newer
* pip
* setuptools
* Git

## Setup & Installation

```bash
git clone <repository-url>

cd python-automation/opsctl-command-platform

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip setuptools wheel

pip install -e .
```

## How to Reproduce

```bash
source venv/bin/activate

opsctl --version

opsctl status

opsctl status --format json

opsctl config set api_endpoint https://api.example.com

opsctl config get api_endpoint

opsctl deploy --app webapp --env dev

opsctl deploy --app webapp --env prod --version 1.2.3
```

## Tools Used

* Python 3
* argparse
* setuptools
* virtualenv
* JSON
* Linux CLI
* Git

## Key Skills Demonstrated

* Command-line application development
* Modular Python package design
* Argument parsing and validation
* Configuration persistence
* Software packaging and distribution
* Error handling and input validation
* Reusable command architecture
* CLI user experience design

## Real-World Use Case

Organizations frequently build internal operational tooling to standardize administrative actions across environments. A platform such as this can serve as the foundation for deployment orchestration, infrastructure automation, compliance checks, operational reporting, and service management workflows while providing a consistent interface for engineers and operators.

## Lessons Learned

* Modular command separation significantly improves maintainability.
* Argument validation should occur as early as possible.
* Persistent configuration improves usability for recurring operations.
* Consistent command structures simplify future feature expansion.
* Packaging applications correctly enables easier distribution and installation.

## Troubleshooting Log

### Invalid Environment Handling

Issue:
Invalid deployment environments were supplied during testing.

Resolution:
Environment validation was enforced using argparse choices and helper validation functions.

### Missing Configuration Keys

Issue:
Users attempted to retrieve configuration values that did not exist.

Resolution:
Graceful error handling was implemented with non-zero exit codes.

### Missing Python Dependencies

Issue:
pip was not installed in the base environment.

Resolution:
Installed python3-pip and verified package installation before setup.

### Command Registration Validation

Issue:
Subcommands must be properly registered with argparse.

Resolution:
Each command module registers itself through add_parser() and set_defaults() command routing.
