"""
testfinder
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

TEST_FILE_REGEX = re.compile(
    r"(tests\.py$)|(test_.*?\.py$)|(.*_test.py)|(tests/__init__\.py)"
)
TEST_CLASS_REGEX = re.compile(r"class (\w+)[:(]")
TEST_CLASS_METHOD_REGEX = re.compile(r"^\s{4}def (test\w*)[(]")
TEST_FUNCTION_REGEX = re.compile(r"^def (test\w*)[(]")


def _find_test_files_via_git(directory: str) -> list[Path] | None:
    """
    Use ``git ls-files`` to enumerate tracked (non-ignored) Python files in
    *directory*, then filter them to test files.  Returns ``None`` if git is
    unavailable or the directory is not inside a git repository, so callers
    can fall back to a plain recursive glob.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.py"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    base = Path(directory)
    paths = [base / line for line in result.stdout.splitlines() if line]
    return [p for p in paths if p.is_file() and TEST_FILE_REGEX.search(p.name)]


def find_test_files(directory: str) -> list[Path]:
    """
    Find all test case files recursively in the specified directory.

    Respects ``.gitignore`` when inside a git repository (via ``git ls-files``).
    Falls back to a plain recursive glob when git is unavailable or the
    directory is not a git repo.
    """
    git_files = _find_test_files_via_git(directory)
    if git_files is not None:
        return git_files

    python_files = [path for path in Path(directory).rglob("*.py") if path.is_file()]
    return [path for path in python_files if TEST_FILE_REGEX.search(path.name)]


def find_test_methods(path: Path) -> list[str]:
    """
    Arguments
    ---------
    path:
        pathlib.Path instance to a test file.

    Returns
    --------
    A list of strings, containing fully qualified path to run a particular test case in pytest.
    Eg. ['mymodule/tests/test_my_viewset.py::MyViewSetTest::test_list_method', ...]
    """
    test_methods: list[str] = []

    with open(path, encoding="utf-8", errors="ignore") as test_file:
        current_class: str = ""

        for line in test_file.readlines():
            if match := TEST_CLASS_REGEX.search(line):
                current_class = match.group(1)
                test_methods.append(f"{path}::{current_class}")
                continue

            if match := TEST_CLASS_METHOD_REGEX.search(line):
                method_name = match.group(1)
                test_methods.append(f"{path}::{current_class}::{method_name}")
                continue

            if match := TEST_FUNCTION_REGEX.search(line):
                method_name = match.group(1)
                test_methods.append(f"{path}::{method_name}")
                continue

    return test_methods


def main():
    """
    Entry point for CLI.
    """
    paths = find_test_files(".")
    methods = []
    for path in paths:
        methods.extend(find_test_methods(path))

    for method in methods:
        print(method)


if __name__ == "__main__":
    main()
