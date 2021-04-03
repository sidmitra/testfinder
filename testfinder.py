"""
testfinder
"""

from __future__ import annotations

import re
from pathlib import Path

TEST_FILE_REGEX = re.compile(
    r"(tests\.py$)|(test_.*?\.py$)|(.*_test.py)|(tests/__init__\.py)"
)
TEST_CLASS_REGEX = re.compile(r"class (\w+)[:(]")
TEST_CLASS_METHOD_REGEX = re.compile(r"^\s{4}def (test\w*)[(]")
TEST_FUNCTION_REGEX = re.compile(r"^def (test\w*)[(]")


def find_test_files(directory: str) -> list[Path]:
    """
    Find all test case files recursively in the specified directory.
    """
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

    with open(path) as test_file:
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
