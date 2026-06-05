# Post-Incident Report

## Executive Summary
- Incident Date:
- Duration:
- Severity:
- Services Affected:
- User Impact:

## Timeline
| Time | Event |
|------|-------|
| | Incident began |
| | Incident detected |
| | Response initiated |
| | Root cause identified |
| | Resolution applied |
| | Service restored |
| | Incident closed |

## Root Cause Analysis

### What Happened
Document the technical failure.

### Why It Happened
Document the underlying cause.

### Contributing Factors
- Missing validation
- Lack of automated alerting
- Manual operational risk

## Response Evaluation

### What Went Well
- Structured runbook was available.
- System state was captured before and after resolution.

### What Could Be Improved
- Add automated alerts.
- Add safer pre-checks before service changes.

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add monitoring alerts | Platform Engineer | Next sprint | Open |
| Automate recovery checks | Platform Engineer | Next sprint | Open |

## Lessons Learned
1. Controlled drills improve response speed.
2. Logs and baselines reduce guesswork.
3. Safe rollback paths are essential.

## Preventive Measures
- Add service health checks.
- Monitor disk and CPU thresholds.
- Validate Nginx config before reload.
