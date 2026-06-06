#!/usr/bin/env python3
"""
Main Compliance Workflow Orchestrator
Coordinates evidence collection, reporting, and audit logging.
"""

from pathlib import Path
from evidence_collector import EvidenceCollector
from report_generator import ComplianceReportGenerator
from audit_logger import AuditLogger


class ComplianceWorkflow:
    def __init__(self, config_path):
        self.config_path = Path(config_path).resolve()
        self.base_dir = self.config_path.parent.parent
        self.collector = EvidenceCollector(self.config_path)
        self.audit_logger = AuditLogger(self.base_dir / "logs")

    def run_full_compliance_cycle(self):
        results = {
            "evidence_collected": [],
            "reports_generated": [],
            "audit_summary": {},
            "errors": []
        }

        collection_methods = [
            ("system_logs", self.collector.collect_system_logs),
            ("access_logs", self.collector.collect_access_logs),
            ("configuration_snapshots", self.collector.collect_configuration_snapshot),
            ("security_events", self.collector.collect_security_events)
        ]

        evidence_data = []

        for evidence_type, method in collection_methods:
            try:
                evidence = method()
                evidence_data.append(evidence)
                results["evidence_collected"].append(evidence_type)
                self.audit_logger.log_evidence_collection(
                    evidence_type,
                    "success",
                    {"records": len(evidence.get("data", []))}
                )
            except Exception as exc:
                results["errors"].append({"stage": evidence_type, "error": str(exc)})
                self.audit_logger.log_evidence_collection(evidence_type, "error", {"error": str(exc)})

        try:
            generator = ComplianceReportGenerator(evidence_data, self.base_dir / "output")
            json_report = generator.generate_json_report()
            html_report = generator.generate_html_report()
            csv_report = generator.generate_csv_report()

            for report_type, path in [
                ("json", json_report),
                ("html", html_report),
                ("csv", csv_report)
            ]:
                results["reports_generated"].append(path)
                self.audit_logger.log_report_generation(report_type, path, "success")

        except Exception as exc:
            results["errors"].append({"stage": "report_generation", "error": str(exc)})
            self.audit_logger.log_report_generation("all", "", "error")

        results["audit_summary"] = self.audit_logger.generate_audit_summary()
        return results

    def display_summary(self, results):
        print("\n============================================================")
        print("COMPLIANCE EVIDENCE GENERATION SUMMARY")
        print("============================================================")

        print("\nEvidence Collected:")
        for item in results["evidence_collected"]:
            print(f"  - {item}")

        print("\nReports Generated:")
        for report in results["reports_generated"]:
            print(f"  - {report}")

        print("\nAudit Summary:")
        for key, value in results["audit_summary"].items():
            print(f"  - {key}: {value}")

        if results["errors"]:
            print("\nErrors:")
            for error in results["errors"]:
                print(f"  - {error}")
        else:
            print("\nErrors: None")

        print("============================================================")


def main():
    config_path = "../config/compliance_config.yaml"
    workflow = ComplianceWorkflow(config_path)
    results = workflow.run_full_compliance_cycle()
    workflow.display_summary(results)

    print("\nCompliance workflow completed.")
    print("Check the following directories:")
    print("  - output/ for generated reports")
    print("  - logs/ for audit logs")


if __name__ == "__main__":
    main()
