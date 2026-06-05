# SQL Injection Remediation Workflow

## What This Does

This implementation demonstrates a complete secure development lifecycle workflow for identifying, reproducing, fixing, and preventing a SQL injection vulnerability.

The workflow starts with a deliberately vulnerable Flask login application, reproduces authentication bypass through SQL injection, documents the exploit impact, then implements a secure version using parameterized queries, password hashing, and input validation. It also includes regression tests and a CI-style security testing script to prevent the same vulnerability from returning.

## Architecture

    Security Test Operator
            |
            v
    +-------------------------------+
    | Vulnerable Flask Application  |
    | Port 5000                     |
    | String-Based SQL Query        |
    +-------------------------------+
            |
            v
    SQL Injection Exploit Reproduced
            |
            v
    +-------------------------------+
    | Exploit Documentation         |
    | exploit_report.md             |
    +-------------------------------+
            |
            v
    +-------------------------------+
    | Secure Flask Application      |
    | Port 5001                     |
    | Parameterized SQL Queries     |
    | SHA256 Password Hashing       |
    | Input Validation              |
    +-------------------------------+
            |
            v
    +-------------------------------+
    | Regression Testing Layer      |
    | pytest                        |
    | pytest-cov                    |
    | test-results.xml              |
    | htmlcov/                      |
    +-------------------------------+
            |
            v
    +-------------------------------+
    | Security Automation Layer     |
    | run_security_tests.sh         |
    | security_checklist.md         |
    +-------------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- SQLite3
- Git
- curl

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv sqlite3 git curl

mkdir -p ~/exploit-fix-lab

cd ~/exploit-fix-lab

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install flask pytest requests pytest-cov

## How to Reproduce

Start the vulnerable application:

source venv/bin/activate

python3 vulnerable_app.py

In another terminal, run the exploit test:

cd ~/exploit-fix-lab

source venv/bin/activate

python3 exploit_test.py

Expected result:

- Normal login succeeds.
- SQL injection payload bypasses authentication on the vulnerable application.

Start the secure application:

source venv/bin/activate

python3 secure_app.py

Run the exploit test again:

python3 exploit_test.py

Expected result:

- Normal login succeeds.
- SQL injection payload fails against the secure application.

Run the regression test suite:

pytest test_security.py -v

Run coverage:

pytest test_security.py --cov=secure_app --cov-report=html

Run CI-style security tests:

./run_security_tests.sh

## Tools Used

- Python 3
- Flask
- SQLite3
- pytest
- pytest-cov
- requests
- Bash
- curl
- Git

## Key Skills Demonstrated

- Secure Development Lifecycle workflow
- SQL injection reproduction
- Exploit documentation
- Secure code remediation
- Parameterized SQL queries
- Password hashing
- Input validation
- Security regression testing
- CI/CD-style security validation
- Test coverage generation
- Vulnerability prevention workflow

## Real-World Use Case

Application security teams, DevSecOps engineers, and backend developers use this workflow to handle real vulnerabilities reported through penetration tests, bug bounty submissions, internal audits, or production incidents. The key engineering value is not only fixing the issue once, but creating regression tests that prove the vulnerability cannot return silently in future releases.

## Lessons Learned

- SQL injection occurs when user input is directly inserted into SQL queries.
- Parameterized queries separate data from SQL logic and prevent query manipulation.
- Passwords should never be stored in plaintext.
- Input validation reduces attack surface before database access.
- Regression tests are critical because security bugs can return during future code changes.
- CI-style scripts make security validation repeatable and automation-friendly.

## Troubleshooting Log

Issue:
pip3 was missing from the fresh Ubuntu environment.

Resolution:
Installed python3-pip through apt.

Issue:
sqlite3 was missing from the fresh Ubuntu environment.

Resolution:
Installed sqlite3 through apt.

Issue:
The vulnerable application intentionally allowed SQL injection through string-formatted SQL.

Resolution:
Implemented parameterized SQL queries in the secure application.

Issue:
Passwords were stored in plaintext in the vulnerable database.

Resolution:
Stored SHA256 password hashes in the secure database.

Issue:
Exploit payloads could reach database logic directly.

Resolution:
Added username and password validation before database access.

Issue:
Security fixes needed long-term protection.

Resolution:
Created pytest regression tests and a CI-style security test script.
