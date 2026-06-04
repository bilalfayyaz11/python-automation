#!/usr/bin/env python3

import subprocess
import sys
import time
import yaml

from collections import defaultdict, deque
from enum import Enum
from typing import Dict, List


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class Job:
    def __init__(self, name: str, command: str, dependencies: List[str] = None):
        self.name = name
        self.command = command
        self.dependencies = dependencies or []
        self.status = JobStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.error_message = None

    def execute(self) -> bool:
        self.status = JobStatus.RUNNING
        self.start_time = time.time()

        print(f"\n[RUNNING] {self.name}")
        print(f"Command: {self.command}")

        try:
            result = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.stdout.strip():
                print(result.stdout.strip())

            if result.returncode == 0:
                self.status = JobStatus.SUCCESS
                print(f"[SUCCESS] {self.name}")
            else:
                self.status = JobStatus.FAILED
                self.error_message = result.stderr.strip() or f"Command exited with code {result.returncode}"
                print(f"[FAILED] {self.name}: {self.error_message}")

            self.end_time = time.time()
            return self.status == JobStatus.SUCCESS

        except Exception as error:
            self.status = JobStatus.FAILED
            self.error_message = str(error)
            self.end_time = time.time()
            print(f"[FAILED] {self.name}: {self.error_message}")
            return False

    def __repr__(self):
        return f"Job({self.name}, status={self.status.value})"


class PipelineRunner:
    def __init__(self, config_file: str):
        self.jobs: Dict[str, Job] = {}
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)
        self.reverse_graph: Dict[str, List[str]] = defaultdict(list)
        self.load_config(config_file)

    def load_config(self, config_file: str):
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if not config or "jobs" not in config:
            raise ValueError("Configuration must contain a jobs list")

        for job_data in config["jobs"]:
            name = job_data["name"]
            command = job_data["command"]
            dependencies = job_data.get("dependencies", [])

            if name in self.jobs:
                raise ValueError(f"Duplicate job name detected: {name}")

            self.jobs[name] = Job(name, command, dependencies)

        for job_name, job in self.jobs.items():
            for dependency in job.dependencies:
                if dependency not in self.jobs:
                    raise ValueError(
                        f"Job '{job_name}' depends on missing job '{dependency}'"
                    )

                self.dependency_graph[dependency].append(job_name)
                self.reverse_graph[job_name].append(dependency)

        for job_name in self.jobs:
            self.dependency_graph[job_name]
            self.reverse_graph[job_name]

    def validate_dag(self) -> bool:
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {job: WHITE for job in self.jobs}

        def has_cycle(node: str) -> bool:
            color[node] = GRAY

            for neighbor in self.dependency_graph[node]:
                if color[neighbor] == GRAY:
                    return True

                if color[neighbor] == WHITE and has_cycle(neighbor):
                    return True

            color[node] = BLACK
            return False

        for job in self.jobs:
            if color[job] == WHITE:
                if has_cycle(job):
                    return False

        return True

    def topological_sort(self) -> List[str]:
        in_degree = {
            job: len(self.reverse_graph[job])
            for job in self.jobs
        }

        queue = deque(
            job for job, degree in in_degree.items()
            if degree == 0
        )

        sorted_order = []

        while queue:
            current_job = queue.popleft()
            sorted_order.append(current_job)

            for dependent in self.dependency_graph[current_job]:
                in_degree[dependent] -= 1

                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(sorted_order) != len(self.jobs):
            raise ValueError("Cycle detected or unresolved dependency exists")

        return sorted_order

    def can_execute(self, job_name: str) -> bool:
        dependencies = self.reverse_graph[job_name]

        return all(
            self.jobs[dependency].status == JobStatus.SUCCESS
            for dependency in dependencies
        )

    def mark_downstream_skipped(self, job_name: str):
        queue = deque(self.dependency_graph[job_name])
        visited = set()

        while queue:
            current_job = queue.popleft()

            if current_job in visited:
                continue

            visited.add(current_job)

            if self.jobs[current_job].status == JobStatus.PENDING:
                self.jobs[current_job].status = JobStatus.SKIPPED
                self.jobs[current_job].error_message = (
                    f"Skipped because upstream job '{job_name}' failed"
                )

            for downstream_job in self.dependency_graph[current_job]:
                queue.append(downstream_job)

    def execute_pipeline(self) -> Dict[str, JobStatus]:
        print("\n" + "=" * 60)
        print("STARTING PIPELINE EXECUTION")
        print("=" * 60)

        if not self.validate_dag():
            print("ERROR: Cycle detected in dependencies")
            return {}

        execution_order = self.topological_sort()

        print(f"\nExecution order: {' -> '.join(execution_order)}")

        for job_name in execution_order:
            job = self.jobs[job_name]

            if job.status == JobStatus.SKIPPED:
                print(f"\n[SKIPPED] {job_name}")
                continue

            if not self.can_execute(job_name):
                job.status = JobStatus.SKIPPED
                job.error_message = "Skipped because one or more dependencies did not succeed"
                print(f"\n[SKIPPED] {job_name}: dependency failure")
                self.mark_downstream_skipped(job_name)
                continue

            success = job.execute()

            if not success:
                self.mark_downstream_skipped(job_name)

        return {
            name: job.status
            for name, job in self.jobs.items()
        }

    def print_summary(self):
        print("\n" + "=" * 60)
        print("PIPELINE EXECUTION SUMMARY")
        print("=" * 60)

        for job_name, job in self.jobs.items():
            duration = ""

            if job.start_time and job.end_time:
                duration = f" ({job.end_time - job.start_time:.2f}s)"

            status_symbol = {
                JobStatus.SUCCESS: "✓",
                JobStatus.FAILED: "✗",
                JobStatus.SKIPPED: "⊘",
                JobStatus.PENDING: "○",
                JobStatus.RUNNING: "▶",
            }.get(job.status, "?")

            print(f"{status_symbol} {job_name}: {job.status.value}{duration}")

            if job.error_message:
                print(f"  Error: {job.error_message}")

        print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline_runner.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    runner = PipelineRunner(config_file)
    runner.execute_pipeline()
    runner.print_summary()


if __name__ == "__main__":
    main()
