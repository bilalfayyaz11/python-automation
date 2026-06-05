import re
import json
import sys
from collections import Counter


class PrivacyValidator:
    """
    Validates that log files contain no exposed sensitive identifiers.
    """

    def __init__(self):
        self.violations = []
        self.rules = {
            "ssn_exposed": r"\b(?!XXX-XX-)\d{3}-\d{2}-\d{4}\b",
            "full_email": r"\b[A-Za-z0-9._%+-]{2,}@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            "full_phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        }

    def check_record(self, record: dict, line_num: int) -> list:
        violations = []
        record_str = json.dumps(record)

        for rule_name, pattern in self.rules.items():
            matches = re.findall(pattern, record_str)
            for match in matches:
                violations.append({
                    "line": line_num,
                    "rule": rule_name,
                    "matched_value": match
                })

        if "ip_address" in record:
            violations.append({
                "line": line_num,
                "rule": "ip_field_present",
                "matched_value": record["ip_address"]
            })

        if "ssn" in record and not str(record["ssn"]).startswith("XXX-XX-"):
            violations.append({
                "line": line_num,
                "rule": "ssn_not_masked",
                "matched_value": record["ssn"]
            })

        return violations

    def validate_file(self, filename: str) -> bool:
        self.violations = []
        total_records = 0
        parse_errors = 0

        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line_num, line in enumerate(file, start=1):
                    try:
                        record = json.loads(line)
                        total_records += 1
                        self.violations.extend(self.check_record(record, line_num))
                    except json.JSONDecodeError:
                        parse_errors += 1
                        self.violations.append({
                            "line": line_num,
                            "rule": "json_parse_error",
                            "matched_value": "Invalid JSON"
                        })
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return False

        print("===== PRIVACY VALIDATION SUMMARY =====")
        print(f"File checked: {filename}")
        print(f"Records checked: {total_records}")
        print(f"Parse errors: {parse_errors}")
        print(f"Violations found: {len(self.violations)}")

        return len(self.violations) == 0

    def generate_report(self):
        if not self.violations:
            print("No privacy violations found.")
            return

        counts = Counter(v["rule"] for v in self.violations)

        print("\n===== VIOLATIONS BY TYPE =====")
        for rule, count in counts.items():
            print(f"{rule}: {count}")

        print("\n===== VIOLATION DETAILS =====")
        for violation in self.violations[:25]:
            print(
                f"Line {violation['line']} | "
                f"Rule: {violation['rule']} | "
                f"Matched: {violation['matched_value']}"
            )

        if len(self.violations) > 25:
            print(f"... {len(self.violations) - 25} additional violations hidden for readability")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 privacy_validator.py <log_file>")
        sys.exit(1)

    validator = PrivacyValidator()
    is_compliant = validator.validate_file(sys.argv[1])

    if is_compliant:
        print("\n✓ LOG FILE IS PRIVACY COMPLIANT")
        sys.exit(0)
    else:
        print("\n✗ PRIVACY VIOLATIONS DETECTED")
        validator.generate_report()
        sys.exit(1)
