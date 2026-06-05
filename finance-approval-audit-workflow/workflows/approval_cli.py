#!/usr/bin/env python3
import argparse
import json

from approval_engine import ApprovalEngine


def main():
    parser = argparse.ArgumentParser(description="Finance Approval System")
    parser.add_argument("action", choices=["request", "approve", "status"])
    parser.add_argument("--request-id")
    parser.add_argument("--amount", type=float)
    parser.add_argument("--requester")
    parser.add_argument("--approver")
    parser.add_argument("--description")

    args = parser.parse_args()
    engine = ApprovalEngine("config/approval_rules.yaml")

    if args.action == "request":
        result = engine.request_approval({
            "request_id": args.request_id,
            "amount": args.amount,
            "requester": args.requester,
            "description": args.description
        })
        print(json.dumps(result, indent=2))

    elif args.action == "approve":
        approved = engine.approve_request(args.request_id, args.approver)
        print(json.dumps({
            "request_id": args.request_id,
            "fully_approved": approved
        }, indent=2))

    elif args.action == "status":
        result = engine.get_request_status(args.request_id)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
