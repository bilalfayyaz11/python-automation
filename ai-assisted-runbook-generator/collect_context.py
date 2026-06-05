#!/usr/bin/env python3

import subprocess
import json
import socket
from datetime import datetime, UTC

class SystemContextCollector:
    def __init__(self):
        self.context = {
            "timestamp": datetime.now(UTC).isoformat(),
            "hostname": socket.gethostname(),
            "system_info": {},
            "services": [],
            "network": {},
            "disk": {}
        }

    def run_command(self, command):
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        return {
            "command": " ".join(command),
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

    def collect_system_info(self):
        os_release = {}

        try:
            with open("/etc/os-release", "r") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        os_release[key] = value.strip('"')
        except FileNotFoundError:
            os_release["error"] = "/etc/os-release not found"

        kernel = self.run_command(["uname", "-r"])
        cpu = self.run_command(["lscpu"])
        memory = self.run_command(["free", "-h"])

        self.context["system_info"] = {
            "os_release": os_release,
            "kernel": kernel["stdout"],
            "cpu": cpu["stdout"],
            "memory": memory["stdout"]
        }

    def collect_service_status(self, services):
        for service in services:
            is_active = self.run_command(["systemctl", "is-active", service])
            status = self.run_command(["systemctl", "status", service, "--no-pager"])

            self.context["services"].append({
                "name": service,
                "active_state": is_active["stdout"],
                "status_summary": "\n".join(status["stdout"].splitlines()[:12]),
                "exit_code": is_active["exit_code"]
            })

    def collect_network_info(self):
        ip_addresses = self.run_command(["ip", "-brief", "addr"])
        listening_ports = self.run_command(["ss", "-tlnp"])

        self.context["network"] = {
            "interfaces": ip_addresses["stdout"],
            "listening_ports": listening_ports["stdout"]
        }

    def collect_disk_info(self):
        disk_usage = self.run_command(["df", "-h"])
        inode_usage = self.run_command(["df", "-i"])

        self.context["disk"] = {
            "disk_usage": disk_usage["stdout"],
            "inode_usage": inode_usage["stdout"]
        }

    def export_context(self, filename="system_context.json"):
        with open(filename, "w") as file:
            json.dump(self.context, file, indent=2)
        return filename

if __name__ == "__main__":
    collector = SystemContextCollector()
    collector.collect_system_info()
    collector.collect_service_status(["ssh", "cron", "systemd-journald"])
    collector.collect_network_info()
    collector.collect_disk_info()
    output = collector.export_context()
    print(f"Context collection complete: {output}")
