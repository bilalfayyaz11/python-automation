# AI Test Suggestion Pipeline

## What This Does

This implementation provides an automated test suggestion pipeline that analyzes Python source code, extracts function metadata, estimates function complexity, and generates structured test recommendations.

The system combines Git-based change detection, Python AST parsing, function-level risk analysis, and AI-ready test recommendation logic. It supports commit-range analysis, JSON output generation, and Markdown reporting for developer review.

This type of automation helps Platform Engineering, DevOps, AIOps, QA Engineering, and Developer Experience teams identify missing test coverage earlier in the development lifecycle.

## Architecture

    +-----------------------------+
    | Python Source Repository    |
    | sample_project/             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Git Change Detection        |
    | HEAD / Commit Range         |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | AST Code Analyzer           |
    | src/code_analyzer.py        |
    | Function Extraction         |
    | Parameter Detection         |
    | Complexity Estimation       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Test Suggestion Engine      |
    | src/test_suggester.py       |
    | AI Prompt Generation        |
    | Local Model Fallback Logic  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Pipeline Orchestrator       |
    | src/pipeline.py             |
    | JSON + Markdown Output      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Test Recommendation Reports|
    | suggestions/*.json/*.md     |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3.12
- Python pip
- Python virtual environments
- Git
- GitPython
- OpenAI Python SDK
- tree
- Optional: Ollama with a local code model

## Setup & Installation

sudo apt update

sudo apt install -y python3-pip python3-venv git tree curl

mkdir -p ~/ai-test-pipeline

cd ~/ai-test-pipeline

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install openai gitpython

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Run the analyzer verification:

python3 tests/test_analyzer.py

Run the pipeline against the sample repository:

python3 src/pipeline.py --repo ./sample_project --output ./suggestions --commit-range HEAD~1..HEAD

Review generated JSON output:

python3 -m json.tool suggestions/test_suggestions.json

Review generated Markdown report:

cat suggestions/report.md

Inspect the full directory structure:

tree ~/ai-test-pipeline

## Tools Used

- Python 3.12
- Python AST
- Git
- GitPython
- argparse
- JSON
- Markdown
- Bash
- Linux
- tree
- Optional Ollama-compatible local model execution

## Key Skills Demonstrated

- Automated source code analysis
- Git commit-range inspection
- Python AST parsing
- Function metadata extraction
- Complexity estimation
- AI prompt engineering for test generation
- Fallback design for unavailable model services
- CLI pipeline development
- JSON and Markdown report generation
- Developer productivity automation
- CI/CD quality gate design
- AIOps-style engineering workflow automation

## Real-World Use Case

Engineering teams often struggle to maintain strong test coverage when code changes quickly. This system can be connected to pull request workflows in GitHub Actions, GitLab CI, Jenkins, or internal developer platforms to analyze changed Python files and recommend tests for newly added or modified functions. It helps reviewers quickly identify missing edge cases, boundary conditions, and higher-risk functions before code reaches production.

## Lessons Learned

- Python's built-in AST module is enough for reliable function extraction without adding unnecessary parser dependencies.
- Commit-range analysis needs fallback logic because a repository with only one commit does not support HEAD~1..HEAD.
- Local AI inference can slow down execution when the model service is unavailable, so timeout and fallback behavior are important.
- Complexity estimation does not need to be perfect to be useful; even branch and loop counts provide helpful testing signals.
- Structured JSON and Markdown outputs make the pipeline easier to integrate into automation systems.

## Troubleshooting Log

Issue:
The suggested ast-parser dependency is unnecessary and may fail in modern Python environments.

Resolution:
Removed ast-parser and used Python's built-in ast module.

Issue:
Global pip installation on Ubuntu 24.04 can conflict with externally managed Python environments.

Resolution:
Created and used a Python virtual environment before installing Python packages.

Issue:
tree was missing from the fresh Ubuntu environment.

Resolution:
Installed tree through apt.

Issue:
The initial repository only had one commit, so HEAD~1..HEAD could fail before a second commit existed.

Resolution:
Added fallback behavior that analyzes tracked Python files when commit-range diff detection fails.

Issue:
The AI model was unavailable, causing the pipeline to take too long during execution.

Resolution:
Reduced the model call timeout and used deterministic fallback recommendations when local inference was unavailable.

Issue:
The provided skeleton contained unfinished TODO logic.

Resolution:
Implemented code change detection, AST extraction, complexity estimation, suggestion generation, report writing, and CLI argument handling.
