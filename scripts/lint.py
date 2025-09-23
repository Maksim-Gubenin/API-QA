"""
Linter Runner Module

This module provides automated execution of multiple code quality tools
for Python projects. It runs a series of linters and formatters in sequence
and exits with an appropriate status code if any checks fail.

The module is designed to be used as part of a CI/CD pipeline or pre-commit
hook to ensure code quality standards are maintained.
"""

import subprocess
import sys
from typing import Final, List

#: List of linter commands to execute sequentially
#: Each command is represented as a list of strings for subprocess execution
commands: Final[List[List[str]]] = [
    # Black code formatter - checks if code is properly formatted
    ["black", "--check", "."],
    # isort import sorter - verifies imports are correctly sorted and organized
    ["isort", "--check", "."],
    # flake8 style guide enforcement - runs pycodestyle, pyflakes, and mccabe
    ["flake8", "."],
    # pylint static code analysis - comprehensive Python code analysis
    ["pylint", "--recursive=y", ".", "--load-plugins=pylint_django"],
    # mypy static type checker - verifies type annotations throughout the codebase
    ["mypy", "."],
]


def main() -> None:
    """
    Execute all configured linters in sequence.

    This function iterates through the predefined list of linter commands,
    runs each one using subprocess, and immediately exits if any linter
    returns a non-zero exit code (indicating failures or issues found).

    The function provides real-time feedback by printing each command
    being executed and finally displays a success message if all linters pass.

    Raises:
        SystemExit: If any linter command fails (non-zero return code),
                   the system exits with the same return code.

    Example:
        >>> main()
        Running: black --check .
        Running: isort --check .
        Running: flake8 .
        Running: pylint --recursive=y . --load-plugins=pylint_django
        Running: mypy .
        ✅ All linters passed!
    """
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")

        # Fix for pylint warning: explicitly set check=False to indicate
        # we're manually handling the return code instead of raising exceptions
        result = subprocess.run(cmd, check=False)

        if result.returncode != 0:
            print(f"❌ Linter failed: {' '.join(cmd)}")
            sys.exit(result.returncode)

    print("✅ All linters passed!")


if __name__ == "__main__":
    main()
