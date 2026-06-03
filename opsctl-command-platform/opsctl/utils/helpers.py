"""Helper utilities for opsctl."""

import sys


def print_success(message):
    """Print success message in green."""
    print(f"\033[92m[SUCCESS]\033[0m {message}")


def print_error(message):
    """Print error message in red."""
    print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)


def print_info(message):
    """Print info message in blue."""
    print(f"\033[94m[INFO]\033[0m {message}")


def validate_environment(env):
    """Validate environment parameter."""
    allowed_environments = {"dev", "staging", "prod"}
    return env in allowed_environments
