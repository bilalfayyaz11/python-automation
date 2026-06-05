# Operational Runbook: CPU usage is at 95% and application response time is degraded

**Generated:** 2026-06-05T22:29:34.976166+00:00

**Hostname:** ip-172-31-10-10

**Scenario:** CPU usage is at 95% and application response time is degraded

## System Information

- **OS:** Ubuntu 24.04.3 LTS
- **Kernel:** 6.14.0-1018-aws

## Prerequisites

- Linux shell access
- sudo access where required
- Access to system logs
- Service ownership or escalation path

## Procedure

1. Confirm current CPU load with: top -bn1 | head -20
2. Identify expensive processes with: ps aux --sort=-%cpu | head -10
3. Check system load with: uptime
4. Review service logs with: journalctl -xe --no-pager | tail -50
5. If one process is clearly runaway, document PID before restarting or stopping it.
6. Verify recovery with: top -bn1 | head -10

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
