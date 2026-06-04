#!/usr/bin/env python3

import os
import json
import yaml
import hashlib

from datetime import datetime
from pathlib import Path
from deepdiff import DeepDiff


class ConfigDriftScanner:

    def __init__(self, baseline_dir, current_dir, report_dir):

        self.baseline_dir = Path(baseline_dir)
        self.current_dir = Path(current_dir)
        self.report_dir = Path(report_dir)

        self.drift_results = []

        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def calculate_file_hash(self, filepath):

        try:

            with open(filepath, "rb") as file:
                return hashlib.sha256(
                    file.read()
                ).hexdigest()

        except Exception:
            return None

    def compare_text_files(
        self,
        baseline_file,
        current_file
    ):

        result = {
            "file": baseline_file.name,
            "drift_detected": False,
            "differences": []
        }

        try:

            with open(baseline_file, "r") as file:
                baseline_lines = file.readlines()

            with open(current_file, "r") as file:
                current_lines = file.readlines()

            baseline_hash = self.calculate_file_hash(
                baseline_file
            )

            current_hash = self.calculate_file_hash(
                current_file
            )

            if baseline_hash != current_hash:

                result["drift_detected"] = True
                result["baseline_hash"] = baseline_hash
                result["current_hash"] = current_hash

                max_lines = max(
                    len(baseline_lines),
                    len(current_lines)
                )

                for index in range(max_lines):

                    baseline_line = (
                        baseline_lines[index].strip()
                        if index < len(baseline_lines)
                        else "<missing>"
                    )

                    current_line = (
                        current_lines[index].strip()
                        if index < len(current_lines)
                        else "<missing>"
                    )

                    if baseline_line != current_line:

                        result["differences"].append({
                            "line": index + 1,
                            "baseline": baseline_line,
                            "current": current_line
                        })

        except Exception as error:

            result["error"] = str(error)

        return result

    def compare_yaml_configs(
        self,
        baseline_file,
        current_file
    ):

        result = {
            "file": baseline_file.name,
            "drift_detected": False,
            "differences": {}
        }

        try:

            with open(baseline_file, "r") as file:
                baseline_data = yaml.safe_load(file)

            with open(current_file, "r") as file:
                current_data = yaml.safe_load(file)

            diff = DeepDiff(
                baseline_data,
                current_data,
                ignore_order=True
            )

            if diff:

                result["drift_detected"] = True

                result["differences"] = json.loads(
                    diff.to_json()
                )

        except Exception as error:

            result["error"] = str(error)

        return result

    def scan_for_drift(self):

        print(
            "Starting configuration drift scan..."
        )

        text_configs = [
            "hosts.baseline",
            "packages.baseline",
            "services.baseline"
        ]

        for config in text_configs:

            baseline_path = (
                self.baseline_dir / config
            )

            current_path = (
                self.current_dir /
                config.replace(
                    ".baseline",
                    ".current"
                )
            )

            if (
                baseline_path.exists()
                and current_path.exists()
            ):

                result = self.compare_text_files(
                    baseline_path,
                    current_path
                )

                self.drift_results.append(
                    result
                )

        yaml_baseline = (
            self.baseline_dir /
            "app-config.baseline.yaml"
        )

        yaml_current = (
            self.current_dir /
            "app-config.current.yaml"
        )

        if (
            yaml_baseline.exists()
            and yaml_current.exists()
        ):

            result = self.compare_yaml_configs(
                yaml_baseline,
                yaml_current
            )

            self.drift_results.append(
                result
            )

        return self.drift_results

    def generate_report(
        self,
        output_format="json"
    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        report_data = {
            "scan_timestamp": timestamp,
            "total_configs_scanned":
                len(self.drift_results),
            "drifts_detected":
                sum(
                    1
                    for result
                    in self.drift_results
                    if result.get(
                        "drift_detected"
                    )
                ),
            "findings":
                self.drift_results
        }

        if output_format == "json":

            report_file = (
                self.report_dir /
                f"drift_report_{timestamp}.json"
            )

            with open(
                report_file,
                "w"
            ) as file:

                json.dump(
                    report_data,
                    file,
                    indent=2
                )

        else:

            report_file = (
                self.report_dir /
                f"drift_report_{timestamp}.txt"
            )

            with open(
                report_file,
                "w"
            ) as file:

                file.write(
                    "Configuration Drift Report\n"
                )

                file.write(
                    f"Generated: {timestamp}\n"
                )

                file.write(
                    "=" * 60 + "\n\n"
                )

                for finding in self.drift_results:

                    file.write(
                        f"File: {finding['file']}\n"
                    )

                    file.write(
                        f"Drift Detected: {finding['drift_detected']}\n"
                    )

                    if finding.get(
                        "drift_detected"
                    ):

                        file.write(
                            json.dumps(
                                finding.get(
                                    "differences",
                                    {}
                                ),
                                indent=2
                            )
                        )

                        file.write("\n")

                    file.write(
                        "-" * 60 + "\n"
                    )

        print(
            f"Report generated: {report_file}"
        )

        return report_file


if __name__ == "__main__":

    scanner = ConfigDriftScanner(
        baseline_dir=os.path.expanduser(
            "~/config-drift-scanner/baselines"
        ),
        current_dir=os.path.expanduser(
            "~/config-drift-scanner/current"
        ),
        report_dir=os.path.expanduser(
            "~/config-drift-scanner/reports"
        )
    )

    scanner.scan_for_drift()

    scanner.generate_report(
        output_format="json"
    )

    scanner.generate_report(
        output_format="text"
    )
