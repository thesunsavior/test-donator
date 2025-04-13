"""
Pytest plugin for donate-a-pytest.

This module exposes the pytest plugin functionality when the package is installed.
It registers the custom donate marker and makes the decorator available.
It also allows pytest to discover tests in files without the test_ prefix.
"""

import os
import inspect
import sys
import pytest
from pathlib import Path
from donate_a_pytest.decorators import register_for_donation

# Export the decorator for convenient imports
__all__ = ["register_for_donation", "donate"]


def pytest_configure(config):
    """
    Register custom markers with pytest.

    This will eliminate warnings about unknown markers when users run tests
    with the 'donate' marker, and provides documentation for the marker.
    """
    config.addinivalue_line(
        "markers",
        "donate: mark tests that are created via the @register_for_donation decorator",
    )


def pytest_collect_file(parent, path):
    """
    Custom hook to collect test files that don't start with 'test_'.

    This allows pytest to discover tests in regular Python files that contain
    functions decorated with @register_for_donation.
    """
    # Skip files that pytest already collects (test_*.py or *_test.py)
    name = os.path.basename(str(path))
    if name.startswith("test_") or name.endswith("_test.py"):
        return None

    # Only process Python files
    if str(path).endswith(".py"):
        # Create our custom file collector for donated tests
        return DonatedTestFile.from_parent(parent, fspath=path)

    return None


class DonatedTestFile(pytest.File):
    """Custom file collector for files containing donated tests."""

    def collect(self):
        """Find test functions in a non-test file."""
        # Import the module
        module_path = str(self.fspath)
        module_name = os.path.splitext(os.path.basename(module_path))[0]

        # Try to load the module into sys.modules
        if module_name in sys.modules:
            module = sys.modules[module_name]
        else:
            try:
                # Prepare the module path for import
                sys.path.insert(0, os.path.dirname(module_path))
                module = __import__(module_name)
                sys.path.pop(0)
            except ImportError:
                return  # If we can't import the module, skip it

        # Set the module as the object for this collector
        self.obj = module

        # Look for all functions in the module that have 'test_' prefix
        # which would have been created by the @register_for_donation decorator
        for name, obj in module.__dict__.items():
            if (
                name.startswith("test_")
                and callable(obj)
                and hasattr(obj, "pytestmark")
            ):
                # Check if this function has our donate marker
                if any(marker.name == "donate" for marker in obj.pytestmark):
                    # Yield test item from the parent class
                    yield pytest.Function.from_parent(self, name=name)


# Make the marker available directly
donate = pytest.mark.donate
