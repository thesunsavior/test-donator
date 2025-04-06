import os
import json
import yaml

from donate_a_pytest.utils import find_paths_with_substring

def crawl_json_test_cases(test_name: str) -> list:
    """
    Crawl the json input for a given test name
    """
    json_files = find_paths_with_substring(os.path.dirname(__file__),test_name, ".json")
    test_cases = []
    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            test_cases.append(data)
    
    return test_cases

def crawl_yaml_test_cases(test_name: str) -> list:
    """
    Crawl the yaml input for a given test name
    """
    yaml_files = find_paths_with_substring(os.path.dirname(__file__),test_name, ".yaml")
    test_cases = []
    for yaml_file in yaml_files:
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.load(f)
            test_cases.append(data)
    
    return test_cases
