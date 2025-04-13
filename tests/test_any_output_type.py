import os
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch

from donate_a_pytest.decorators import register_for_donation
from donate_a_pytest.tests_crawler import get_all_test_cases
from donate_a_pytest.main import run_donated_tests
from donate_a_pytest.model import TestCase


def test_different_output_types():
    """Test that the TestCase class can handle different output types."""
    # Test with integer output
    int_case = TestCase(input={"a": 1, "b": 2}, output=3)
    assert int_case.outp == 3

    # Test with string output
    str_case = TestCase(input={"a": "hello", "b": "world"}, output="hello world")
    assert str_case.outp == "hello world"

    # Test with list output
    list_case = TestCase(input={"a": [1, 2], "b": [3, 4]}, output=[1, 2, 3, 4])
    assert list_case.outp == [1, 2, 3, 4]

    # Test with dictionary output
    dict_case = TestCase(input={"a": {"x": 1}, "b": {"y": 2}}, output={"x": 1, "y": 2})
    assert dict_case.outp == {"x": 1, "y": 2}

    # Test with boolean output
    bool_case = TestCase(input={"a": True, "b": False}, output=True)
    assert bool_case.outp is True

    # Test with None output
    none_case = TestCase(input={"a": None, "b": None}, output=None)
    assert none_case.outp is None


def create_mixed_test_data(directory, func_name):
    """Create test data files with different output types."""
    # Create test data with mixed output types
    test_data = [
        {"input": {"a": 1, "b": 2}, "output": 3, "description": "Integer output"},
        {
            "input": {"a": "hello", "b": "world"},
            "output": "hello world",
            "description": "String output",
        },
        {
            "input": {"a": [1, 2], "b": [3, 4]},
            "output": [1, 2, 3, 4],
            "description": "List output",
        },
        {
            "input": {"a": {"x": 1}, "b": {"y": 2}},
            "output": {"x": 1, "y": 2},
            "description": "Dictionary output",
        },
        {
            "input": {"a": True, "b": False},
            "output": True,
            "description": "Boolean output",
        },
        {"input": {"a": None, "b": None}, "output": None, "description": "None output"},
    ]

    # Write to a JSON file
    file_path = os.path.join(directory, f"{func_name}.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(test_data, f)

    return file_path


def test_process_data_function_with_any_output():
    """Test a function that processes data and returns different output types."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Define the function we want to test
        def process_data(a, b):
            """Function that handles different types of inputs and returns different types of outputs."""
            if isinstance(a, int) and isinstance(b, int):
                return a + b
            elif isinstance(a, str) and isinstance(b, str):
                return a + " " + b
            elif isinstance(a, list) and isinstance(b, list):
                return a + b
            elif isinstance(a, dict) and isinstance(b, dict):
                return {**a, **b}
            elif isinstance(a, bool) or isinstance(b, bool):
                return a or b
            return None

        # Create test data
        func_name = "process_data"
        data_dir = os.path.join(tmp_dir, "test_data")
        file_path = create_mixed_test_data(data_dir, func_name)

        # Get the test cases
        test_cases = get_all_test_cases(func_name, search_dir=data_dir)

        # Verify we have all the test cases
        assert len(test_cases) == 6

        # Test each test case manually
        for test_case in test_cases:
            func_args = test_case.inp
            expected_output = test_case.outp
            actual_output = process_data(**func_args)
            assert actual_output == expected_output
