"""Миксин для арифметики."""
from typing import Any, Union
from employee_interfaces import IArithmetic

class ArithmeticMixin(IArithmetic):
    def __add__(self, other: Any) -> float:
        if hasattr(other, 'calculate_salary'):
            return self.calculate_salary() + other.calculate_salary()
        elif isinstance(other, (int, float)):
            return self.calculate_salary() + other
        return NotImplemented
    
    def __radd__(self, other: Any) -> float:
        if isinstance(other, (int, float)):
            return other + self.calculate_salary()
        return NotImplemented