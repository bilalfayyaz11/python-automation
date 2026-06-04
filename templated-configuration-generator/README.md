# Templated Configuration Generator

## What This Does

This implementation provides a reusable configuration generation system using Jinja2 templates, YAML environment data, and JSON Schema validation.

The generator creates standardized Nginx and application configuration files for different environments such as development and production. The validator checks generated YAML configuration against a schema and performs structural validation for Nginx configuration files.

This pattern is widely used in DevOps and platform engineering to reduce manual configuration errors, standardize deployments, and safely generate environment-specific infrastructure and application settings.

## Architecture

    +-----------------------------+
    | Environment Data            |
    | data/dev_config.yaml        |
    | data/prod_config.yaml       |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Jinja2 Templates            |
    | templates/nginx.conf.j2     |
    | templates/app_config.yaml.j2|
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Config Generator            |
    | generator.py                |
    | render templates + data     |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Generated Configurations    |
    | configs/nginx.conf          |
    | configs/app_config.yaml     |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Validation Layer            |
    | validator.py                |
    | JSON Schema + Nginx checks  |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Verification Script         |
    | verify_config_generator.sh  |
    +-----------------------------+

## Prerequisites

- Ubuntu Linux or compatible Linux environment
- Python 3.8 or newer
- python3-pip
- python3-venv
- Git
- Bash shell
- Jinja2
- PyYAML
- jsonschema

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git

python3 -m venv venv

source venv/bin/activate

pip install jinja2 pyyaml jsonschema

## How to Reproduce

Create and activate the Python environment.

python3 -m venv venv

source venv/bin/activate

pip install jinja2 pyyaml jsonschema

Generate development configurations.

python3 generator.py data/dev_config.yaml

Generate production configurations.

python3 generator.py data/prod_config.yaml

Validate the generated application configuration.

python3 validator.py configs/app_config.yaml app_config_schema.json

Validate the generated Nginx configuration.

python3 validator.py configs/nginx.conf nginx

Run the verification workflow.

./verify_config_generator.sh

## Tools Used

- Python
- Jinja2
- PyYAML
- jsonschema
- Bash
- YAML
- JSON Schema
- Nginx configuration syntax
- Linux shell
- Git

## Key Skills Demonstrated

- Built a reusable configuration generator using Jinja2 templates
- Separated environment-specific data from reusable configuration templates
- Generated development and production-ready configuration outputs
- Validated YAML configuration using JSON Schema
- Added structural validation for generated Nginx configuration
- Implemented a repeatable verification workflow
- Demonstrated DevOps configuration management patterns used in Ansible, Helm, Terraform, and internal platform tooling
- Reduced manual configuration risk through automation and validation

## Real-World Use Case

This approach is used by DevOps and platform engineering teams to generate consistent configuration files across multiple environments. A company may need separate configurations for development, staging, and production while keeping the same structure and controls. Template-driven generation allows engineers to maintain one reusable template and inject environment-specific values safely, reducing configuration drift and deployment errors.

## Lessons Learned

- Templates reduce repeated manual configuration work.
- YAML data files make environment-specific values easy to manage.
- Schema validation catches configuration mistakes before deployment.
- Generated infrastructure and application configs should always be validated before use.
- Separating templates from data makes configuration workflows easier to scale.

## Troubleshooting Log

- Global Python package installation was avoided because Ubuntu 24.04 may restrict unmanaged system-level pip installs.
- A Python virtual environment was used for Jinja2, PyYAML, and jsonschema.
- The starter generator had self.env set to None and incomplete TODO sections.
- Replaced generator placeholders with a complete Jinja2 rendering implementation.
- The starter validator had incomplete TODO sections.
- Replaced validator placeholders with complete YAML schema validation and Nginx structure checks.
- Missing data files caused generation failure and were recreated under the data directory.
- Added an invalid configuration test to verify schema validation catches missing required fields.
