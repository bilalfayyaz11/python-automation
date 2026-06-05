from faker import Faker
import json
import random
from datetime import datetime, timezone

fake = Faker()

DIAGNOSES = [
    "Hypertension",
    "Diabetes",
    "Asthma",
    "COVID-19"
]

def generate_patient_record():
    """
    Generate a single patient record with sensitive healthcare data.
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "patient_id": str(random.randint(10000000, 99999999)),
        "ssn": fake.ssn(),
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "diagnosis": random.choice(DIAGNOSES),
        "ip_address": fake.ipv4()
    }

def generate_log_entries(count=50):
    """
    Generate healthcare log records and write one JSON object per line.
    """
    with open("healthcare_raw.log", "w", encoding="utf-8") as file:
        for _ in range(count):
            record = generate_patient_record()
            file.write(json.dumps(record) + "\n")

if __name__ == "__main__":
    generate_log_entries(50)
    print("Generated 50 log entries in healthcare_raw.log")
