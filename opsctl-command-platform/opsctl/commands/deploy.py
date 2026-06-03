"""Deploy command implementation."""

import time
from opsctl.utils.helpers import print_success, print_error, print_info, validate_environment


def execute(args):
    """Execute the deploy command."""
    if not validate_environment(args.env):
        print_error(f"Invalid environment: {args.env}")
        print_error("Allowed environments: dev, staging, prod")
        return 2

    app_version = args.app_version or "latest"

    print_info(f"Starting deployment for application: {args.app}")
    print_info(f"Target environment: {args.env}")
    print_info(f"Application version: {app_version}")

    steps = [
        "Validating deployment inputs",
        "Preparing deployment package",
        "Checking target environment",
        "Applying deployment changes",
        "Running post-deployment verification",
    ]

    for step in steps:
        print_info(step)
        time.sleep(0.2)

    print_success(f"Deployment completed for {args.app} in {args.env}")
    return 0


def add_parser(subparsers):
    """Add deploy command parser."""
    parser = subparsers.add_parser(
        "deploy",
        help="Deploy an application to an environment",
        description="Simulate deployment of an application to dev, staging, or prod",
    )
    parser.add_argument(
        "--app",
        required=True,
        help="Application name to deploy",
    )
    parser.add_argument(
        "--env",
        required=True,
        choices=["dev", "staging", "prod"],
        help="Target environment",
    )
    parser.add_argument(
        "--version",
        dest="app_version",
        help="Application version to deploy",
        default=None,
    )
    parser.set_defaults(func=execute)
