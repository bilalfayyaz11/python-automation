# Async Execution Engine

## What This Does
This system implements a Python asynchronous execution engine for running multiple tasks concurrently with controlled worker pools. It supports task submission, queue-based scheduling, execution tracking, cancellation, priority handling, monitoring, and statistics reporting. The engine demonstrates how modern automation platforms process many independent jobs efficiently without blocking the main application. This pattern is directly applicable to cloud automation, CI/CD runners, background processing, and AIOps workflows.

## Architecture
    +--------------------------+
    | Task Producer            |
    | main.py / advanced_test  |
    +------------+-------------+
                 |
                 v
    +--------------------------+
    | AsyncExecutionEngine     |
    | submit_task()            |
    | get_statistics()         |
    | cancel_task()            |
    +------------+-------------+
                 |
        +--------+--------+
        |                 |
        v                 v
    +-----------+     +----------------+
    | Queue     |     | Priority Queue |
    | FIFO      |     | Ordered Tasks  |
    +-----+-----+     +--------+-------+
          |                    |
          +---------+----------+
                    |
                    v
    +--------------------------+
    | Worker Pool              |
    | Worker 1                 |
    | Worker 2                 |
    | Worker 3+                |
    +------------+-------------+
                 |
      +----------+----------+
      |          |          |
      v          v          v
    Compute    File I/O    Monitoring

## Prerequisites
- Ubuntu Linux or compatible Linux environment
- Python 3.8 or newer
- python3-pip
- python3-venv
- Git
- Internet access for Python package installation

## Setup & Installation
sudo apt update

sudo apt install -y python3 python3-pip python3-venv git

python3 -m venv venv

source venv/bin/activate

pip install aiohttp aiofiles

## How to Reproduce
Create and activate the environment.

python3 -m venv venv
source venv/bin/activate
pip install aiohttp aiofiles

Create the test input file.

echo "Sample data for async file processing" > test_input.txt

Run the basic execution workflow.

python main.py

Run the advanced test workflow.

python advanced_test.py

Select option 1 for stress testing.

Select option 2 for priority execution testing.

Verify syntax.

python -m py_compile task_model.py execution_engine.py sample_tasks.py main.py monitor.py advanced_test.py

## Tools Used
- Python
- asyncio
- aiohttp
- aiofiles
- dataclasses
- priority queues
- worker pools
- Linux shell
- Git

## Key Skills Demonstrated
- Built an asynchronous task execution engine using Python asyncio
- Implemented concurrent worker pools with controlled parallelism
- Added task lifecycle tracking for pending, running, completed, failed, and cancelled states
- Implemented FIFO and priority-based scheduling
- Added execution statistics and monitoring visibility
- Created reusable async task functions for compute and file operations
- Designed scalable automation logic similar to CI/CD and platform execution systems
- Implemented defensive error handling for failed task execution

## Real-World Use Case
This design is used in engineering platforms where many independent jobs need to run efficiently in the background. Examples include CI/CD pipelines, infrastructure automation systems, cloud provisioning workflows, log processing systems, monitoring pipelines, internal developer platforms, and AIOps automation engines. Instead of blocking the main application, tasks are submitted to a queue and processed concurrently by workers.

## Lessons Learned
- asyncio improves throughput when tasks involve waiting, I/O, or independent execution.
- Worker pools prevent unlimited concurrency from overwhelming the system.
- Task lifecycle states make automation systems easier to debug and monitor.
- Priority queues allow urgent tasks to execute before lower-priority work.
- Monitoring and statistics are essential for understanding execution health.

## Troubleshooting Log
- The original implementation contained pass placeholders in the core engine, sample tasks, monitoring logic, and advanced tests.
- Replaced placeholders with complete async queue, worker, monitoring, and priority scheduling logic.
- Added explicit task states to make execution progress observable.
- Added queue draining during shutdown to prevent submitted tasks from being lost.
- Added syntax validation using py_compile to confirm all Python files are executable.
