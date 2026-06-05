#!/usr/bin/env python3

from collect_context import SystemContextCollector
from datetime import datetime, UTC
import yaml
import sys

SCENARIOS = {
    "high_cpu": "CPU usage is at 95% and application response time is degraded",
    "disk_full": "Root filesystem is 98% full and services may fail to write logs",
    "service_down": "A web service is not responding to requests"
}

PROCEDURES = {
    "high_cpu": """
1. Confirm current CPU load with: top -bn1 | head -20
2. Identify expensive processes with: ps aux --sort=-%cpu | head -10
3. Check system load with: uptime
4. Review service logs with: journalctl -xe --no-pager | tail -50
5. If one process is clearly runaway, document PID before restarting or stopping it.
6. Verify recovery with: top -bn1 | head -10
""",
    "disk_full": """
1. Confirm disk usage with: df -h
2. Check inode pressure with: df -i
3. Find large directories with: sudo du -xh / 2>/dev/null | sort -hr | head -20
4. Check logs with: sudo journalctl --disk-usage
5. Safely clean temporary files only after confirming ownership and impact.
6. Verify recovery with: df -h
""",
    "service_down": """
1. Confirm service status with: systemctl status <service> --no-pager
2. Check listening ports with: ss -tlnp
3. Review recent logs with: journalctl -u <service> -n 50 --no-pager
4. Validate configuration before restart.
5. Restart service only after confirming the failure cause.
6. Verify recovery with curl or service-specific health check.
"""
}

def write_outputs(key, context):
    scenario = SCENARIOS[key]
    procedure = PROCEDURES[key].strip()
    created = datetime.now(UTC).isoformat()
    os_version = context["system_info"]["os_release"].get("PRETTY_NAME", "unknown")
    kernel = context["system_info"].get("kernel", "unknown")
    hostname = context.get("hostname", "unknown")

    md = f"""# Operational Runbook: {scenario}

**Generated:** {created}

**Hostname:** {hostname}

**Scenario:** {scenario}

## System Information

- **OS:** {os_version}
- **Kernel:** {kernel}

## Prerequisites

- Linux shell access
- sudo access where required
- Access to system logs
- Service ownership or escalation path

## Procedure

{procedure}

## Verification Steps

- Confirm the affected resource is stable.
- Review system logs for repeated errors.
- Validate CPU, memory, disk, and network state.
- Document the root cause and recovery action.

## Rollback Procedure

- Revert the last risky operational change if the issue worsens.
- Preserve logs before major remediation.
- Escalate to senior platform engineering if recovery fails.

---

Generated through local runbook automation workflow.
"""

    data = {
        "title": f"Operational Runbook: {scenario}",
        "created": created,
        "hostname": hostname,
        "scenario": scenario,
        "system": {
            "os_version": os_version,
            "kernel": kernel
        },
        "procedure": procedure,
        "verification": [
            "Confirm affected resource is stable",
            "Review logs for repeated errors",
            "Validate system state",
            "Document root cause"
        ],
        "rollback": [
            "Revert risky changes",
            "Preserve evidence",
            "Escalate if recovery fails"
        ]
    }

    with open(f"runbook_{key}.md", "w") as file:
        file.write(md)

    with open(f"runbook_{key}.yaml", "w") as file:
        yaml.safe_dump(data, file, sort_keys=False)

def main():
    key = sys.argv[1] if len(sys.argv) > 1 else "high_cpu"

    if key not in SCENARIOS:
        print("Available scenarios:", ", ".join(SCENARIOS))
        sys.exit(1)

    collector = SystemContextCollector()
    collector.collect_system_info()
    collector.collect_service_status(["ssh", "cron", "systemd-journald"])
    collector.collect_network_info()
    collector.collect_disk_info()
    collector.export_context()

    write_outputs(key, collector.context)

    print("Runbook generated successfully")
    print("Scenario:", key)
    print("Markdown:", f"runbook_{key}.md")
    print("YAML:", f"runbook_{key}.yaml")

if __name__ == "__main__":
    main()
