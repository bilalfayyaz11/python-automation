# Typed Configuration Loader with Schema Validation

## Overview

This implementation provides a type-safe configuration loader for applications that need reliable JSON and YAML configuration management.

The loader validates configuration files against strict schemas, applies default values for optional settings, detects invalid values before runtime, and provides clear error messages for debugging.

This pattern is commonly used in production systems where configuration errors can cause deployment failures, unstable applications, or operational incidents.

## Architecture

+-----------------------------+
|     JSON / YAML Config      |
+--------------+--------------+
               |
               v
+-----------------------------+
|      ConfigLoader           |
| File Detection and Parsing  |
+--------------+--------------+
               |
               v
+-----------------------------+
|      Pydantic Schemas       |
| Type and Value Validation   |
+--------------+--------------+
               |
               v
+-----------------------------+
|     Validated AppConfig     |
| Safe Runtime Configuration  |
+-----------------------------+

## Features

- JSON configuration loading
- YAML configuration loading
- Type-safe schema validation
- Default values for optional settings
- Required field enforcement
- Nested configuration models
- Clear validation error reporting
- Configuration reload support
- Practical application usage example
- Automated test coverage

## Components

### config_loader.py

Core implementation containing:

- DatabaseConfig schema
- CacheConfig schema
- LoggingConfig schema
- AppConfig schema
- ConfigLoader class
- JSON/YAML parsing
- Validation error handling
- Reload functionality

### test_configs.py

Test suite validating:

- Full YAML configuration loading
- Minimal JSON configuration loading
- Default value application
- Invalid configuration rejection
- Missing required field detection
- Configuration reload behavior

### app_example.py

Practical CLI-style usage example that loads a config file and prints a structured summary.

### configs/valid_config.yaml

Complete production-style YAML configuration.

### configs/minimal_config.json

Minimal JSON configuration that relies on default values.

### configs/invalid_config.yaml

Intentionally invalid configuration used to verify validation failures.

## Technologies Used

- Python 3
- Pydantic
- PyYAML
- JSON
- YAML
- pathlib
- virtualenv

## Validation Rules

### Application

- app_name is required and cannot be empty
- environment must be one of: development, staging, production
- debug defaults to false

### Database

- username, password, and database are required
- host defaults to localhost
- port defaults to 5432 and must be between 1 and 65535
- max_connections defaults to 10 and must be between 1 and 100
- host must be localhost, a valid hostname, or a valid IPv4 address

### Cache

- enabled defaults to true
- ttl_seconds defaults to 300 and cannot be negative
- max_size_mb defaults to 100 and cannot exceed 1024

### Logging

- level defaults to INFO
- allowed levels are DEBUG, INFO, WARNING, ERROR, and CRITICAL
- format defaults to json
- allowed formats are json and text
- output_path defaults to /var/log/app.log

## How to Run

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install pyyaml "pydantic>=2"

Run the full test suite:

python3 test_configs.py

Run practical examples:

python3 app_example.py configs/valid_config.yaml
python3 app_example.py configs/minimal_config.json
python3 app_example.py configs/invalid_config.yaml

## Key Skills Demonstrated

- Type-safe Python configuration management
- Schema-based validation
- JSON and YAML parsing
- Pydantic model design
- Nested configuration modeling
- Default value handling
- Validation error reporting
- Runtime safety patterns
- Production configuration design

## Real World Applications

This type of configuration loader is used in backend services, DevOps platforms, deployment automation tools, cloud-native applications, and internal engineering systems.

It helps teams prevent broken deployments by validating configuration files before services start. This reduces runtime failures, improves debugging speed, and makes environment-specific configuration safer to manage.

## Lessons Learned

- Configuration should be validated before application startup
- Defaults reduce duplication but must still be explicit and safe
- Nested schemas make large configuration files easier to reason about
- Clear validation errors are critical for operational troubleshooting
- Modern Pydantic uses field_validator instead of legacy validator syntax

## Troubleshooting Log

### Legacy Pydantic Validator Syntax

Issue:
The original implementation pattern used the older validator decorator.

Resolution:
The implementation was updated to use Pydantic v2 field_validator syntax for modern compatibility.

### Invalid Environment

Issue:
The invalid configuration used environment value testing.

Resolution:
The schema correctly rejects unsupported environments and only allows development, staging, and production.

### Invalid Database Port

Issue:
The invalid configuration used port 99999.

Resolution:
The schema restricts database ports to the valid TCP/UDP range of 1 to 65535.

### Empty Database Host

Issue:
The invalid configuration used an empty database host.

Resolution:
The schema rejects empty host values and accepts localhost, hostnames, and valid IPv4 addresses only.

