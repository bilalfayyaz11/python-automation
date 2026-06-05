#!/usr/bin/env python3
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

import yaml

from audit_logger import AuditLogger


class ApprovalEngine:
    def __init__(self, config_path):
        self.config_path = config_path

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.state_file = Path("approval_state.json")
        self.audit_logger = AuditLogger(self.config["audit_settings"]["log_directory"])
        self.state = self._load_state()

    def _load_state(self):
        if not self.state_file.exists():
            return {"requests": {}}

        with self.state_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_state(self):
        temp_file = self.state_file.with_suffix(".tmp")

        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(self.state, file, indent=2)

        os.replace(temp_file, self.state_file)

    def _select_gate(self, amount):
        selected_gate = None

        for gate in sorted(
            self.config["approval_gates"],
            key=lambda item: item["threshold"]
        ):
            if amount >= gate["threshold"]:
                selected_gate = gate

        return selected_gate

    def request_approval(self, request_data):
        required_fields = ["amount", "requester", "description"]

        for field in required_fields:
            if field not in request_data or request_data[field] in [None, ""]:
                raise ValueError(f"Missing required field: {field}")

        request_id = request_data.get("request_id") or f"REQ-{uuid.uuid4().hex[:8].upper()}"
        amount = float(request_data["amount"])
        gate = self._select_gate(amount)

        if gate:
            status = "pending_approval"
            required_approvals = gate["required_approvals"]
            approvers = gate["approvers"]
            gate_name = gate["name"]
        else:
            status = "approved"
            required_approvals = 0
            approvers = []
            gate_name = "auto_approved"

        record = {
            "request_id": request_id,
            "amount": amount,
            "requester": request_data["requester"],
            "description": request_data["description"],
            "gate": gate_name,
            "authorized_approvers": approvers,
            "required_approvals": required_approvals,
            "approvals": [],
            "status": status,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        self.state["requests"][request_id] = record
        self._save_state()
        self._log_audit_event("approval_requested", record)

        return record

    def approve_request(self, request_id, approver):
        if request_id not in self.state["requests"]:
            raise ValueError(f"Request not found: {request_id}")

        request = self.state["requests"][request_id]

        if request["status"] == "approved":
            self._log_audit_event("approval_skipped", {
                "request_id": request_id,
                "approver": approver,
                "reason": "already approved"
            })
            return True

        if approver not in request["authorized_approvers"]:
            self._log_audit_event("approval_rejected", {
                "request_id": request_id,
                "approver": approver,
                "reason": "unauthorized approver"
            })
            raise PermissionError(f"Unauthorized approver: {approver}")

        if approver not in request["approvals"]:
            request["approvals"].append(approver)

        if len(request["approvals"]) >= request["required_approvals"]:
            request["status"] = "approved"

        self._save_state()
        self._log_audit_event("approval_recorded", {
            "request_id": request_id,
            "approver": approver,
            "status": request["status"],
            "approvals": request["approvals"]
        })

        return request["status"] == "approved"

    def get_request_status(self, request_id):
        if request_id not in self.state["requests"]:
            raise ValueError(f"Request not found: {request_id}")

        request = self.state["requests"][request_id]
        progress = {
            "received": len(request["approvals"]),
            "required": request["required_approvals"]
        }

        return {
            "request_id": request_id,
            "status": request["status"],
            "gate": request["gate"],
            "amount": request["amount"],
            "requester": request["requester"],
            "approvals": request["approvals"],
            "approval_progress": progress
        }

    def _log_audit_event(self, event_type, event_data):
        self.audit_logger.log_event(event_type, event_data)
