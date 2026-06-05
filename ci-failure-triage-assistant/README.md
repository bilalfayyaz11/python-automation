# CI Failure Triage Assistant

## What This Does

This implementation provides an automated CI/CD log triage assistant that analyzes failed pipeline logs, detects known failure patterns, ranks likely root causes, and suggests actionable remediation steps.

The system uses a YAML-based pattern database to identify common CI failures such as dependency download failures, test assertion failures, compilation errors, Docker build failures, and resource exhaustion. It supports both single-log analysis and batch processing across multiple pipeline logs.

This type of automation helps DevOps, SRE, Platform Engineering, Release Engineering, and AIOps teams reduce the time spent manually reading CI logs and speed up build failure diagnosis.

## Architecture

    +-----------------------------+
    | CI/CD Failure Logs          |
    | logs/*.log                  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Pattern Database            |
    | patterns/failure_patterns   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | CI Triage Engine            |
    | ci_triage.py                |
    | Keyword Matching            |
    | Confidence Scoring          |
    | Error Context Extraction    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Batch Analysis Layer        |
    | batch_triage.py             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Triage Reports              |
    | output/*.txt                |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/ci-triage-lab

cd ~/ci-triage-lab

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pyyaml colorama

## How to Reproduce

Analyze a single CI log:

source venv/bin/activate

python3 ci_triage.py logs/build_failure_1.log

python3 ci_triage.py logs/test_failure_2.log

python3 ci_triage.py logs/compile_error_3.log

python3 ci_triage.py logs/docker_failure_4.log

Run batch analysis:

python3 batch_triage.py logs

Verify generated reports:

ls -lh output

Review report content:

cat output/batch_summary.txt

## Failure Patterns Supported

- Network or dependency download failure
- Test assertion failure
- Compilation failure
- Memory or resource exhaustion
- Docker build failure

## Tools Used

- Python 3
- PyYAML
- Colorama
- YAML
- Bash
- Linux
- Git
- tree

## Key Skills Demonstrated

- CI/CD troubleshooting automation
- Log parsing
- Pattern matching
- YAML-driven configuration
- Failure classification
- Confidence scoring
- Error context extraction
- Batch processing
- DevOps workflow automation
- Release engineering diagnostics
- SRE support tooling
- AIOps-style triage automation

## Real-World Use Case

Engineering teams often spend significant time reading failed CI/CD logs to identify whether a build failed because of dependency downloads, test regressions, compilation errors, Docker registry issues, or resource exhaustion. This tool automates the first-pass investigation by identifying likely failure categories and producing structured reports with suggested next actions.

In a production engineering organization, this type of assistant could be integrated into GitHub Actions, GitLab CI, Jenkins, Buildkite, CircleCI, or internal developer platforms to summarize failures automatically and reduce mean time to diagnosis.

## Lessons Learned

- Generic keywords such as error can create noisy false positives.
- Pattern databases need carefully selected keywords to improve triage accuracy.
- YAML is useful for making failure rules editable without changing Python code.
- Batch analysis helps identify repeated failure trends across many CI logs.
- Automated triage does not replace engineers, but it reduces the time needed to reach the right investigation path.

## Troubleshooting Log

Issue:
Global pip installation can fail on Ubuntu 24.04 due to externally managed Python environments.

Resolution:
Created and used a Python virtual environment before installing PyYAML and Colorama.

Issue:
tree was missing from the fresh Ubuntu environment.

Resolution:
Installed tree through apt.

Issue:
Compilation pattern initially matched unrelated logs because the keyword error: was too generic.

Resolution:
Replaced broad matching with more specific compilation indicators such as cannot find symbol, Compilation failed, symbol:, and location:.

Issue:
Docker failures were not detected by the default pattern database.

Resolution:
Added a custom Docker Build Failure pattern with registry and image-pull related keywords.

Issue:
Batch reports needed persistent output artifacts.

Resolution:
Added output report generation for individual logs and a batch summary file.
