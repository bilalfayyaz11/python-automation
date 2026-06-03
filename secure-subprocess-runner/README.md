# Secure Subprocess Execution Framework

## What This Does

This implementation provides a secure wrapper around Python's subprocess module for executing approved system commands safely. The framework enforces command whitelisting, blocks command injection attempts, applies execution timeouts, and records all execution activity for auditing purposes.

The solution demonstrates defensive programming techniques commonly used in automation platforms, DevSecOps tooling, orchestration systems, and operational automation frameworks.

By validating commands before execution and enforcing strict execution controls, the framework reduces the risk of unauthorized command execution and system compromise.

## Architecture

```text
+--------------------------+
|      User Request        |
+------------+-------------+
             |
             v
+--------------------------+
|   Command Validation     |
|  Whitelist Enforcement   |
+------------+-------------+
             |
             v
+--------------------------+
| Security Inspection Layer|
| Injection Detection      |
| Path Validation          |
+------------+-------------+
             |
             v
+--------------------------+
|  Safe Execution Engine   |
|  subprocess.run()        |
|  Timeout Enforcement     |
+------------+-------------+
             |
             v
+--------------------------+
| Structured Result Output |
| Logging & Audit Trail    |
+--------------------------+
```

## Prerequisites

* Ubuntu 24.04 or compatible Linux distribution
* Python 3.12+
* pip
* Python virtual environment support
* Git

## Setup & Installation

```bash
git clone <repository-url>

cd secure-subprocess-runner

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
```

## How to Reproduce

```bash
source venv/bin/activate

python3 test_runner.py

python3 examples.py

python3 verify_security.py
```

## Tools Used

* Python 3
* subprocess
* pathlib
* shlex
* logging
* virtualenv
* Linux command utilities

## Key Skills Demonstrated

* Secure subprocess execution
* Command injection prevention
* Defensive programming
* Input validation
* Whitelist-based security controls
* Timeout management
* Structured error handling
* Security logging and auditing
* Python automation engineering

## Real-World Use Case

Organizations frequently build automation systems that execute operating system commands on servers, containers, and infrastructure platforms. Without strict validation controls, these systems become vulnerable to command injection attacks. This framework provides a security layer that can be embedded into deployment platforms, orchestration systems, CI/CD tooling, infrastructure automation services, and operational control systems.

## Lessons Learned

* Command whitelisting is safer than attempting to blacklist dangerous inputs.
* Every subprocess execution should have a timeout.
* Structured return objects simplify automation workflows.
* Security logging is essential for auditability and troubleshooting.
* Input validation should occur before execution is attempted.

## Troubleshooting Log

### Command Injection Attempt

Issue:

```bash
ls; rm -rf /
```

Resolution:

Blocked by validation logic before execution.

### Pipe Injection Attempt

Issue:

```bash
echo test | grep test
```

Resolution:

Shell metacharacters are rejected during validation.

### Restricted File Access

Issue:

```bash
cat /etc/passwd
```

Resolution:

Sensitive system paths are blocked through path validation controls.

### Hanging Commands

Issue:

Long-running commands may never return.

Resolution:

Timeout enforcement terminates execution after the configured threshold.

### Verification Logic Bug

Issue:

The original timeout verification checked for the word:

```text
timeout
```

while the implementation returned:

```text
timed out
```

Resolution:

Verification updated to check for both forms of timeout messaging.
