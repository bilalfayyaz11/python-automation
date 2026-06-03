"""Secure subprocess execution library.

This module provides a defensive wrapper around Python subprocess execution.
It validates commands, blocks shell metacharacters, applies timeouts, and logs
all execution attempts for auditability.
"""

import logging
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "subprocess.log"),
        logging.StreamHandler(),
    ],
)


class SafeSubprocessRunner:
    """Secure wrapper for executing approved system commands."""

    ALLOWED_COMMANDS: Set[str] = {
        "ls",
        "cat",
        "echo",
        "pwd",
        "whoami",
        "date",
        "df",
        "du",
        "grep",
        "wc",
        "sleep",
    }

    DANGEROUS_TOKENS: Set[str] = {
        ";",
        "&&",
        "||",
        "|",
        ">",
        "<",
        "`",
        "$(",
        ")",
    }

    RESTRICTED_PATHS: Set[str] = {
        "/etc/passwd",
        "/etc/shadow",
        "/etc/sudoers",
        "/root",
    }

    def __init__(self, timeout: int = 30, allowed_commands: Optional[Set[str]] = None):
        self.timeout = timeout
        self.allowed_commands = allowed_commands or self.ALLOWED_COMMANDS
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_command(self, command: Union[str, List[str]]) -> List[str]:
        """Validate and normalize a command before execution."""
        if isinstance(command, str):
            command_parts = shlex.split(command)
        elif isinstance(command, list):
            command_parts = command
        else:
            raise ValueError("Command must be a string or list of arguments")

        if not command_parts:
            raise ValueError("Command cannot be empty")

        base_command = os.path.basename(command_parts[0])

        if base_command not in self.allowed_commands:
            raise ValueError(f"Command not allowed: {base_command}")

        for part in command_parts:
            if not isinstance(part, str):
                raise ValueError("All command arguments must be strings")

            if part in self.DANGEROUS_TOKENS:
                raise ValueError(f"Dangerous shell token blocked: {part}")

            if any(token in part for token in [";", "&&", "||", "|", ">", "<", "`", "$("]):
                raise ValueError(f"Dangerous shell pattern blocked: {part}")

            if ".." in Path(part).parts:
                raise ValueError(f"Path traversal blocked: {part}")

            if part in self.RESTRICTED_PATHS:
                raise ValueError(f"Restricted path blocked: {part}")

        return command_parts

    def execute(
        self,
        command: Union[str, List[str]],
        cwd: Optional[str] = None,
        capture_output: bool = True,
    ) -> Dict[str, Any]:
        """Execute a validated command with timeout and structured output."""
        try:
            validated_command = self.validate_command(command)
            self.logger.info("Executing command: %s", validated_command)

            completed_process = subprocess.run(
                validated_command,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                timeout=self.timeout,
                check=False,
            )

            result = {
                "success": completed_process.returncode == 0,
                "returncode": completed_process.returncode,
                "stdout": completed_process.stdout if capture_output else "",
                "stderr": completed_process.stderr if capture_output else "",
                "error": None,
            }

            if completed_process.returncode != 0:
                result["error"] = completed_process.stderr.strip() or "Command failed"
                self.logger.warning("Command failed: %s", result["error"])

            return result

        except subprocess.TimeoutExpired:
            error_message = f"Command timed out after {self.timeout} seconds"
            self.logger.error(error_message)
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "error": error_message,
            }

        except Exception as error:
            error_message = str(error)
            self.logger.error("Command blocked or failed: %s", error_message)
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "error": error_message,
            }

    def execute_pipeline(self, commands: List[Union[str, List[str]]]) -> Dict[str, Any]:
        """Execute multiple validated commands sequentially."""
        results = []

        try:
            validated_commands = [self.validate_command(command) for command in commands]
        except Exception as error:
            return {
                "success": False,
                "results": results,
                "error": str(error),
            }

        for command in validated_commands:
            result = self.execute(command)
            results.append(
                {
                    "command": command,
                    "success": result["success"],
                    "returncode": result["returncode"],
                    "stdout": result["stdout"],
                    "stderr": result["stderr"],
                    "error": result["error"],
                }
            )

            if not result["success"]:
                return {
                    "success": False,
                    "results": results,
                    "error": result["error"],
                }

        return {
            "success": True,
            "results": results,
            "error": None,
        }
