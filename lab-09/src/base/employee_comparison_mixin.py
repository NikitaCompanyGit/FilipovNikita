"""Миксин для сравнения."""
from typing import Any
from employee_interfaces import IComparable

class ComparisonMixin(IComparable):
    def __eq__(self, other: Any) -> bool:
        if hasattr(other, 'id'):
            return self.id == other.id
        return False
    
    def __lt__(self, other: 'ComparisonMixin') -> bool:
        if hasattr(other, 'calculate_salary'):
            return self.calculate_salary() < other.calculate_salary()
        return NotImplemented