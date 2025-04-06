import logging
import pytest
from tqdm import tqdm

from donate_a_pytest.tests_crawler import get_all_test_cases

logger = logging.getLogger(__name__)


def register_for_donation(func):
    """
    Decorator to register a function for donation.
    """

    @pytest.mark.donate
    def test_wrapper():
        logger.info(f"Donating tests for {func.__name__}")
        test_cases = get_all_test_cases(func.__name__)
        for test_case in tqdm(test_cases):
            func_args = test_case.inp
            output = func(**func_args)
            assert output == test_case.outp

    return test_wrapper
