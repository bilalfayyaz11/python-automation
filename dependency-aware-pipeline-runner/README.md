# Dependency-Aware Pipeline Runner

## What This Does

This implementation provides a dependency-aware pipeline runner that executes jobs in the correct order based on declared dependencies.

The runner reads pipeline definitions from YAML, builds a directed dependency graph, validates that the graph has no cycles, resolves execution order using topological sorting, and executes each job safely. If a job fails, all downstream jobs that depend on it are automatically skipped.

This mirrors the core orchestration logic used in CI/CD platforms, workflow engines, data pipelines, and automation systems.

## Architecture

    +-----------------------------+
    | YAML Pipeline Configuration |
    | pipeline_config.yaml        |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | PipelineRunner              |
    | load_config()               |
    | validate_dag()              |
    | topological_sort()          |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Dependency Graph            |
    | job -> downstream jobs      |
    | job -> required jobs        |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Execution Engine            |
    | can_execute()               |
    | execute_pipeline()          |
    | mark_downstream_skipped()   |
    +--------------+--------------+
                   |
                   v
    +-----------------------------+
    | Job Execution               |
    | subprocess commands         |
    | success / failed / skipped  |
    +-----------------------------+

## Prerequisites

- Ubuntu Linux or compatible Linux environment
- Python 3.8 or newer
- python3-pip
- python3-venv
- PyYAML
- Git
- Bash shell

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git

python3 -m venv venv

source venv/bin/activate

pip install pyyaml

## How to Reproduce

Create and activate the Python environment.

python3 -m venv venv
source venv/bin/activate
pip install pyyaml

Run the successful pipeline.

python3 pipeline_runner.py pipeline_config.yaml

Run the failure propagation scenario.

python3 pipeline_runner.py pipeline_config_fail.yaml

Run the complex dependency graph.

python3 pipeline_runner.py pipeline_complex.yaml

Run the complete test suite.

python3 test_pipeline.py

Validate Python syntax.

python3 -m py_compile pipeline_runner.py test_pipeline.py

## Tools Used

- Python
- PyYAML
- Bash
- subprocess
- directed graphs
- topological sorting
- cycle detection
- dependency propagation
- Linux shell
- Git

## Key Skills Demonstrated

- Built a dependency-aware execution system using directed acyclic graphs
- Implemented topological sorting to determine safe execution order
- Added cycle detection to prevent invalid pipeline definitions
- Implemented failure propagation for downstream dependent jobs
- Parsed YAML configuration into executable job objects
- Used subprocess execution with timeout handling and output capture
- Modeled CI/CD orchestration logic from first principles
- Validated multiple pipeline scenarios including success, failure, and complex dependency graphs

## Real-World Use Case

This pattern is used in CI/CD platforms, workflow schedulers, build systems, data pipeline orchestrators, and infrastructure automation tools. In a real engineering organization, pipelines often include checkout, dependency installation, linting, testing, building, security scanning, packaging, and deployment. A dependency-aware runner ensures these jobs execute safely in the correct order and prevents deployment when required upstream checks fail.

## Lessons Learned

- Pipelines are best represented as directed acyclic graphs when jobs depend on one another.
- Topological sorting provides a reliable way to calculate execution order.
- Cycle detection is critical because circular dependencies make execution impossible.
- Failure propagation prevents unsafe downstream actions after an upstream failure.
- YAML is useful for defining pipelines because it separates configuration from execution logic.

## Troubleshooting Log

- The starter implementation contained pass placeholders across job execution, configuration loading, DAG validation, sorting, dependency checks, and pipeline execution.
- Replaced placeholders with a complete pipeline runner implementation.
- Added missing dependency validation so jobs cannot depend on undefined jobs.
- Added cycle detection using DFS color states.
- Added Kahn-style topological sorting for deterministic execution order.
- Added downstream skip propagation when upstream jobs fail.
- Added syntax validation with py_compile.
