#!/usr/bin/env python3
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class PolicyRule:
    id: str
    enabled: bool
    severity: str
    requirement: str = ""
    metadata: Dict = field(default_factory=dict)


class PolicyProfile:
    def __init__(self, profile_data: Dict):
        profile = profile_data.get("profile", {})
        self.name = profile.get("name")
        self.industry = profile.get("industry")
        self.rules = {}

        for rule_data in profile.get("rules", []):
            known_fields = {"id", "enabled", "severity", "requirement"}
            metadata = {k: v for k, v in rule_data.items() if k not in known_fields}

            rule = PolicyRule(
                id=rule_data.get("id"),
                enabled=bool(rule_data.get("enabled", False)),
                severity=rule_data.get("severity", "low"),
                requirement=rule_data.get("requirement", ""),
                metadata=metadata
            )

            self.rules[rule.id] = rule

    def get_rule(self, rule_id: str) -> Optional[PolicyRule]:
        return self.rules.get(rule_id)

    def get_enabled_rules(self) -> List[PolicyRule]:
        return [rule for rule in self.rules.values() if rule.enabled]

    def to_dict(self):
        return {
            "name": self.name,
            "industry": self.industry,
            "enabled_rules": [
                {
                    "id": rule.id,
                    "severity": rule.severity,
                    "requirement": rule.requirement,
                    "metadata": rule.metadata
                }
                for rule in self.get_enabled_rules()
            ]
        }


class PolicyGate:
    def __init__(self):
        self.profiles = {}
        self.active_profile = None

    def load_profile(self, profile_path: str) -> None:
        path = Path(profile_path)
        with open(path, "r", encoding="utf-8") as file:
            profile_data = yaml.safe_load(file)

        profile = PolicyProfile(profile_data)
        if not profile.name:
            raise ValueError(f"Profile name missing in {profile_path}")

        self.profiles[profile.name] = profile

    def load_profiles_from_directory(self, profiles_dir: str = "config/profiles") -> None:
        for profile_file in sorted(Path(profiles_dir).glob("*.yaml")):
            self.load_profile(str(profile_file))

    def switch_profile(self, profile_name: str) -> bool:
        if profile_name not in self.profiles:
            return False

        self.active_profile = self.profiles[profile_name]
        return True

    def check_encryption_rule(self, request_data: Dict, rule: PolicyRule) -> Dict:
        passed = bool(request_data.get("encrypted", False))
        return self.build_rule_result(rule, passed, "encrypted field must be true")

    def check_access_logging_rule(self, request_data: Dict, rule: PolicyRule) -> Dict:
        passed = bool(request_data.get("access_logged", False))
        return self.build_rule_result(rule, passed, "access_logged field must be true")

    def check_network_segmentation_rule(self, request_data: Dict, rule: PolicyRule) -> Dict:
        passed = bool(request_data.get("network_segmented", False))
        return self.build_rule_result(rule, passed, "network_segmented field must be true")

    def check_access_control_rule(self, request_data: Dict, rule: PolicyRule) -> Dict:
        min_length = int(rule.metadata.get("min_password_length", 12))
        password_length = int(request_data.get("password_length", 0))
        passed = password_length >= min_length
        return self.build_rule_result(rule, passed, f"password_length must be at least {min_length}")

    def check_rate_limiting_rule(self, request_data: Dict, rule: PolicyRule) -> Dict:
        max_requests = int(rule.metadata.get("max_requests", 1000))
        request_count = int(request_data.get("request_count", 0))
        passed = request_count <= max_requests
        return self.build_rule_result(rule, passed, f"request_count must not exceed {max_requests}")

    def check_data_retention_rule(self, request_data: Dict, rule: PolicyRule) -> Dict:
        max_days = int(rule.metadata.get("max_days", 2555))
        retention_days = int(request_data.get("retention_days", max_days))
        passed = retention_days <= max_days
        return self.build_rule_result(rule, passed, f"retention_days must not exceed {max_days}")

    def build_rule_result(self, rule: PolicyRule, passed: bool, expected: str) -> Dict:
        return {
            "rule_id": rule.id,
            "severity": rule.severity,
            "requirement": rule.requirement,
            "passed": passed,
            "expected": expected
        }

    def evaluate_rule(self, request_data: Dict, rule: PolicyRule) -> Dict:
        handlers = {
            "data_encryption": self.check_encryption_rule,
            "access_logging": self.check_access_logging_rule,
            "network_segmentation": self.check_network_segmentation_rule,
            "access_control": self.check_access_control_rule,
            "rate_limiting": self.check_rate_limiting_rule,
            "data_retention": self.check_data_retention_rule
        }

        handler = handlers.get(rule.id)
        if not handler:
            return self.build_rule_result(rule, True, "No custom evaluator registered")

        return handler(request_data, rule)

    def enforce_policy(self, request_data: Dict) -> Dict:
        if not self.active_profile:
            return {
                "allowed": False,
                "error": "No active profile selected",
                "violations": []
            }

        checks = []
        violations = []

        for rule in self.active_profile.get_enabled_rules():
            result = self.evaluate_rule(request_data, rule)
            checks.append(result)

            if not result["passed"]:
                violations.append(result)

        return {
            "allowed": len(violations) == 0,
            "profile": self.active_profile.name,
            "industry": self.active_profile.industry,
            "total_rules_checked": len(checks),
            "violations_count": len(violations),
            "checks": checks,
            "violations": violations
        }

    def get_active_profile_info(self) -> Dict:
        if not self.active_profile:
            return {
                "active_profile": None,
                "available_profiles": sorted(self.profiles.keys())
            }

        return {
            "active_profile": self.active_profile.to_dict(),
            "available_profiles": sorted(self.profiles.keys())
        }


def main():
    gate = PolicyGate()
    gate.load_profiles_from_directory()
    gate.switch_profile("healthcare")
    sample = {"data_type": "PHI", "encrypted": False, "access_logged": True}
    print(json.dumps(gate.enforce_policy(sample), indent=2))


if __name__ == "__main__":
    main()
