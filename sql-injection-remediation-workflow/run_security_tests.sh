#!/bin/bash

set -e

echo "=== Starting Security Regression Tests ==="

source venv/bin/activate

pytest test_security.py -v --junitxml=test-results.xml

pytest test_security.py --cov=secure_app --cov-report=term

echo "=== Security Tests Complete ==="
