"""
Tests for the interface functions that provide programmatic registration of test cases.
"""

import pytest
from donate_a_pytest.interface import (
    register_test_case,
    register,
    get_test_cases,
    get_all_test_cases,
)
from donate_a_pytest.model import TestCase, InputOutputRegistry


@pytest.fixture
def reset_registry():
    """Reset the InputOutputRegistry before and after tests."""
    # Reset before test
    InputOutputRegistry._instance = None
    yield
    # Reset after test
    InputOutputRegistry._instance = None


def test_register_single_case(reset_registry):
    """Test registering a single test case."""
    # Register a test case
    test_case = TestCase(input={"a": 1, "b": 2}, output=3, description="Addition")
    register_test_case("add_function", test_case)

    # Verify it was registered
    case = get_test_cases("add_function")
    assert case[0].inp == {"a": 1, "b": 2}
    assert case[0].outp == 3
    assert case[0].desc == "Addition"


def test_register_multiple_cases(reset_registry):
    """Test registering multiple test cases."""
    # Register first test case
    test_case1 = TestCase(input={"a": 1, "b": 2}, output=3, description="Addition 1+2")
    register_test_case("add_function", test_case1)

    # Register second test case
    test_case2 = TestCase(input={"a": 5, "b": 7}, output=12, description="Addition 5+7")
    register_test_case("add_function", test_case2)

    # Verify both were registered
    cases = get_test_cases("add_function")
    assert len(cases) == 2
    # Check first case
    assert cases[0].inp == {"a": 1, "b": 2}
    assert cases[0].outp == 3
    # Check second case
    assert cases[1].inp == {"a": 5, "b": 7}
    assert cases[1].outp == 12


def test_register_with_function_name(reset_registry):
    """Test registering a test case with a function name."""
    register(
        func_name="mul_function",
        inp={"a": 3, "b": 4},
        outp=12,
        desc="Multiplication 3*4",
    )

    # Verify it was registered
    cases = get_test_cases("mul_function")
    assert len(cases) == 1
    assert cases[0].inp == {"a": 3, "b": 4}
    assert cases[0].outp == 12
    assert cases[0].desc == "Multiplication 3*4"


def test_register_without_function(reset_registry):
    """Test that ValueError is raised when neither func_name nor func is provided."""
    with pytest.raises(ValueError, match="function name must be provided"):
        register(func_name=None, inp={"a": 1, "b": 2}, outp=3)


def test_register_multiple_cases_same_function(reset_registry):
    """Test registering multiple test cases for the same function."""
    # Register multiple test cases
    for i in range(5):
        register(func_name="square", inp={"x": i}, outp=i * i, desc=f"Square of {i}")

    # Verify all were registered
    cases = get_test_cases("square")
    assert len(cases) == 5
    # Check each case
    for i, case in enumerate(cases):
        assert case.inp == {"x": i}
        assert case.outp == i * i
        assert case.desc == f"Square of {i}"


def test_get_existing_cases(reset_registry):
    """Test retrieving existing test cases."""
    # Register a test case
    register_test_case(
        "example_func", TestCase(input={"arg": 1}, output=2, description="Example")
    )

    # Retrieve the test cases
    case = get_test_cases("example_func")
    assert case[0].inp == {"arg": 1}
    assert case[0].outp == 2


def test_get_nonexistent_cases(reset_registry):
    """Test retrieving test cases for a function with no cases."""
    case = get_test_cases("nonexistent_func")
    assert len(case) == 0


def test_get_all_empty(reset_registry):
    """Test retrieving all test cases when none are registered."""
    all_cases = get_all_test_cases()
    assert len(all_cases) == 0


def test_get_all_with_cases(reset_registry):
    """Test retrieving all test cases after registering some."""
    # Register test cases for multiple functions
    register_test_case(
        "func1", TestCase(input={"arg": 1}, output=1, description="Func1 case")
    )
    register_test_case(
        "func2", TestCase(input={"arg": 2}, output=2, description="Func2 case")
    )

    # Retrieve all test cases
    all_cases = get_all_test_cases()
    assert len(all_cases) == 2
    assert "func1" in all_cases
    assert "func2" in all_cases
    assert len(all_cases["func1"]) == 1
    assert len(all_cases["func2"]) == 1
