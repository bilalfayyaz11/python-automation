import yaml
from pathlib import Path
from typing import Dict, Any, Tuple


class PolicyEngine:
    """
    Validates and enforces automation policies.
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path).resolve()

        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.policy_config = self.config.get("policies", {})
        self.allowed_task_types = set(
            self.policy_config.get("allowed_task_types", ["backup", "deploy", "cleanup"])
        )
        self.max_timeout = int(self.policy_config.get("timeout", 300))
        self.max_retries = int(self.policy_config.get("max_retries", 3))

    def validate_task(self, task_data: Dict[str, Any]) -> Tuple[bool, str]:
        if not isinstance(task_data, dict):
            return False, "Task payload must be a JSON object"

        if "task_type" not in task_data:
            return False, "Missing required field: task_type"

        if "parameters" not in task_data:
            return False, "Missing required field: parameters"

        task_type = task_data.get("task_type")
        parameters = task_data.get("parameters")

        if task_type not in self.allowed_task_types:
            return False, f"Invalid task_type '{task_type}'. Allowed values: {sorted(self.allowed_task_types)}"

        if not isinstance(parameters, dict):
            return False, "parameters must be a JSON object"

        priority = task_data.get("priority", "medium")
        if priority not in {"high", "medium", "low"}:
            return False, "priority must be one of: high, medium, low"

        timeout = int(task_data.get("timeout", self.max_timeout))
        if timeout > self.max_timeout:
            return False, f"timeout exceeds policy maximum of {self.max_timeout} seconds"

        if task_type == "backup":
            if "path" not in parameters or "destination" not in parameters:
                return False, "backup tasks require parameters: path and destination"

        if task_type == "deploy":
            if "service" not in parameters or "version" not in parameters:
                return False, "deploy tasks require parameters: service and version"

        if task_type == "cleanup":
            if "target" not in parameters:
                return False, "cleanup tasks require parameter: target"

        return True, "Valid task"

    def get_retry_policy(self, task_type: str) -> int:
        return self.max_retries
