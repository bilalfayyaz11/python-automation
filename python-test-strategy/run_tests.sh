#!/bin/bash

echo "Running Unit Tests..."
pytest tests/unit -m unit -v

echo -e "\nRunning Integration Tests..."
pytest tests/integration -m integration -v

echo -e "\nRunning All Tests with Coverage..."
pytest tests/ --cov=src/order_system --cov-report=html --cov-report=term

echo -e "\nCoverage report generated in htmlcov/index.html"
