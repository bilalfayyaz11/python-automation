# Python Quality Gate Automation

## What This Does

This implementation configures automated pre-commit quality gates for Python development workflows. It enforces code formatting, linting, security scanning, JSON validation, YAML validation, file-size checks, and custom policy enforcement before code can be committed to a repository.

The solution helps prevent low-quality, insecure, or improperly formatted code from entering version control. By shifting quality checks earlier into the development lifecycle, teams can reduce review overhead, improve consistency, and catch issues before they reach CI/CD pipelines.

## Architecture

```text
+-----------------------------+
| Developer Workstation       |
| Python Source + Configs     |
+-------------+---------------+
              |
              v
+-----------------------------+
| Git Commit Attempt          |
| pre-commit hook triggered   |
+-------------+---------------+
              |
              v
+-----------------------------+
| Quality Gate Checks         |
| Black | Flake8 | Bandit     |
| JSON | YAML | File Checks   |
| Custom TODO Check           |
+-------------+---------------+
              |
              v
+-----------------------------+
| Commit Allowed or Blocked   |
| Clean code enters Git only  |
+-----------------------------+
```

## Prerequisites

- Ubuntu 24.04 or compatible Linux distribution
- Python 3.12+
- python3-pip
- python3-venv
- Git
- Internet connectivity
- Basic Git workflow knowledge

## Setup & Installation

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/python-quality-gate
cd ~/python-quality-gate

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install pre-commit
```

## How to Reproduce

```bash
git clone https://github.com/bilalfayyaz11/python-automation.git
cd python-automation/python-quality-gate

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install pre-commit

pre-commit install
pre-commit run --all-files
```

To validate enforcement:

```bash
cat > bad_code.py << 'EOF'
def bad_function(x,y):
    password="secret123"
    return x+y
EOF

git add bad_code.py
git commit -m "Test quality gate enforcement"
```

The commit should be blocked automatically.

## Tools Used

- Python 3.12
- Git
- pre-commit
- Black
- Flake8
- Bandit
- YAML Validation Hooks
- JSON Validation Hooks
- Bash Custom Hooks

## Key Skills Demonstrated

- Git hook automation
- Python code quality enforcement
- Static code analysis integration
- Security scanning implementation
- Shift-left DevSecOps practices
- Configuration management using YAML
- Developer workflow automation
- Repository governance controls

## Real-World Use Case

Organizations commonly enforce automated quality gates to ensure that all code entering shared repositories meets predefined quality and security standards. This approach reduces technical debt, improves maintainability, catches security vulnerabilities early, and creates a consistent development experience across engineering teams. Local quality gates are often combined with CI/CD pipeline validation to establish multiple layers of protection before deployment.

## Lessons Learned

- Virtual environments should never be committed to source control.
- Security scanners must be scoped correctly to avoid scanning third-party dependencies.
- Automated formatting removes style inconsistencies before code review.
- Local quality gates significantly reduce CI/CD failures.
- Custom hooks allow organizations to enforce project-specific development policies.

## Troubleshooting Log

### Virtual Environment Scanned by Bandit

Issue:

Bandit scanned the `.venv` directory and generated hundreds of findings from third-party packages.

Cause:

The virtual environment was accidentally staged with:

```bash
git add .
```

Fix:

```bash
git reset

cat > .gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
EOF

git add .gitignore
```

### Flake8 Unused Import Failure

Issue:

```text
F401 'os' imported but unused
F401 'sys' imported but unused
```

Cause:

Unused imports remained in the application.

Fix:

Remove unnecessary imports and keep only required code.

### Ubuntu 24.04 Python Package Management

Issue:

Modern Ubuntu releases use externally managed Python environments.

Cause:

Direct system-wide package installation may conflict with OS package management.

Fix:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pre-commit
```

### Pre-commit Hooks Not Executing

Fix:

```bash
pre-commit uninstall
pre-commit install
```

### Hook Version Maintenance

Update all hooks periodically:

```bash
pre-commit autoupdate
```

This ensures the latest fixes, security improvements, and compatibility updates are applied.
