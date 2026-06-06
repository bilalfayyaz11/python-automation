#!/usr/bin/env python3
"""
Compliance Evidence Collector
Collects Linux system evidence for compliance reporting.
"""

import json
import yaml
import subprocess
from datetime import datetime
from pathlib import Path


class EvidenceCollector:
    def __init__(self, config_path):
        self.config_path = Path(config_path).resolve()
        self.base_dir = self.config_path.parent.parent
        self.output_dir = self.base_dir / "output"
        self.logs_dir = self.base_dir / "logs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    def run_command(self, command, description):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=20
            )

            return {
                "description": description,
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "status": "success" if result.returncode == 0 else "warning"
            }
        except Exception as exc:
            return {
                "description": description,
                "command": command,
                "return_code": -1,
                "stdout": "",
                "stderr": str(exc),
                "status": "error"
            }

    def collect_system_logs(self):
        evidence = {
            "timestamp": datetime.now().isoformat(),
            "evidence_type": "system_logs",
            "data": []
        }

        evidence["data"].append(
            self.run_command(
                "journalctl -n 100 --no-pager",
                "Recent system journal logs"
            )
        )

        evidence["data"].append(
            self.run_command(
                "systemctl list-units --type=service --state=running --no-pager",
                "Running system services"
            )
        )

        evidence["data"].append(
            self.run_command(
                "logger -t compliance-evidence 'System log evidence collection executed' && journalctl -t compliance-evidence -n 10 --no-pager",
                "Compliance-specific system log events"
            )
        )

        return evidence

    def collect_access_logs(self):
        evidence = {
            "timestamp": datetime.now().isoformat(),
            "evidence_type": "access_logs",
            "data": []
        }

        evidence["data"].append(
            self.run_command(
                "last -n 50",
                "Recent login sessions"
            )
        )

        evidence["data"].append(
            self.run_command(
                "who",
                "Currently logged-in users"
            )
        )

        evidence["data"].append(
            self.run_command(
                "lastb -n 20 2>/dev/null || true",
                "Recent failed login attempts"
            )
        )

        evidence["data"].append(
            self.run_command(
                "getent passwd | head -30",
                "Local user account snapshot"
            )
        )

        return evidence

    def collect_configuration_snapshot(self):
        evidence = {
            "timestamp": datetime.now().isoformat(),
            "evidence_type": "configuration_snapshots",
            "data": []
        }

        evidence["data"].append(
            self.run_command(
                "hostnamectl",
                "Host identity and operating system details"
            )
        )

        evidence["data"].append(
            self.run_command(
                "ip addr",
                "Network interface configuration"
            )
        )

        evidence["data"].append(
            self.run_command(
                "sudo iptables -L -n 2>/dev/null || sudo nft list ruleset 2>/dev/null || true",
                "Firewall rules snapshot"
            )
        )

        evidence["data"].append(
            self.run_command(
                "dpkg -l | head -50",
                "Installed package inventory sample"
            )
        )

        evidence["data"].append(
            self.run_command(
                "uname -a",
                "Kernel and platform information"
            )
        )

        return evidence

    def collect_security_events(self):
        evidence = {
            "timestamp": datetime.now().isoformat(),
            "evidence_type": "security_events",
            "data": []
        }

        evidence["data"].append(
            self.run_command(
                "journalctl -p warning -n 50 --no-pager",
                "Recent warning-level system events"
            )
        )

        evidence["data"].append(
            self.run_command(
                "find /etc -maxdepth 1 -type f -name '*conf' | head -20",
                "Security-relevant configuration files"
            )
        )

        evidence["data"].append(
            self.run_command(
                "systemctl list-unit-files --state=enabled --no-pager | head -50",
                "Enabled service inventory"
            )
        )

        return evidence


if __name__ == "__main__":
    collector = EvidenceCollector("../config/compliance_config.yaml")
    print(json.dumps([
        collector.collect_system_logs(),
        collector.collect_access_logs(),
        collector.collect_configuration_snapshot(),
        collector.collect_security_events()
    ], indent=2))
