#!/usr/bin/env python3
"""
Compliance Report Generator
Generates JSON, HTML, and CSV reports from evidence.
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from collections import Counter


class ComplianceReportGenerator:
    def __init__(self, evidence_data, output_dir="../output"):
        self.evidence_data = evidence_data
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_summary(self):
        evidence_types = [item.get("evidence_type", "unknown") for item in self.evidence_data]
        total_commands = sum(len(item.get("data", [])) for item in self.evidence_data)

        status_counter = Counter()
        for item in self.evidence_data:
            for record in item.get("data", []):
                status_counter[record.get("status", "unknown")] += 1

        return {
            "total_evidence_groups": len(self.evidence_data),
            "total_evidence_records": total_commands,
            "evidence_by_type": dict(Counter(evidence_types)),
            "status_counts": dict(status_counter)
        }

    def generate_json_report(self, filename="compliance_report.json"):
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "compliance_evidence",
                "version": "1.0"
            },
            "evidence_summary": self.build_summary(),
            "evidence_items": self.evidence_data
        }

        output_path = self.output_dir / filename
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)

        return str(output_path)

    def generate_html_report(self, filename="compliance_report.html"):
        summary = self.build_summary()
        rows = ""

        for evidence_group in self.evidence_data:
            evidence_type = evidence_group.get("evidence_type", "unknown")
            for record in evidence_group.get("data", []):
                rows += f"""
                <tr>
                    <td>{evidence_group.get("timestamp", "")}</td>
                    <td>{evidence_type}</td>
                    <td>{record.get("description", "")}</td>
                    <td>{record.get("status", "")}</td>
                    <td><pre>{record.get("stdout", "")[:1000]}</pre></td>
                </tr>
                """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Compliance Evidence Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }}
                th {{ background-color: #4CAF50; color: white; }}
                pre {{ white-space: pre-wrap; max-height: 250px; overflow: auto; }}
            </style>
        </head>
        <body>
            <h1>Compliance Evidence Report</h1>
            <p>Generated: {datetime.now().isoformat()}</p>

            <h2>Evidence Summary</h2>
            <ul>
                <li>Total Evidence Groups: {summary["total_evidence_groups"]}</li>
                <li>Total Evidence Records: {summary["total_evidence_records"]}</li>
                <li>Status Counts: {summary["status_counts"]}</li>
                <li>Evidence Types: {summary["evidence_by_type"]}</li>
            </ul>

            <h2>Detailed Evidence</h2>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Evidence Type</th>
                    <th>Description</th>
                    <th>Status</th>
                    <th>Output Preview</th>
                </tr>
                {rows}
            </table>
        </body>
        </html>
        """

        output_path = self.output_dir / filename
        output_path.write_text(html, encoding="utf-8")
        return str(output_path)

    def generate_csv_report(self, filename="compliance_report.csv"):
        output_path = self.output_dir / filename

        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["timestamp", "evidence_type", "description", "status", "return_code", "command"]
            )
            writer.writeheader()

            for evidence_group in self.evidence_data:
                for record in evidence_group.get("data", []):
                    writer.writerow({
                        "timestamp": evidence_group.get("timestamp", ""),
                        "evidence_type": evidence_group.get("evidence_type", ""),
                        "description": record.get("description", ""),
                        "status": record.get("status", ""),
                        "return_code": record.get("return_code", ""),
                        "command": record.get("command", "")
                    })

        return str(output_path)


if __name__ == "__main__":
    sample = [
        {
            "timestamp": datetime.now().isoformat(),
            "evidence_type": "sample",
            "data": [{"description": "sample check", "status": "success", "return_code": 0, "command": "echo test", "stdout": "test"}]
        }
    ]
    generator = ComplianceReportGenerator(sample)
    print(generator.generate_json_report())
    print(generator.generate_html_report())
    print(generator.generate_csv_report())
