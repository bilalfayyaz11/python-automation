#!/usr/bin/env python3
import json
import datetime
from pathlib import Path

class IncidentLogger:
    def __init__(self, log_dir="incident-logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

    def _now(self):
        return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    def _path(self, incident_id):
        return self.log_dir / f"{incident_id}.json"

    def start_incident(self, incident_type, severity):
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        incident_id = f"INC-{incident_type.upper()}-{timestamp}"

        data = {
            "incident_id": incident_id,
            "incident_type": incident_type,
            "severity": severity,
            "status": "investigating",
            "started_at": self._now(),
            "closed_at": None,
            "duration_seconds": None,
            "actions": []
        }

        self._path(incident_id).write_text(json.dumps(data, indent=2))
        return incident_id

    def log_action(self, incident_id, action, result):
        path = self._path(incident_id)
        data = json.loads(path.read_text())

        data["actions"].append({
            "timestamp": self._now(),
            "action": action,
            "result": result
        })

        path.write_text(json.dumps(data, indent=2))

    def close_incident(self, incident_id, resolution, root_cause):
        path = self._path(incident_id)
        data = json.loads(path.read_text())

        closed_at = datetime.datetime.utcnow().replace(microsecond=0)
        started_at = datetime.datetime.fromisoformat(data["started_at"].replace("Z", ""))

        data["status"] = "resolved"
        data["closed_at"] = closed_at.isoformat() + "Z"
        data["duration_seconds"] = int((closed_at - started_at).total_seconds())
        data["resolution"] = resolution
        data["root_cause"] = root_cause

        path.write_text(json.dumps(data, indent=2))

    def generate_report(self, incident_id):
        data = json.loads(self._path(incident_id).read_text())

        lines = [
            f"# Incident Report: {data['incident_id']}",
            "",
            f"- Type: {data['incident_type']}",
            f"- Severity: {data['severity']}",
            f"- Status: {data['status']}",
            f"- Started At: {data['started_at']}",
            f"- Closed At: {data.get('closed_at')}",
            f"- Duration Seconds: {data.get('duration_seconds')}",
            "",
            "## Actions"
        ]

        for action in data["actions"]:
            lines.append(f"- [{action['timestamp']}] {action['action']} => {action['result']}")

        if data.get("resolution"):
            lines.extend(["", "## Resolution", data["resolution"]])

        if data.get("root_cause"):
            lines.extend(["", "## Root Cause", data["root_cause"]])

        return "\n".join(lines)

if __name__ == "__main__":
    logger = IncidentLogger()
    incident_id = logger.start_incident("test", "low")
    logger.log_action(incident_id, "Logger test", "success")
    logger.close_incident(incident_id, "Logger verified", "Validation run")
    print(logger.generate_report(incident_id))
