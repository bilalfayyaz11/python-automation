#!/usr/bin/env python3
"""
Golden Configuration Enforcement System
Compares current configurations against approved standards and blocks unsafe drift.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import yaml
from deepdiff import DeepDiff
from jsonschema import validate, ValidationError


class ConfigEnforcer:
    def __init__(self, golden_dir, current_dir, log_dir):
        self.golden_dir = Path(golden_dir)
        self.current_dir = Path(current_dir)
        self.log_dir = Path(log_dir)
        self.schema_file = self.golden_dir / "config_schema.json"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def load_yaml(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return data if data else {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        except yaml.YAMLError as error:
            raise ValueError(f"Invalid YAML syntax in {filepath}: {error}")

    def load_schema(self):
        with open(self.schema_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def validate_schema(self, config, config_name):
        violations = []
        try:
            validate(instance=config, schema=self.load_schema())
        except ValidationError as error:
            violations.append({
                "type": "schema_violation",
                "config": config_name,
                "path": list(error.path),
                "message": error.message
            })
        return violations

    def compare_configs(self, golden_config, current_config, config_name):
        violations = []
        diff = DeepDiff(golden_config, current_config, ignore_order=True)

        for path, change in diff.get("values_changed", {}).items():
            violations.append({
                "type": "value_changed",
                "config": config_name,
                "path": path,
                "expected": change.get("old_value"),
                "actual": change.get("new_value")
            })

        for path in diff.get("dictionary_item_removed", []):
            violations.append({
                "type": "missing_required_item",
                "config": config_name,
                "path": path,
                "expected": "present",
                "actual": "missing"
            })

        for path in diff.get("dictionary_item_added", []):
            violations.append({
                "type": "unexpected_item",
                "config": config_name,
                "path": path,
                "expected": "not present",
                "actual": "present"
            })

        return violations

    def check_security_violations(self, current_config, config_name):
        violations = []
        security = current_config.get("security", {})
        hardening = current_config.get("hardening", {})
        network = current_config.get("network", {})

        if security.get("permit_root_login") is True:
            violations.append({
                "type": "critical_security_violation",
                "config": config_name,
                "path": "security.permit_root_login",
                "message": "Root login is enabled"
            })

        if security.get("password_authentication") is True:
            violations.append({
                "type": "critical_security_violation",
                "config": config_name,
                "path": "security.password_authentication",
                "message": "Password authentication is enabled"
            })

        if hardening.get("x11_forwarding") is True:
            violations.append({
                "type": "security_hardening_violation",
                "config": config_name,
                "path": "hardening.x11_forwarding",
                "message": "X11 forwarding is enabled"
            })

        if security.get("ssl", {}).get("enabled") is False:
            violations.append({
                "type": "critical_security_violation",
                "config": config_name,
                "path": "security.ssl.enabled",
                "message": "SSL/TLS is disabled"
            })

        if network.get("timeout", 0) > 60:
            violations.append({
                "type": "operational_violation",
                "config": config_name,
                "path": "network.timeout",
                "message": "Network timeout is too high"
            })

        if security.get("max_auth_tries", 0) > 3:
            violations.append({
                "type": "security_hardening_violation",
                "config": config_name,
                "path": "security.max_auth_tries",
                "message": "Maximum authentication attempts exceed approved baseline"
            })

        return violations

    def match_golden_file(self, current_file):
        name = current_file.stem

        if "webserver" in name:
            return self.golden_dir / "webserver_golden.yaml"

        if "ssh" in name:
            return self.golden_dir / "ssh_golden.yaml"

        return None

    def enforce_config(self, current_file):
        config_name = current_file.name
        golden_file = self.match_golden_file(current_file)

        if golden_file is None:
            return [{
                "type": "mapping_error",
                "config": config_name,
                "message": "No matching golden configuration found"
            }]

        golden_config = self.load_yaml(golden_file)
        current_config = self.load_yaml(current_file)

        violations = []
        violations.extend(self.validate_schema(current_config, config_name))
        violations.extend(self.compare_configs(golden_config, current_config, config_name))
        violations.extend(self.check_security_violations(current_config, config_name))

        return violations

    def log_violations(self, violations):
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"violations_{timestamp}.log"

        payload = {
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "total_violations": len(violations),
            "violations": violations
        }

        with open(log_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

        print(f"Violation log written to: {log_file}")

    def block_deployment(self, violations):
        print("\n" + "=" * 60)
        print("DEPLOYMENT BLOCKED")
        print("=" * 60)
        print(f"Total violations detected: {len(violations)}")
        print("=" * 60)

        for item in violations:
            print(f"- [{item.get('type')}] {item.get('config')}: {item.get('message', item.get('path'))}")

        print("=" * 60 + "\n")
        self.log_violations(violations)
        sys.exit(1)

    def run(self):
        all_violations = []
        current_files = sorted(self.current_dir.glob("*.yaml"))

        if not current_files:
            print("No current configuration files found.")
            return True

        for current_file in current_files:
            print(f"Checking: {current_file.name}")
            violations = self.enforce_config(current_file)
            all_violations.extend(violations)

        if all_violations:
            self.block_deployment(all_violations)

        print("All configurations compliant. Deployment allowed.")
        return True


def main():
    enforcer = ConfigEnforcer(
        golden_dir="golden",
        current_dir="current",
        log_dir="logs"
    )
    enforcer.run()


if __name__ == "__main__":
    main()
