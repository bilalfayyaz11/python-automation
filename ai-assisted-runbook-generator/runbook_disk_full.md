# Operational Runbook: Root filesystem is 98% full and services may fail to write logs

**Generated:** 2026-06-05T22:29:35.168245+00:00

**Hostname:** ip-172-31-10-10

**Scenario:** Root filesystem is 98% full and services may fail to write logs

## System Information

- **OS:** Ubuntu 24.04.3 LTS
- **Kernel:** 6.14.0-1018-aws

## Prerequisites

- Linux shell access
- sudo access where required
- Access to system logs
- Service ownership or escalation path

## Procedure

1. Confirm disk usage with: df -h
2. Check inode pressure with: df -i
3. Find large directories with: sudo du -xh / 2>/dev/null | sort -hr | head -20
4. Check logs with: sudo journalctl --disk-usage
5. Safely clean temporary files only after confirming ownership and impact.
6. Verify recovery with: df -h

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
