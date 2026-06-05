#!/usr/bin/env python3

import json
import requests
import yaml
from jinja2 import Template
from datetime import datetime, UTC

class RunbookGenerator:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "llama3.2:1b"

    def load_context(self, context_file):
        with open(context_file, "r") as file:
            return json.load(file)

    def create_prompt(self, context, scenario):
        os_info = context.get("system_info", {}).get("os_release", {})
        hostname = context.get("hostname", "unknown")
        kernel = context.get("system_info", {}).get("kernel", "unknown")
        disk = "\n".join(context.get("disk", {}).get("disk_usage", "unknown").splitlines()[:6])
        network = "\n".join(context.get("network", {}).get("listening_ports", "unknown").splitlines()[:12])

        prompt = f"""
You are an expert SRE and AIOps engineer.

Generate a clear operational runbook for this incident scenario:

Scenario:
{scenario}

System context:
Hostname: {hostname}
OS: {os_info.get("PRETTY_NAME", "unknown")}
Kernel: {kernel}

Disk usage:
{disk}

Listening ports:
{network}

Write a concise production runbook with:
1. Summary
2. Triage commands
3. Resolution steps
4. Verification
5. Escalation

Rules:
- Maximum 350 words.
- Use practical Linux commands.
- Keep steps numbered.
- Avoid destructive commands.
"""
        return prompt.strip()

    def generate_with_ai(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 220,
                "temperature": 0.2,
                "num_ctx": 1024
            }
        }

        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json=payload,
            timeout=90
        )

        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    def format_runbook(self, ai_output, context, scenario):
        os_info = context.get("system_info", {}).get("os_release", {})

        runbook = {
            "title": f"Operational Runbook: {scenario}",
            "created": datetime.now(UTC).isoformat(),
            "hostname": context.get("hostname", "unknown"),
            "scenario": scenario,
            "system": {
                "os_version": os_info.get("PRETTY_NAME", "unknown"),
                "kernel": context.get("system_info", {}).get("kernel", "unknown"),
                "memory": context.get("system_info", {}).get("memory", "unknown")
            },
            "ai_generated_procedure": ai_output,
            "verification": [
                "Confirm affected service or resource is stable.",
                "Review system logs for repeated errors.",
                "Validate CPU, memory, disk, and network state.",
                "Document actions taken and update the runbook if needed."
            ],
            "rollback": [
                "Revert the last risky operational change if the issue worsens.",
                "Escalate to senior platform or infrastructure engineering if recovery fails.",
                "Preserve logs and command output before major remediation."
            ]
        }

        return runbook

    def export_runbook(self, runbook, output_name, output_format="markdown"):
        if output_format == "yaml":
            filename = f"{output_name}.yaml"
            with open(filename, "w") as file:
                yaml.safe_dump(runbook, file, sort_keys=False)
            return filename

        filename = f"{output_name}.md"

        with open("runbook_template.md", "r") as file:
            template = Template(file.read())

        rendered = template.render(
            title=runbook["title"],
            created=runbook["created"],
            hostname=runbook["hostname"],
            scenario=runbook["scenario"],
            os_version=runbook["system"]["os_version"],
            kernel=runbook["system"]["kernel"],
            memory=runbook["system"]["memory"],
            procedure=runbook["ai_generated_procedure"],
            verification="\n".join(f"- {item}" for item in runbook["verification"]),
            rollback="\n".join(f"- {item}" for item in runbook["rollback"]),
            prerequisites="- Linux shell access\n- sudo privileges if required\n- Access to system logs and service status"
        )

        with open(filename, "w") as file:
            file.write(rendered)

        return filename
