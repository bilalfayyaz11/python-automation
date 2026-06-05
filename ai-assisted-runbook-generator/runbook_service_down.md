# Operational Runbook: A web service is not responding to requests

**Generated:** 2026-06-05T22:29:35.362953+00:00

**Hostname:** ip-172-31-10-10

**Scenario:** A web service is not responding to requests

## System Information

- **OS:** Ubuntu 24.04.3 LTS
- **Kernel:** 6.14.0-1018-aws

## Prerequisites

- Linux shell access
- sudo access where required
- Access to system logs
- Service ownership or escalation path

## Procedure

1. Confirm service status with: systemctl status <service> --no-pager
2. Check listening ports with: ss -tlnp
3. Review recent logs with: journalctl -u <service> -n 50 --no-pager
4. Validate configuration before restart.
5. Restart service only after confirming the failure cause.
6. Verify recovery with curl or service-specific health check.

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
