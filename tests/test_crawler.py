import os
import json
import yaml
import pytest
from unittest.mock import patch, MagicMock
import tempfile
import shutil

from donate_a_pytest.tests_crawler import (
    crawl_json_test_cases,
    crawl_yaml_test_cases,
    get_all_test_cases,
)
from donate_a_pytest.model import TestCase, InputOutputRegistry


@pytest.fixture
def reset_registry():
    """Reset the InputOutputRegistry before each test"""
    InputOutputRegistry._instance = None
    yield
    InputOutputRegistry._instance = None


@pytest.fixture
def test_files_dir(tmp_path):
    """Create a temporary directory with test files"""
    # Create test function JSON files
    test_func_dir = tmp_path / "test_func"
    test_func_dir.mkdir()

    # Valid JSON test file with a single test case
    json_file1 = test_func_dir / "test_func_1.json"
    with open(json_file1, "w", encoding="utf-8") as f:
        json.dump(
            {"input": {"a": 1}, "output": {"result": 2}, "description": "Test 1"},
            f,
            indent=4,
        )

    # Valid JSON test file with multiple test cases (array)
    json_file2 = test_func_dir / "test_func_2.json"
    with open(json_file2, "w", encoding="utf-8") as f:
        json.dump(
            [
                {"input": {"a": 2}, "output": {"result": 4}, "description": "Test 2"},
                {"input": {"a": 3}, "output": {"result": 6}, "description": "Test 3"},
            ],
            f,
            indent=4,
        )

    # Valid YAML test file with a single test case
    yaml_file1 = test_func_dir / "test_func_1.yaml"
    yaml_file1.write_text(
        yaml.dump(
            {"input": {"b": 5}, "output": {"result": 10}, "description": "YAML Test 1"}
        )
    )

    # Valid YAML test file with multiple test cases
    yaml_file2 = test_func_dir / "test_func_2.yaml"
    yaml_file2.write_text(
        yaml.dump(
            [
                {
                    "input": {"b": 6},
                    "output": {"result": 12},
                    "description": "YAML Test 2",
                },
                {
                    "input": {"b": 7},
                    "output": {"result": 14},
                    "description": "YAML Test 3",
                },
            ]
        )
    )

    # Invalid YAML test file
    invalid_yaml = test_func_dir / "invalid_test_func.yaml"
    invalid_yaml.write_text("- invalid: yaml: content:\n  indentation is wrong")

    # Create another test function directory
    other_func_dir = tmp_path / "other_func"
    other_func_dir.mkdir()

    other_json = other_func_dir / "other_func.json"
    other_json.write_text(
        json.dumps(
            {
                "input": {"x": 10},
                "output": {"result": 20},
                "description": "Other Function",
            }
        )
    )

    return tmp_path


class TestCrawlJsonTestCases:
    """Tests for the crawl_json_test_cases function"""

    def test_find_valid_json_files(self, test_files_dir):
        """Test finding and parsing valid JSON test files"""
        # Test with a function that has test files
        test_cases = crawl_json_test_cases("test_func", str(test_files_dir))

        # Should find 2 valid JSON files (one single case, one with array of 2 cases)
        assert len(test_cases) == 3

        # Verify content of first test case
        assert any(tc.get("input", {}).get("a") == 1 for tc in test_cases)
        assert any(tc.get("output", {}).get("result") == 2 for tc in test_cases)

        # Verify content of other test cases
        assert any(tc.get("input", {}).get("a") == 2 for tc in test_cases)
        assert any(tc.get("input", {}).get("a") == 3 for tc in test_cases)

    def test_no_json_files_found(self, test_files_dir):
        """Test behavior when no JSON files are found"""
        # Test with a function that has no test files
        test_cases = crawl_json_test_cases("nonexistent_func", str(test_files_dir))
        assert test_cases == []

    def test_handle_invalid_json(self, test_files_dir):
        """Test handling of invalid JSON files"""
        # This should skip invalid files and only return valid ones

        test_cases = crawl_json_test_cases("test_func", str(test_files_dir))
        assert len(test_cases) == 3


class TestCrawlYamlTestCases:
    """Tests for the crawl_yaml_test_cases function"""

    def test_find_valid_yaml_files(self, test_files_dir):
        """Test finding and parsing valid YAML test files"""
        # Test with a function that has test files
        test_cases = crawl_yaml_test_cases("test_func", str(test_files_dir))

        # Should find 2 valid YAML files (one single case, one with array of 2 cases)
        assert len(test_cases) == 3

        # Verify content of first test case
        assert any(tc.get("input", {}).get("b") == 5 for tc in test_cases)
        assert any(tc.get("output", {}).get("result") == 10 for tc in test_cases)

        # Verify content of other test cases
        assert any(tc.get("input", {}).get("b") == 6 for tc in test_cases)
        assert any(tc.get("input", {}).get("b") == 7 for tc in test_cases)

    def test_handle_invalid_yaml(self, test_files_dir, caplog):
        """Test handling of invalid YAML files"""
        # This should skip invalid files and only return valid ones
        test_cases = crawl_yaml_test_cases("test_func", str(test_files_dir))

        # Should still find the valid YAML files
        assert len(test_cases) == 3
