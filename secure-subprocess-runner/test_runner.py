#!/usr/bin/env python3
"""Test suite for SafeSubprocessRunner."""

from safe_runner import SafeSubprocessRunner


def print_result(name, result):
    """Print a readable test result."""
    status = "PASS" if result["success"] else "BLOCKED/FAILED"
    print(f"{name}: {status}")
    print(f"Return Code: {result['returncode']}")
    if result.get("stdout"):
        print(f"STDOUT: {result['stdout'].strip()}")
    if result.get("stderr"):
        print(f"STDERR: {result['stderr'].strip()}")
    if result.get("error"):
        print(f"ERROR: {result['error']}")
    print("-" * 60)


def test_basic_execution():
    """Test allowed command execution."""
    runner = SafeSubprocessRunner(timeout=10)

    print("Basic execution tests:")
    print_result("ls -la", runner.execute("ls -la"))
    print_result("echo Hello World", runner.execute('echo "Hello World"'))
    print_result("pwd", runner.execute("pwd"))


def test_validation():
    """Test input validation and security controls."""
    runner = SafeSubprocessRunner(timeout=10)

    print("\nValidation tests:")
    print_result("Injection attempt", runner.execute("ls; rm -rf /"))
    print_result("Pipe attempt", runner.execute("echo test | grep test"))
    print_result("Non-whitelisted command", runner.execute("rm -rf /"))
    print_result("Restricted file read", runner.execute("cat /etc/passwd"))


def test_timeout():
    """Test timeout handling."""
    runner = SafeSubprocessRunner(timeout=2)

    print("\nTimeout tests:")
    print_result("sleep 5", runner.execute("sleep 5"))


def test_error_handling():
    """Test graceful handling of normal command errors."""
    runner = SafeSubprocessRunner(timeout=10)

    print("\nError handling tests:")
    print_result("Missing file", runner.execute("cat missing-file.txt"))
    print_result("Invalid ls argument", runner.execute("ls --invalid-option"))


def test_pipeline():
    """Test sequential execution of multiple commands."""
    runner = SafeSubprocessRunner(timeout=10)

    print("\nPipeline tests:")
    pipeline_result = runner.execute_pipeline([
        "pwd",
        "whoami",
        "date",
    ])

    print(f"Pipeline success: {pipeline_result['success']}")
    for item in pipeline_result["results"]:
        print(f"Command: {' '.join(item['command'])}")
        print(f"Success: {item['success']}")
        print(f"Output: {item['stdout'].strip()}")
        print("-" * 60)


if __name__ == "__main__":
    test_basic_execution()
    test_validation()
    test_timeout()
    test_error_handling()
    test_pipeline()
