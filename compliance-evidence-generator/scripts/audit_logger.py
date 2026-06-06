#!/usr/bin/env python3
"""
Audit Log Generator
Creates structured audit logs for compliance tracking.
"""

import json
from datetime import datetime
from pathlib import Path
from collections import Counter


class AuditLogger:
    def __init__(self, log_dir="../logs"):
        self.log_dir = Path(log_dir).resolve()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log = self.log_dir / "audit.log"
        self.audit_json = self.log_dir / "audit.json"

    def write_entry(self, audit_entry):
        line = json.dumps(audit_entry, sort_keys=True)

        with open(self.audit_log, "a", encoding="utf-8") as file:
            file.write(line + "\n")

        existing = []
        if self.audit_json.exists():
            try:
                existing = json.loads(self.audit_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = []

        existing.append(audit_entry)
        self.audit_json.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    def log_evidence_collection(self, evidence_type, status, details=None):
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "evidence_collection",
            "evidence_type": evidence_type,
            "status": status,
            "details": details or {}
        }
        self.write_entry(audit_entry)

    def log_report_generation(self, report_type, output_path, status):
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "report_generation",
            "report_type": report_type,
            "output_path": output_path,
            "status": status
        }
        self.write_entry(audit_entry)

    def generate_audit_summary(self):
        events = []

        if self.audit_log.exists():
            for line in self.audit_log.read_text(encoding="utf-8").splitlines():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return {
            "total_events": len(events),
            "events_by_type": dict(Counter(event.get("event_type", "unknown") for event in events)),
            "events_by_status": dict(Counter(event.get("status", "unknown") for event in events))
        }
