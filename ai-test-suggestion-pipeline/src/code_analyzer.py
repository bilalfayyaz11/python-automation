import ast
import os
from typing import List, Dict
from git import Repo


class CodeAnalyzer:
    """Analyzes Python code changes and extracts function metadata."""

    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        self.repo = Repo(self.repo_path)

    def get_changed_files(self, commit_range: str = "HEAD~1..HEAD") -> List[str]:
        try:
            changed = self.repo.git.diff("--name-only", commit_range).splitlines()
        except Exception:
            changed = self.repo.git.ls_files().splitlines()

        return [
            os.path.join(self.repo_path, file)
            for file in changed
            if file.endswith(".py") and os.path.exists(os.path.join(self.repo_path, file))
        ]

    def extract_functions(self, file_path: str) -> List[Dict]:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        tree = ast.parse(content)
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "params": [arg.arg for arg in node.args.args],
                    "docstring": ast.get_docstring(node),
                    "line_number": node.lineno,
                    "complexity": self.analyze_complexity(node)
                })

        return functions

    def analyze_complexity(self, function_node: ast.FunctionDef) -> Dict:
        branches = sum(isinstance(node, (ast.If, ast.IfExp)) for node in ast.walk(function_node))
        loops = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(function_node))
        try_blocks = sum(isinstance(node, ast.Try) for node in ast.walk(function_node))
        cyclomatic_estimate = 1 + branches + loops + try_blocks

        if cyclomatic_estimate >= 6:
            risk = "high"
        elif cyclomatic_estimate >= 3:
            risk = "medium"
        else:
            risk = "low"

        return {
            "branches": branches,
            "loops": loops,
            "try_blocks": try_blocks,
            "cyclomatic_estimate": cyclomatic_estimate,
            "risk": risk
        }
