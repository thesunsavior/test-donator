import os
import sys
import json
import tempfile
import pytest

from donate_a_pytest.decorators import register_for_donation


def test_function_preserved():
    """Test that the original function is preserved and usable."""
    # Define a decorated function
    @register_for_donation
    def sample_func(a, b):
        return a + b

    # Verify the function works normally
    assert sample_func(1, 2) == 3
    assert sample_func(3, 4) == 7


def test_test_function_created():
    """Test that a test function is created in the module."""
    # Define a decorated function
    @register_for_donation
    def another_func(a, b):
        return a + b

    # Verify the test function exists in the current module
    current_module = sys.modules[__name__]
    assert hasattr(current_module, "test_another_func")
    assert callable(getattr(current_module, "test_another_func"))

    # Verify the test function has the donate marker
    test_func = getattr(current_module, "test_another_func")
    assert hasattr(test_func, "pytestmark")
    assert any(marker.name == "donate" for marker in test_func.pytestmark)
