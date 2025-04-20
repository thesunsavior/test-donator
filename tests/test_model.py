import pytest
from unittest.mock import Mock
import logging
from donate_a_pytest.model import TestCase, InputOutputRegistry


class TestTestCase:
    """Tests for the TestCase model"""

    def test_create_test_case(self):
        """Test creating a TestCase with valid input and output"""
        test_case = TestCase(
            input={"a": 1}, output={"result": 2}, description="Test description"
        )
        assert test_case.inp == {"a": 1}
        assert test_case.outp == {"result": 2}
        assert test_case.desc == "Test description"

    def test_field_aliasing(self):
        """Test that aliasing works correctly"""
        test_case = TestCase(input={"a": 1}, output={"result": 2})
        assert test_case.inp == {"a": 1}  # input -> inp
        assert test_case.outp == {"result": 2}  # output -> outp


class TestInputOutputRegistry:
    """Tests for the InputOutputRegistry class"""

    def setup_method(self):
        """Reset the registry for each test"""
        # Clear the singleton instance for each test
        InputOutputRegistry._instance = None
        # Get a new instance
        self.registry = InputOutputRegistry.get_instance()
        # Ensure _test_cases is initialized (addressing linter error)
        if not hasattr(self.registry, "_test_cases"):
            self.registry._test_cases = {}

    def test_singleton_behavior(self):
        """Test that multiple calls to get_instance() return the same instance"""
        instance1 = InputOutputRegistry.get_instance()
        instance2 = InputOutputRegistry.get_instance()
        assert instance1 is instance2

    def test_constructor_raises_exception(self):
        """Test that constructor raises an Exception when called directly"""
        with pytest.raises(Exception) as excinfo:
            InputOutputRegistry()
        assert "The class is a singleton" in str(excinfo.value)

    def test_register_with_func_name(self):
        """Test registering a test case with func_name"""
        self.registry.register(
            func_name="test_func",
            inp={"a": 1},
            outp={"result": 2},
            desc="Test description",
        )
        test_cases = self.registry.get(func_name="test_func")
        assert len(test_cases) == 1
        assert test_cases[0].inp == {"a": 1}
        assert test_cases[0].outp == {"result": 2}
        assert test_cases[0].desc == "Test description"

    def test_register_with_function(self):
        """Test registering a test case with a function"""

        def test_func():
            pass

        self.registry.register(func=test_func, inp={"a": 1}, outp={"result": 2})
        test_cases = self.registry.get(func=test_func)
        assert len(test_cases) == 1
        assert test_cases[0].inp == {"a": 1}
        assert test_cases[0].outp == {"result": 2}

    def test_register_multiple_test_cases(self):
        """Test registering multiple test cases for the same function"""
        self.registry.register(func_name="test_func", inp={"a": 1}, outp={"result": 2})
        self.registry.register(func_name="test_func", inp={"a": 2}, outp={"result": 4})
        test_cases = self.registry.get(func_name="test_func")
        assert len(test_cases) == 2
        # Sort by input value to ensure consistent order
        test_cases.sort(key=lambda x: x.inp["a"])
        assert test_cases[0].inp == {"a": 1}
        assert test_cases[0].outp == {"result": 2}
        assert test_cases[1].inp == {"a": 2}
        assert test_cases[1].outp == {"result": 4}

    def test_register_duplicate_test_cases(self, caplog):
        """Test registering duplicate test cases (should be ignored)"""
        caplog.set_level(logging.INFO)

        self.registry.register(
            func_name="test_func",
            inp={"a": 1},
            outp={"result": 2},
            desc="Test description",
        )
        # Register the same test case again
        self.registry.register(
            func_name="test_func",
            inp={"a": 1},
            outp={"result": 2},
            desc="Test description",
        )
        test_cases = self.registry.get(func_name="test_func")
        assert len(test_cases) == 1  # Should only have one test case
        assert "Test case already registered" in caplog.text

    def test_register_testcase_method(self, caplog):
        """Test the register_testcase method"""
        caplog.set_level(logging.INFO)

        test_case = TestCase(input={"a": 1}, output={"result": 2})
        self.registry.register_testcase("test_func", test_case)

        # Register the same test case again
        self.registry.register_testcase("test_func", test_case)

        test_cases = self.registry.get(func_name="test_func")
        assert len(test_cases) == 1
        assert "Test case already registered" in caplog.text

    def test_get_with_func_name(self):
        """Test getting test cases by func_name"""
        self.registry.register(func_name="test_func", inp={"a": 1}, outp={"result": 2})
        test_cases = self.registry.get(func_name="test_func")
        assert len(test_cases) == 1
        assert test_cases[0].inp == {"a": 1}
        assert test_cases[0].outp == {"result": 2}

    def test_get_with_function(self):
        """Test getting test cases by function"""

        def test_func():
            pass

        self.registry.register(func=test_func, inp={"a": 1}, outp={"result": 2})
        test_cases = self.registry.get(func=test_func)
        assert len(test_cases) == 1
        assert test_cases[0].inp == {"a": 1}
        assert test_cases[0].outp == {"result": 2}

    def test_get_non_existent_function(self):
        """Test getting test cases for a non-existent function"""
        test_cases = self.registry.get(func_name="non_existent_func")
        assert len(test_cases) == 0
        assert test_cases == []

    def test_get_with_no_params(self):
        """Test getting test cases with no parameters"""
        with pytest.raises(ValueError) as excinfo:
            self.registry.get()
        assert "Either func_name or func must be provided" in str(excinfo.value)

    def test_register_with_no_params(self):
        """Test registering test cases with no parameters"""
        with pytest.raises(ValueError) as excinfo:
            self.registry.register(inp={}, outp={})
        assert "Either func_name or func must be provided" in str(excinfo.value)

    def test_check_duplicate(self):
        """Test the _check_duplicate method"""
        # First register a test case
        self.registry.register(
            func_name="test_func",
            inp={"a": 1},
            outp={"result": 2},
            desc="Test description",
        )

        # Create a duplicate test case
        duplicate_case = TestCase(
            input={"a": 1}, output={"result": 2}, description="Test description"
        )

        # Create a different test case
        different_case = TestCase(
            input={"a": 2}, output={"result": 4}, description="Different description"
        )

        # Check if the test cases are duplicates
        assert self.registry._check_duplicate("test_func", duplicate_case) is True
        assert self.registry._check_duplicate("test_func", different_case) is False
        assert (
            self.registry._check_duplicate("non_existent_func", duplicate_case) is False
        )

    def test_clear_by_func_name(self):
        """Test the clear_by_func_name method"""
        self.registry.register(func_name="test_func", inp={"a": 1}, outp={"result": 2})
        self.registry.register(func_name="test_func", inp={"a": 2}, outp={"result": 4})
        self.registry.clear_by_func_name("test_func")
        assert len(self.registry.get(func_name="test_func")) == 0

    def test_clear(self):
        """Test the clear method"""
        self.registry.register(func_name="test_func", inp={"a": 1}, outp={"result": 2})
        self.registry.register(
            func_name="test_func_1", inp={"a": 2}, outp={"result": 4}
        )
        self.registry.clear()
        assert len(self.registry.get_all()) == 0
