"""Поиск тестовых файлов."""
from pathlib import Path
from typing import List, Optional
from config import TestConfig

class TestFileFinder:
    def __init__(self, config: TestConfig) -> None:
        self.config = config
    
    def find_all_test_files(self) -> List[str]:
        examples_dir = Path(self.config.EXAMPLES_DIR)
        if not examples_dir.exists():
            return []
        return sorted([str(f) for f in examples_dir.glob(self.config.TEST_FILE_PATTERN)])