# Runbook: Disk Space Exhaustion

## Detection
```bash
df -h
df -i
du -sh /tmp/* 2>/dev/null | sort -hr | head -10
