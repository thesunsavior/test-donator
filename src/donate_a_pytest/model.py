from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

class TestCase(BaseModel):
    inp: dict = Field(alias="input")
    outp: dict = Field(alias="output")
    desc: Optional[str] = Field(alias="description")

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
        
    
    def register(self, func_name: str="", func: callable=None, inp: dict=None, outp: dict=None, desc: Optional[str] = None) -> None:
        """Register a test function"""
        logger = logging.getLogger(__name__)

        if func_name:
            test_name = func_name
        elif func:
            test_name = func.__name__
        else:
            raise ValueError("Either func_name or func must be provided")

        for test_case in self._test_cases.get(test_name, []):
            if test_case.inp == inp and test_case.outp == outp and test_case.desc == desc:
                logger.info(f"Test case already registered: {test_name}")
                return
            
        tests_cases = self._test_cases.get(test_name, [])
        tests_cases.append(TestCase(inp=inp, outp=outp, desc=desc))

        self._test_cases[test_name] = tests_cases
    
    def get(self, func_name: str = "", func: callable = None) -> callable:
        """Get a test function by name"""
        if func_name:
            return self._test_cases.get(func_name, [])  
        elif func:
            return self._test_cases.get(func.__name__, [])
        else:
            raise ValueError("Either func_name or func must be provided")