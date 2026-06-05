#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from pathlib import Path


class AuditLogger:
    def __init__(self, log_directory):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_directory / "audit.log"

    def log_event(self, event_type, event_data):
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "data": event_data
        }

        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")

    def query_logs(self, filters=None):
        filters = filters or {}
        records = []

        if not self.log_file.exists():
            return records

        with self.log_file.open("r", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)

                if filters.get("event_type") and record["event_type"] != filters["event_type"]:
                    continue

                if filters.get("user"):
                    data = record.get("data", {})
                    if filters["user"] not in str(data):
                        continue

                records.append(record)

        return records

    def generate_report(self, start_date=None, end_date=None):
        records = self.query_logs()
        stats = {}

        for record in records:
            event_type = record["event_type"]
            stats[event_type] = stats.get(event_type, 0) + 1

        return {
            "total_events": len(records),
            "event_counts": stats,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
