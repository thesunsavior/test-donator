import logging
import pytest
import inspect
import sys
from tqdm import tqdm

from donate_a_pytest.tests_crawler import get_all_test_cases

logger = logging.getLogger(__name__)


def register_for_donation(func):
    """
    Decorator to register a function for donation.

    This decorator does two things:
    1. Creates a test function that will be collected by pytest
    2. Returns the original function so it can still be used normally

    The test function will:
    - Have the name "test_{original_function_name}"
    - Be marked with @pytest.mark.donate
    - Run all test cases found for the original function
    """
    # Create the test wrapper function
    @pytest.mark.donate
    def test_wrapper():
        logger.info(f"Donating tests for {func.__name__}")
        test_cases = get_all_test_cases(func.__name__)
        for test_case in tqdm(test_cases):
            func_args = test_case.inp
            output = func(**func_args)
            assert output == test_case.outp

    # Rename the wrapper to ensure pytest collection
    test_name = f"test_{func.__name__}"
    test_wrapper.__name__ = test_name

    # Get the module where the original function was defined
    module = inspect.getmodule(func)

    # Add the test function to the module's global namespace
    if module:
        setattr(module, test_name, test_wrapper)
    else:
        # Fallback to the caller's module if we can't determine the function's module
        frame = inspect.currentframe().f_back
        if frame and frame.f_globals:
            caller_module = frame.f_globals.get("__name__")
            if caller_module and caller_module in sys.modules:
                setattr(sys.modules[caller_module], test_name, test_wrapper)

    return func
