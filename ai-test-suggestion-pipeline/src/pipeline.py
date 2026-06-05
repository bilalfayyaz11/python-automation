import argparse
import json
import os
from code_analyzer import CodeAnalyzer
from test_suggester import TestSuggester


class TestSuggestionPipeline:
    """Orchestrates code analysis and AI-powered test suggestion generation."""

    def __init__(self, repo_path: str, output_dir: str = "./suggestions"):
        self.repo_path = repo_path
        self.analyzer = CodeAnalyzer(repo_path)
        self.suggester = TestSuggester()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def run(self, commit_range: str = "HEAD~1..HEAD") -> dict:
        changed_files = self.analyzer.get_changed_files(commit_range)
        all_suggestions = {
            "repository": self.repo_path,
            "commit_range": commit_range,
            "files_analyzed": [],
            "total_functions": 0,
            "suggestions": {}
        }

        for file_path in changed_files:
            functions = self.analyzer.extract_functions(file_path)
            relative_path = os.path.relpath(file_path, self.repo_path)
            all_suggestions["files_analyzed"].append(relative_path)
            all_suggestions["suggestions"][relative_path] = []

            for function in functions:
                suggestion = self.suggester.suggest_tests(function)
                all_suggestions["suggestions"][relative_path].append(suggestion)
                all_suggestions["total_functions"] += 1

        json_path = os.path.join(self.output_dir, "test_suggestions.json")
        report_path = os.path.join(self.output_dir, "report.md")

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(all_suggestions, file, indent=2)

        with open(report_path, "w", encoding="utf-8") as file:
            file.write(self.generate_report(all_suggestions))

        return all_suggestions

    def generate_report(self, suggestions: dict) -> str:
        lines = []
        lines.append("# AI Test Suggestion Report")
        lines.append("")
        lines.append(f"Repository: `{suggestions['repository']}`")
        lines.append(f"Commit Range: `{suggestions['commit_range']}`")
        lines.append(f"Files Analyzed: {len(suggestions['files_analyzed'])}")
        lines.append(f"Functions Analyzed: {suggestions['total_functions']}")
        lines.append("")

        for file_path, items in suggestions["suggestions"].items():
            lines.append(f"## File: {file_path}")
            lines.append("")

            for item in items:
                lines.append(f"### Function: `{item['function']}`")
                lines.append(f"- Parameters: `{item['params']}`")
                lines.append(f"- Complexity: `{item['complexity']}`")
                lines.append("")
                lines.append("Suggested Tests:")
                for suggestion in item["suggestions"]:
                    lines.append(f"- {suggestion['description']}")
                lines.append("")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI-powered test suggestion pipeline")
    parser.add_argument("--repo", required=True, help="Path to git repository")
    parser.add_argument("--output", default="./suggestions", help="Output directory")
    parser.add_argument("--commit-range", default="HEAD~1..HEAD", help="Git commit range")
    args = parser.parse_args()

    pipeline = TestSuggestionPipeline(args.repo, args.output)
    result = pipeline.run(args.commit_range)

    print("AI test suggestion pipeline completed.")
    print(f"Files analyzed: {len(result['files_analyzed'])}")
    print(f"Functions analyzed: {result['total_functions']}")
    print(f"Output directory: {args.output}")


if __name__ == "__main__":
    main()
