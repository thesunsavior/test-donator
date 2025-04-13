from typing import Any, Optional

from donate_a_pytest.model import InputOutputRegistry, TestCase


def register_test_case(func_name: str, test_case: TestCase):
    InputOutputRegistry.get_instance().register_testcase(func_name, test_case)


def register(func_name: str, inp: dict, outp: Any, desc: Optional[str] = None):
    if func_name:
        test_name = func_name
    else:
        raise ValueError("function name must be provided")

    InputOutputRegistry.get_instance().register(test_name, None, inp, outp, desc)


def register_test_cases(func_name: str, test_cases: list[TestCase]):
    for test_case in test_cases:
        register_test_case(func_name, test_case)


def get_test_cases(func_name: str):
    return InputOutputRegistry.get_instance().get(func_name)


def get_all_test_cases():
    return InputOutputRegistry.get_instance().get_all()
