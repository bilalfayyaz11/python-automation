import json
import hashlib
import re
from typing import Dict, Any


class HealthcareLogSanitizer:
    """
    Sanitizes healthcare logs by masking PII before records are stored or shared.
    """

    def __init__(self):
        self.pii_patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        }

    def mask_ssn(self, ssn: str) -> str:
        digits = re.sub(r"\D", "", str(ssn))
        if len(digits) >= 4:
            return f"XXX-XX-{digits[-4:]}"
        return "XXX-XX-XXXX"

    def mask_email(self, email: str) -> str:
        email = str(email)
        if "@" not in email:
            return "masked-email"
        username, domain = email.split("@", 1)
        first_char = username[0] if username else "x"
        return f"{first_char}****@{domain}"

    def mask_phone(self, phone: str) -> str:
        digits = re.sub(r"\D", "", str(phone))
        if len(digits) >= 4:
            return f"XXX-XXX-{digits[-4:]}"
        return "XXX-XXX-XXXX"

    def hash_patient_id(self, patient_id: str) -> str:
        value = str(patient_id).encode("utf-8")
        return hashlib.sha256(value).hexdigest()[:16]

    def mask_name(self, name: str) -> str:
        parts = str(name).split()
        if len(parts) >= 2:
            return f"{parts[0][0].upper()}.{parts[-1][0].upper()}."
        if len(parts) == 1 and parts[0]:
            return f"{parts[0][0].upper()}."
        return "X."

    def sanitize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = record.copy()

        if "ssn" in sanitized:
            sanitized["ssn"] = self.mask_ssn(sanitized["ssn"])

        if "email" in sanitized:
            sanitized["email"] = self.mask_email(sanitized["email"])

        if "phone" in sanitized:
            sanitized["phone"] = self.mask_phone(sanitized["phone"])

        if "patient_id" in sanitized:
            sanitized["patient_id"] = self.hash_patient_id(sanitized["patient_id"])

        if "name" in sanitized:
            sanitized["name"] = self.mask_name(sanitized["name"])

        sanitized.pop("ip_address", None)

        return sanitized

    def process_log_file(self, input_file: str, output_file: str):
        processed = 0
        failed = 0

        with open(input_file, "r", encoding="utf-8") as source, open(output_file, "w", encoding="utf-8") as target:
            for line_number, line in enumerate(source, start=1):
                try:
                    record = json.loads(line)
                    sanitized_record = self.sanitize_record(record)
                    target.write(json.dumps(sanitized_record) + "\n")
                    processed += 1
                except json.JSONDecodeError:
                    failed += 1
                    print(f"Failed to parse JSON at line {line_number}")

        print(f"Processed records: {processed}")
        print(f"Failed records: {failed}")
        print(f"Sanitized output written to {output_file}")


if __name__ == "__main__":
    sanitizer = HealthcareLogSanitizer()
    sanitizer.process_log_file("healthcare_raw.log", "healthcare_sanitized.log")
