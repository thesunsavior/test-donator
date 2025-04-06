import logging
import pytest

logger = logging.getLogger(__name__)


def register_for_donation(func):
    """
    Decorator to register a function for donation.
    """

    @pytest.mark.donate
    def test_wrapper(*args, **kwargs):
        logger.info(f"Donating {func.__name__}")
        return func(*args, **kwargs)

    return test_wrapper
