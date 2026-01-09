"""Форматирование вывода."""
from typing import List

class OutputFormatter:
    LINE_WIDTH = 80
    
    @staticmethod
    def print_header(title: str) -> None:
        print(f"\n{'='*80}\n {title.center(78)}\n{'='*80}\n")
    
    @staticmethod
    def print_success(message: str) -> None:
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message: str) -> None:
        print(f"❌ {message}")