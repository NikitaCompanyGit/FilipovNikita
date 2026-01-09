"""
Сервисы для управления сотрудниками.

Этот пакет содержит:
- Базовые сервисы (валидация, форматирование, сериализация)
- Стратегии расчёта зарплаты
- Фабрика создания сотрудников
- Специфичные валидаторы и форматтеры для каждого типа
"""

from .base_validator import BaseValidator
from .base_formatter import BaseFormatter
from .salary_strategy import (
    SalaryStrategy,
    BaseSalaryStrategy,
    BonusSalaryStrategy,
    CommissionSalaryStrategy,
    DeveloperSalaryStrategy
)
from .employee_serializer import EmployeeSerializer
from .employee_factory import EmployeeFactory

__all__ = [
    'BaseValidator',
    'BaseFormatter',
    'SalaryStrategy',
    'BaseSalaryStrategy',
    'BonusSalaryStrategy',
    'CommissionSalaryStrategy',
    'DeveloperSalaryStrategy',
    'EmployeeSerializer',
    'EmployeeFactory'
]