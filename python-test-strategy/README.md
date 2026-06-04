# Python Test Strategy Framework

## What This Does

This implementation demonstrates a multi-layered testing strategy for a Python application using unit tests, integration tests, and coverage analysis. The system models a simplified e-commerce order processing platform and validates both individual component behavior and complete workflow execution.

The solution provides confidence that business logic behaves correctly under normal and edge-case conditions. By combining isolated component testing with end-to-end workflow validation, the implementation reduces deployment risk and improves software maintainability.

## Architecture

```text
+--------------------------------------------------+
|                    Test Suite                    |
+----------------------+---------------------------+
                       |
         +-------------+-------------+
         |                           |
         v                           v
+-------------------+      +----------------------+
|    Unit Tests     |      | Integration Tests    |
| Models            |      | Order Processing     |
| Inventory         |      | Inventory Updates    |
| Calculations      |      | Workflow Validation  |
+---------+---------+      +----------+-----------+
          |                           |
          +-------------+-------------+
                        |
                        v
+--------------------------------------------------+
|              Order Processing System             |
+----------------------+---------------------------+
| Models               | Inventory Manager         |
| Product              | Product Storage           |
| OrderItem            | Availability Checks       |
| Order                | Stock Management          |
+----------------------+---------------------------+
                        |
                        v
+--------------------------------------------------+
|                 Order Processor                  |
| Validation | Processing | Inventory Updates      |
+--------------------------------------------------+
```

## Prerequisites

* Ubuntu 24.04 or compatible Linux distribution
* Python 3.12+
* python3-pip
* python3-venv
* Git
* pytest
* pytest-cov
* pytest-mock

## Setup & Installation

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git

mkdir -p ~/python-test-strategy
cd ~/python-test-strategy

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install pytest pytest-cov pytest-mock
```

## How to Reproduce

```bash
git clone https://github.com/bilalfayyaz11/python-automation.git
cd python-automation/python-test-strategy

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt 2>/dev/null || true

pytest tests/ -v

pytest tests/ \
  --cov=src/order_system \
  --cov-report=term-missing
```

## Tools Used

* Python 3.12
* Pytest
* Pytest Coverage
* Pytest Mock
* Git
* Virtual Environments
* Decimal Module
* Dataclasses

## Key Skills Demonstrated

* Unit Test Design
* Integration Test Design
* Test Layer Separation
* Business Logic Validation
* Test Fixtures
* Coverage Analysis
* Inventory Management Logic
* Order Processing Workflow Validation
* Test Automation
* Software Quality Engineering

## Real-World Use Case

This testing strategy mirrors how modern engineering teams validate production services. Unit tests verify individual components such as pricing calculations and inventory management. Integration tests validate complete workflows including order validation, stock reduction, and transaction processing. The combination provides confidence that system changes can be deployed safely without introducing regressions.

## Lessons Learned

* Unit tests should validate behavior in complete isolation.
* Integration tests provide confidence that components work together correctly.
* Decimal values should always be used for monetary calculations.
* Fixtures simplify test setup and improve maintainability.
* Coverage reports reveal untested code paths that may contain defects.

## Troubleshooting Log

### Import Errors

Issue:

Tests fail due to module resolution errors.

Fix:

```bash
cd ~/python-test-strategy
source .venv/bin/activate
pytest tests/
```

### Decimal Precision Issues

Issue:

Unexpected failures during monetary calculations.

Fix:

```python
from decimal import Decimal
```

Always use Decimal instead of float for currency calculations.

### Coverage Not Displaying

Issue:

Coverage report shows zero results.

Fix:

```bash
pytest tests/ \
  --cov=src/order_system \
  --cov-report=term-missing
```

### Fixture Resolution Problems

Issue:

Pytest cannot locate fixtures.

Fix:

Ensure fixtures exist within the test class or move shared fixtures into `conftest.py`.
