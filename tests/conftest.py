import os
import sys
import pytest
import random

from pathlib import Path


CWD = Path(__file__).resolve().parent
code_dir = CWD / '..'
sys.path.append(str(code_dir))

#os.environ.update({})

print(sys.path)

def pytest_configure(config):
    """Called at the start of the entire test run"""
    pass


def pytest_unconfigure(config):
    """Called at the end of a test run"""
    pass


def pytest_runtest_teardown(item, nextitem):
    """Called at the end of each test"""
    pass
