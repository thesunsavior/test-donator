import os
import json
import yaml
import logging

from itertools import chain

from donate_a_pytest.utils import find_paths_with_substring
from donate_a_pytest.model import TestCase, InputOutputRegistry


def crawl_json_test_cases(test_name: str, search_dir: str = None) -> list:
    """
    Crawl the json input for a given test name
    """
    logger = logging.getLogger(__name__)

    search_dir = search_dir or os.getcwd()
    json_files = find_paths_with_substring(search_dir, test_name, ".json")
    test_cases = []
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON file: {json_file}")
                continue

            if isinstance(data, list):
                test_cases.extend(data)
            else:
                test_cases.append(data)

    return test_cases


def crawl_yaml_test_cases(test_name: str, search_dir: str = None) -> list:
    """
    Crawl the yaml input for a given test name
    """
    logger = logging.getLogger(__name__)

    search_dir = search_dir or os.getcwd()
    yaml_files = find_paths_with_substring(search_dir, test_name, ".yaml")
    test_cases = []
    for yaml_file in yaml_files:
        with open(yaml_file, "r", encoding="utf-8") as f:
            try:
                data = yaml.load(f, Loader=yaml.SafeLoader)
            except yaml.YAMLError:
                logger.warning(f"Invalid YAML file: {yaml_file}")
                continue

            if isinstance(data, list):
                test_cases.extend(data)
            elif data:
                test_cases.append(data)

    return test_cases


def get_all_test_cases(
    func_name: str = "", func: callable = None, search_dir: str = None
) -> list:
    """
    Get the test cases for a given function name or function
    """
    logger = logging.getLogger(__name__)

    logger.info(f"Getting all test cases for {func_name}")
    name = ""
    if func_name:
        name = func_name
    elif func:
        name = func.__name__
    else:
        raise ValueError("Either func_name or func must be provided")

    # Crawl the test cases from the json and yaml files
    json_test_cases = crawl_json_test_cases(name, search_dir)
    yaml_test_cases = crawl_yaml_test_cases(name, search_dir)
    print(json_test_cases)
    print(yaml_test_cases)
    for test_case in chain(json_test_cases, yaml_test_cases):
        test_case = TestCase(**test_case)
        InputOutputRegistry.get_instance().register_testcase(name, test_case)

    logger.info(
        f"Found {len(InputOutputRegistry.get_instance().get(name))} test cases for {name}"
    )
    return InputOutputRegistry.get_instance().get(name)
