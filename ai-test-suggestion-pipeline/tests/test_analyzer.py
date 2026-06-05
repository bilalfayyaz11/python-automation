import sys
sys.path.insert(0, './src')

from code_analyzer import CodeAnalyzer


def test_analyzer():
    analyzer = CodeAnalyzer('./sample_project')
    functions = analyzer.extract_functions('./sample_project/calculator.py')

    print(f"Found {len(functions)} functions")

    for func in functions:
        print(f"Function: {func['name']}")
        print(f"Parameters: {func['params']}")
        print(f"Complexity: {func['complexity']}")
        print("---")


if __name__ == "__main__":
    test_analyzer()
