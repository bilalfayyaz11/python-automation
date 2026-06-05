#!/usr/bin/env python3

import sys
import yaml
from pathlib import Path
from colorama import Fore, init

init(autoreset=True)

class CITriageAssistant:
    def __init__(self, patterns_file):
        self.patterns = self._load_patterns(patterns_file)
        self.log_content = ""
        self.matches = []

    def _load_patterns(self, patterns_file):
        with open(patterns_file, "r") as file:
            data = yaml.safe_load(file)
            return data.get("patterns", [])

    def analyze_log(self, log_file):
        with open(log_file, "r") as file:
            self.log_content = file.read().lower()

        self.matches = []

        for pattern in self.patterns:
            match_count = 0
            matched_keywords = []

            for keyword in pattern["keywords"]:
                count = self.log_content.count(keyword.lower())
                if count > 0:
                    match_count += count
                    matched_keywords.append(keyword)

            if match_count > 0:
                self.matches.append({
                    "pattern": pattern,
                    "score": match_count,
                    "matched_keywords": matched_keywords
                })

        self.matches.sort(key=lambda item: item["score"], reverse=True)
        return self.matches

    def extract_error_lines(self, log_file, context_lines=2):
        error_snippets = []

        with open(log_file, "r") as file:
            lines = file.readlines()

        for index, line in enumerate(lines):
            if "ERROR" in line or "FATAL" in line or "FAIL" in line:
                start = max(0, index - context_lines)
                end = min(len(lines), index + context_lines + 1)
                snippet = "".join(lines[start:end])
                if snippet not in error_snippets:
                    error_snippets.append(snippet)

        return error_snippets

    def generate_report_text(self, log_file):
        lines = []
        lines.append("=" * 70)
        lines.append("CI FAILURE TRIAGE REPORT")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Log File: {log_file}")
        lines.append("")

        if not self.matches:
            lines.append("No known failure patterns detected.")
            lines.append("Manual investigation required.")
            return "\n".join(lines)

        lines.append("Detected Failure Patterns:")
        lines.append("")

        for index, match in enumerate(self.matches, 1):
            pattern = match["pattern"]
            lines.append(f"{index}. {pattern['name']}")
            lines.append(f"   Severity: {pattern['severity'].upper()}")
            lines.append(f"   Confidence Score: {match['score']}")
            lines.append(f"   Matched Keywords: {', '.join(match['matched_keywords'])}")
            lines.append("")
            lines.append("   Suggested Actions:")
            for suggestion in pattern["suggestions"]:
                lines.append(f"   - {suggestion}")
            lines.append("")

        lines.append("Error Context from Log:")
        lines.append("")

        for snippet in self.extract_error_lines(log_file)[:3]:
            lines.append(snippet.strip())
            lines.append("-" * 70)

        return "\n".join(lines)

    def generate_report(self, log_file):
        report = self.generate_report_text(log_file)

        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}CI FAILURE TRIAGE REPORT")
        print(f"{Fore.CYAN}{'='*70}\n")
        print(f"{Fore.YELLOW}Log File: {Fore.WHITE}{log_file}\n")

        if not self.matches:
            print(f"{Fore.RED}No known failure patterns detected.")
            print(f"{Fore.YELLOW}Manual investigation required.\n")
            return report

        print(f"{Fore.GREEN}Detected Failure Patterns:\n")

        for index, match in enumerate(self.matches, 1):
            pattern = match["pattern"]
            severity_color = self._get_severity_color(pattern["severity"])

            print(f"{Fore.WHITE}{index}. {Fore.CYAN}{pattern['name']}")
            print(f"   {Fore.WHITE}Severity: {severity_color}{pattern['severity'].upper()}")
            print(f"   {Fore.WHITE}Confidence Score: {Fore.YELLOW}{match['score']}")
            print(f"   {Fore.WHITE}Matched Keywords: {Fore.MAGENTA}{', '.join(match['matched_keywords'])}\n")

            print(f"   {Fore.GREEN}Suggested Actions:")
            for suggestion in pattern["suggestions"]:
                print(f"   {Fore.WHITE}- {suggestion}")
            print()

        print(f"{Fore.YELLOW}Error Context from Log:\n")

        for snippet in self.extract_error_lines(log_file)[:3]:
            print(f"{Fore.RED}{snippet}")
            print(f"{Fore.WHITE}{'-'*70}\n")

        return report

    def _get_severity_color(self, severity):
        colors = {
            "critical": Fore.RED,
            "high": Fore.RED,
            "medium": Fore.YELLOW,
            "low": Fore.GREEN
        }
        return colors.get(severity.lower(), Fore.WHITE)

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python3 ci_triage.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    patterns_file = "patterns/failure_patterns.yaml"

    if not Path(log_file).exists():
        print(f"{Fore.RED}Error: Log file not found: {log_file}")
        sys.exit(1)

    assistant = CITriageAssistant(patterns_file)
    assistant.analyze_log(log_file)
    report = assistant.generate_report(log_file)

    Path("output").mkdir(exist_ok=True)
    output_file = Path("output") / f"{Path(log_file).stem}_triage_report.txt"
    output_file.write_text(report)

if __name__ == "__main__":
    main()
