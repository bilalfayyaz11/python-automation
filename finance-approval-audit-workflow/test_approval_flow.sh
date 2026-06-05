#!/bin/bash
set -e

echo "Testing Finance Approval System"

python3 workflows/approval_cli.py request \
  --request-id REQ001 \
  --amount 2000 \
  --requester dev_user \
  --description "Infrastructure deployment"

python3 workflows/approval_cli.py status --request-id REQ001

python3 workflows/approval_cli.py approve \
  --request-id REQ001 \
  --approver finance_manager

python3 workflows/approval_cli.py status --request-id REQ001

python3 workflows/approval_cli.py approve \
  --request-id REQ001 \
  --approver team_lead

python3 workflows/approval_cli.py status --request-id REQ001

python3 workflows/audit_query.py --days 1

python3 workflows/audit_query.py --report --days 7
