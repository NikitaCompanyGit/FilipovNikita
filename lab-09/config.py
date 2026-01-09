"""Конфигурация проекта."""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class TestConfig:
    EXAMPLES_DIR: str = "examples"
    TEST_FILE_PATTERN: str = "test_*_lr8_*.py"
    PARTS_INFO: Dict[str, Dict[str, str]] = None
    PYTEST_ARGS_BASE: List[str] = None
    PYTEST_ARGS_COVERAGE: List[str] = None
    
    def __post_init__(self) -> None:
        if self.PARTS_INFO is None:
            self.PARTS_INFO = {
                'part1': {'title': 'Часть 1', 'tests': '35+', 'description': ''},
                'part2': {'title': 'Часть 2', 'tests': '30+', 'description': ''},
                'part3': {'title': 'Часть 3', 'tests': '25+', 'description': ''},
                'part4': {'title': 'Часть 4', 'tests': '25+', 'description': ''},
                'part5': {'title': 'Часть 5', 'tests': '30+', 'description': ''},
            }
        if self.PYTEST_ARGS_BASE is None:
            self.PYTEST_ARGS_BASE = ["-v", "--tb=short"]
        if self.PYTEST_ARGS_COVERAGE is None:
            self.PYTEST_ARGS_COVERAGE = ["--cov=src", "--cov-report=html", "-v"]

config = TestConfig()
