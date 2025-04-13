import os
import sys
import pytest
import json
import yaml
import tempfile
from pathlib import Path

from donate_a_pytest.decorators import register_for_donation
from donate_a_pytest.tests_crawler import get_all_test_cases
from donate_a_pytest.main import run_donated_tests


@pytest.fixture
def data_path():
    return Path(__file__).parent / "test_data"


def test_get_all_test_cases_with_real_files(data_path):
    """Test that get_all_test_cases correctly finds and loads test cases from files."""
    func_name = "sample_function_1"
    dir_path = data_path / func_name

    # Get test cases
    test_cases = get_all_test_cases(func_name, search_dir=dir_path)

    # We should have 4 test cases (2 from JSON, 2 from YAML)
    assert len(test_cases) == 4

    # Verify test case content
    inputs = [tc.inp for tc in test_cases]
    outputs = [tc.outp for tc in test_cases]

    # Check that we have the expected inputs and outputs
    assert {"a": 1, "b": 2} in inputs
    assert {"a": -1, "b": 1} in inputs
    assert {"a": 3, "b": 4} in inputs
    assert {"a": 10, "b": -5} in inputs

    assert 3 in outputs
    assert 0 in outputs
    assert 7 in outputs
    assert 5 in outputs


def test_decorator_with_test_data(monkeypatch, data_path):
    """Test that @register_for_donation correctly uses test data files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Define a sample function
        @register_for_donation
        def sample_function_1(a, b):
            return a + b

        # Override __name__ to match our test files
        sample_function_1.__name__ = "sample_function_1"
        dir_path = data_path / sample_function_1.__name__

        # Verify the test function exists in the current module
        current_module = sys.modules[__name__]
        assert hasattr(current_module, "test_sample_function_1")
        assert callable(getattr(current_module, "test_sample_function_1"))

        # Verify the test function has the donate marker
        test_func = getattr(current_module, "test_sample_function_1")
        assert hasattr(test_func, "pytestmark")
        assert any(marker.name == "donate" for marker in test_func.pytestmark)

        # Create a pytest test to verify that our sample_function works with test data
        test_py_file = os.path.join(tmp_dir, "test_sample.py")
        with open(test_py_file, "w") as f:
            f.write(
                """
import pytest
from donate_a_pytest.decorators import register_for_donation

# This function will be registered for donation testing
@register_for_donation
def sample_function_1(a, b):
    return a + b
"""
            )

        # Run the tests
        result = run_donated_tests(directory=tmp_dir)

        # Verify the result
        assert result["success"] is True
