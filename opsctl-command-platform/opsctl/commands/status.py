"""Status command implementation."""

import json
import os
import platform
from opsctl.utils.helpers import print_info


def _load_cpu_usage():
    try:
        load_avg = os.getloadavg()
        return {
            "load_1m": load_avg[0],
            "load_5m": load_avg[1],
            "load_15m": load_avg[2],
        }
    except OSError:
        return {
            "load_1m": None,
            "load_5m": None,
            "load_15m": None,
        }


def execute(args):
    """Execute the status command."""
    status_data = {
        "service": args.service or "all",
        "system": platform.system(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "cpu_load": _load_cpu_usage(),
        "last_deployment": "not_available",
        "health": "ok",
    }

    if args.format == "json":
        print(json.dumps(status_data, indent=2))
    else:
        print_info("System status check completed")
        print(f"Service: {status_data['service']}")
        print(f"System: {status_data['system']}")
        print(f"Hostname: {status_data['hostname']}")
        print(f"Python Version: {status_data['python_version']}")
        print(f"CPU Load 1m/5m/15m: {status_data['cpu_load']['load_1m']} / {status_data['cpu_load']['load_5m']} / {status_data['cpu_load']['load_15m']}")
        print(f"Last Deployment: {status_data['last_deployment']}")
        print(f"Health: {status_data['health']}")

    return 0


def add_parser(subparsers):
    """Add status command parser."""
    parser = subparsers.add_parser(
        "status",
        help="Check system or service status",
        description="Check operational status for the system or a specific service",
    )
    parser.add_argument(
        "--service",
        help="Optional service name to check",
        default=None,
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.set_defaults(func=execute)
