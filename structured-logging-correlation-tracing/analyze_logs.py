import json
import sys
from collections import defaultdict

def analyze_logs(log_file):

    groups = defaultdict(list)

    with open(log_file) as f:

        for line in f:

            try:
                entry = json.loads(line)

                cid = entry.get(
                    "correlation_id",
                    "unknown"
                )

                groups[cid].append(entry)

            except Exception:
                pass

    for cid, entries in groups.items():

        print("=" * 60)
        print("Correlation ID:", cid)

        for item in entries:

            print(
                item.get("asctime"),
                item.get("message")
            )

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(
            "Usage: python analyze_logs.py logfile"
        )
    else:
        analyze_logs(sys.argv[1])
