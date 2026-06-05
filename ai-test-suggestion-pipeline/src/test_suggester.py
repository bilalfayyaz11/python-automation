import subprocess
from typing import List, Dict


class TestSuggester:
    """Generates test suggestions using local AI when available, with deterministic fallback."""

    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        self.model_name = model_name

    def generate_prompt(self, function_data: Dict) -> str:
        return f"""
You are a senior Python test engineer.

Analyze this function and suggest practical unit tests.

Function name: {function_data['name']}
Parameters: {function_data['params']}
Docstring: {function_data.get('docstring')}
Complexity: {function_data['complexity']}

Return test suggestions covering:
1. Happy path
2. Edge cases
3. Error handling
4. Boundary conditions
5. Parameterized tests where useful
"""

    def call_ollama(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            return self._fallback_response()
        except Exception:
            return self._fallback_response()

    def _fallback_response(self) -> str:
        return (
            "AI model unavailable. Generated deterministic suggestions: "
            "test normal valid inputs, invalid inputs, boundary values, "
            "exception paths, and branch-specific behavior."
        )

    def parse_suggestions(self, ai_response: str) -> List[Dict]:
        return [
            {
                "type": "ai_recommendation",
                "description": ai_response
            }
        ]

    def suggest_tests(self, function_data: Dict) -> Dict:
        prompt = self.generate_prompt(function_data)
        ai_response = self.call_ollama(prompt)
        parsed = self.parse_suggestions(ai_response)

        return {
            "function": function_data["name"],
            "params": function_data["params"],
            "complexity": function_data["complexity"],
            "suggestions": parsed
        }
