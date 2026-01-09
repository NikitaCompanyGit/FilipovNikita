"""
Абстрактный класс сотрудника - РЕФАКТОРЕННАЯ ВЕРСИЯ

Применены SOLID принципы:
- ISP: разделены интерфейсы на маленькие
- SRP: логика перемещена в миксины
- DIP: используется зависимость от интерфейсов

БЫЛО: AbstractEmployee требует от всех:
  calculate_salary, get_info, to_dict, сравнение, арифметика

СТАЛО: Гибкое комбинирование интерфейсов через наследование
"""

from abc import ABC
from employee import Employee
from employee_interfaces import (
    ISalaryCalculable,
    IInfoProvidable,
    ISerializable,
    IComparable,
    IArithmetic
)
from employee_comparison_mixin import ComparisonMixin
from employee_arithmetic_mixin import ArithmeticMixin


class AbstractEmployee(
    Employee,
    ISalaryCalculable,
    IInfoProvidable,
    ISerializable,
    ComparisonMixin,
    ArithmeticMixin,
    ABC
):
    """
    Абстрактный базовый класс сотрудника. РЕФАКТОРЕННАЯ ВЕРСИЯ.
    
    Наследуется от:
    - Employee (данные и валидация)
    - ISalaryCalculable, IInfoProvidable, ISerializable (интерфейсы)
    - ComparisonMixin (логика сравнения)
    - ArithmeticMixin (логика арифметики)
    - ABC (для абстрактных методов)
    
    Каждый конкретный класс (Developer, Manager) наследуется от этого.
    """
    
    # Все абстрактные методы определяют конкретные подклассы:
    # - calculate_salary()
    # - get_info()
    # - to_dict()
    #
    # Магические методы наследуются из миксинов:
    # - __eq__, __lt__ из ComparisonMixin
    # - __add__, __radd__ из ArithmeticMixin
    
    pass