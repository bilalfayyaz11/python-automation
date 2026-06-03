#!/usr/bin/env python3
"""Practical examples for SafeSubprocessRunner."""

from safe_runner import SafeSubprocessRunner


def print_section(title):
    """Print section heading."""
    print(f"\n=== {title} ===")


def print_output(label, result):
    """Print command output cleanly."""
    print(f"\n{label}")
    print(f"Success: {result['success']}")
    if result.get("stdout"):
        print(result["stdout"].strip())
    if result.get("error"):
        print(f"Error: {result['error']}")


def example_system_info():
    """Gather system information safely."""
    runner = SafeSubprocessRunner(timeout=10)

    print_output("Current user:", runner.execute("whoami"))
    print_output("Current directory:", runner.execute("pwd"))
    print_output("Current date:", runner.execute("date"))
    print_output("Disk usage:", runner.execute("df -h"))


def example_file_operations():
    """Perform safe file operations."""
    runner = SafeSubprocessRunner(timeout=10)

    print_output("Files in current directory:", runner.execute("ls -la"))
    print_output("Line count for safe_runner.py:", runner.execute("wc -l safe_runner.py"))
    print_output("Search for class definition:", runner.execute("grep SafeSubprocessRunner safe_runner.py"))


if __name__ == "__main__":
    print_section("System Information")
    example_system_info()

    print_section("File Operations")
    example_file_operations()
