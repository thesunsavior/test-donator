from pydantic import BaseModel, Field
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class TestCase(BaseModel):
    inp: dict = Field(alias="input")
    outp: Any = Field(alias="output")
    desc: Optional[str] = Field(default=None, alias="description")


class InputOutputRegistry:
    """
    Singleton class to manage registered test functions and their test cases.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InputOutputRegistry, cls).__new__(cls)
            cls._instance._test_cases = {}
        return cls._instance

    def __init__(self) -> None:
        raise Exception("The class is a singleton, use get_instance() instead")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def _check_duplicate(self, test_name: str, target_case: TestCase) -> bool:
        """Check if the input output set is already registered"""
        for test_case in self._test_cases.get(test_name, []):
            if (
                test_case.inp == target_case.inp
                and test_case.outp == target_case.outp
                and test_case.desc == target_case.desc
            ):
                return True
        return False

    def register(
        self,
        func_name: str = "",
        func: callable = None,
        inp: dict = None,
        outp: Any = None,
        desc: Optional[str] = None,
    ) -> None:
        """Register an input output set for a test function"""
        logger = logging.getLogger(__name__)

        if func_name:
            test_name = func_name
        elif func:
            test_name = func.__name__
        else:
            raise ValueError("Either func_name or func must be provided")

        target_case = TestCase(input=inp, output=outp, description=desc)
        if self._check_duplicate(test_name, target_case):
            logger.info(f"Test case already registered: {test_name}")
            return

        tests_cases = self._test_cases.get(test_name, [])
        tests_cases.append(target_case)
        self._test_cases[test_name] = tests_cases

    def register_testcase(self, test_name: str, test_case: TestCase) -> None:
        """Register a test case for a test function"""
        if self._check_duplicate(test_name, test_case):
            logger.info(f"Test case already registered: {test_name}")
            return

        tests_cases = self._test_cases.get(test_name, [])
        tests_cases.append(test_case)
        self._test_cases[test_name] = tests_cases

    def get(self, func_name: str = "", func: callable = None) -> callable:
        """Get an input output set by name"""
        if func_name:
            return self._test_cases.get(func_name, [])
        elif func:
            return self._test_cases.get(func.__name__, [])
        else:
            raise ValueError("Either func_name or func must be provided")

    def get_all(self):
        """Get all registered test cases."""
        return self._test_cases
