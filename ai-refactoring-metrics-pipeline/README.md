# AI-Driven Refactoring Metrics Pipeline

## What This Does

This implementation provides a metrics-driven Python refactoring workflow that measures legacy code complexity, refactors the logic into a cleaner strategy-based design, and validates behavior with automated tests.

The system compares cyclomatic complexity and maintainability before and after refactoring using Radon. It also verifies that the refactored implementation produces the same outputs as the original legacy code.

This type of workflow helps engineering teams reduce technical debt safely by proving that code quality improved without breaking business logic.

## Architecture

    +-----------------------------+
    | Legacy Pricing Logic        |
    | legacy_calculator.py        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Code Quality Measurement    |
    | Radon CC / MI Metrics       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Refactored Design           |
    | Strategy Pattern            |
    | Early Returns               |
    | Type Hints                  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Validation Layer            |
    | pytest Correctness Tests    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Refactoring Evidence        |
    | Complexity Comparison       |
    | Maintainability Improvement |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3.12
- Python pip
- Python virtual environments
- Git
- tree
- Radon
- Pylint
- Pytest
- pytest-benchmark
- Black
- isort

## Setup & Installation

sudo apt update

sudo apt install -y python3-pip python3-venv git tree

mkdir -p ~/ai-refactor-lab

cd ~/ai-refactor-lab

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install radon pylint pytest pytest-benchmark black isort

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Measure legacy complexity:

radon cc legacy_calculator.py -s

radon mi legacy_calculator.py -s

Measure refactored complexity:

radon cc refactored_calculator.py -s

radon mi refactored_calculator.py -s

Run correctness validation:

pytest -v test_correctness.py

Review the full working directory:

tree ~/ai-refactor-lab

## Tools Used

- Python 3.12
- Radon
- Pytest
- Pylint
- Black
- isort
- Bash
- Git
- Linux
- Strategy Pattern
- Type Hints

## Key Skills Demonstrated

- Legacy code refactoring
- Code complexity analysis
- Maintainability measurement
- Strategy pattern implementation
- Automated regression testing
- Technical debt reduction
- Quality gate design
- Python software engineering
- DevOps-style code quality monitoring
- Evidence-based engineering improvement

## Real-World Use Case

Companies often have legacy business logic that works but is difficult to maintain, risky to modify, and expensive to test manually. This workflow shows how an engineering team can measure code quality, refactor safely, validate behavior with tests, and produce objective evidence that maintainability improved. It is directly useful in backend engineering, platform engineering, DevOps, SRE, and technical debt modernization work.

## Lessons Learned

- Refactoring should start with measurement, not opinion.
- Deeply nested conditionals increase complexity and make future changes risky.
- Strategy pattern is useful when business rules differ by category or type.
- Automated tests are required to prove that behavior stayed the same after refactoring.
- Metrics like cyclomatic complexity and maintainability index help justify technical debt work to engineering leaders.

## Troubleshooting Log

Issue:
The original lab suggested installing aider-chat, which can add unnecessary setup time and dependency overhead.

Resolution:
Skipped aider-chat and implemented the refactor directly using Python, Radon, and pytest.

Issue:
The provided scripts contained TODO placeholders and could not run as written.

Resolution:
Implemented the legacy code, refactored design, and correctness tests manually.

Issue:
Fresh Ubuntu environment did not include pip, tree, Radon, pytest, Black, or isort.

Resolution:
Installed system dependencies through apt and Python quality tools inside a virtual environment.

Issue:
Legacy code used deeply nested conditionals that made business logic difficult to follow.

Resolution:
Refactored category-specific discount behavior into separate strategy classes.

Issue:
Refactoring could have changed pricing behavior accidentally.

Resolution:
Created pytest regression tests comparing legacy and refactored outputs for the same inputs.
