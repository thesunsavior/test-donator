import os
import json
import yaml
from itertools import chain
from donate_a_pytest.utils import find_paths_with_substring
from donate_a_pytest.model import TestCase, InputOutputRegistry


def crawl_json_test_cases(test_name: str, search_dir: str = None) -> list:
    """
    Crawl the json input for a given test name
    """
    search_dir = search_dir or os.getcwd()
    json_files = find_paths_with_substring(search_dir, test_name, ".json")
    test_cases = []
    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            test_cases.append(data)

    return test_cases


def crawl_yaml_test_cases(test_name: str, search_dir: str = None) -> list:
    """
    Crawl the yaml input for a given test name
    """
    search_dir = search_dir or os.getcwd()
    yaml_files = find_paths_with_substring(search_dir, test_name, ".yaml")
    test_cases = []
    for yaml_file in yaml_files:
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.load(f)
            test_cases.append(data)

    return test_cases


def get_test_cases(func_name: str = "", func: callable = None) -> list:
    """
    Get the test cases for a given function name or function
    """
    name = ""
    if func_name:
        name = func_name
    elif func:
        name = func.__name__
    else:
        raise ValueError("Either func_name or func must be provided")

    # Crawl the test cases from the json and yaml files
    json_test_cases = crawl_json_test_cases(name)
    yaml_test_cases = crawl_yaml_test_cases(name)
    for test_case in chain(json_test_cases, yaml_test_cases):
        test_case = TestCase(**test_case)
        InputOutputRegistry.get_instance().register_testcase(name, test_case)

    return InputOutputRegistry.get_instance().get(name)
