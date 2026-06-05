#!/usr/bin/env python3
import argparse
import json

from audit_logger import AuditLogger


def main():
    parser = argparse.ArgumentParser(description="Audit Log Query Tool")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--event-type")
    parser.add_argument("--user")
    parser.add_argument("--report", action="store_true")

    args = parser.parse_args()
    logger = AuditLogger("logs")

    if args.report:
        print(json.dumps(logger.generate_report(), indent=2))
        return

    records = logger.query_logs({
        "event_type": args.event_type,
        "user": args.user
    })

    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
