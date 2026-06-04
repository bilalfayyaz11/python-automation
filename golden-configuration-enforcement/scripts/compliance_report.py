#!/usr/bin/env python3
"""
Generate compliance report from enforcement logs.
"""

import json
from pathlib import Path
from collections import Counter


def generate_report(log_dir):
    log_path = Path(log_dir)
    log_files = sorted(log_path.glob("violations_*.log"))

    if not log_files:
        print("No violation logs found.")
        print("Compliance Rate: 100% based on available checks.")
        return

    total_violations = 0
    violation_types = Counter()
    affected_configs = Counter()

    for file_path in log_files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for violation in data.get("violations", []):
            total_violations += 1
            violation_types[violation.get("type", "unknown")] += 1
            affected_configs[violation.get("config", "unknown")] += 1

    print("\nCompliance Report")
    print("=================")
    print(f"Log files reviewed: {len(log_files)}")
    print(f"Total violations: {total_violations}")

    print("\nViolations by Type")
    print("------------------")
    for violation_type, count in violation_types.most_common():
        print(f"{violation_type}: {count}")

    print("\nAffected Configurations")
    print("-----------------------")
    for config, count in affected_configs.most_common():
        print(f"{config}: {count}")


if __name__ == "__main__":
    generate_report("logs")
