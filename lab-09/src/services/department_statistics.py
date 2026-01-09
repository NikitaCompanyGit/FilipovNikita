from typing import List, Dict
from base.abstract_employee import AbstractEmployee

class DepartmentStatistics:
    """
    Сервис для расчётов и статистики отдела.
    Отвечает ТОЛЬКО за вычисления (SRP).
    """

    @staticmethod
    def calculate_total_salary(employees: List[AbstractEmployee]) -> float:
        """
        Рассчитывает общий фонд оплаты труда (ФОТ) отдела.

        ✅ ИСПРАВЛЕН BUG: 
        ❌ ДО:  return sum(employees)  # TypeError!
        ✅ ПОСЛЕ: return sum(emp.calculate_salary() for emp in employees)
        """
        return sum(emp.calculate_salary() for emp in employees)

    @staticmethod
    def get_employee_count(employees: List[AbstractEmployee]) -> Dict[str, int]:
        """
        Возвращает статистику по количеству сотрудников каждого типа.
        Пример: {'Manager': 1, 'Developer': 5}
        """
        counts = {}
        for emp in employees:
            type_name = emp.__class__.__name__
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    @staticmethod
    def get_average_salary(employees: List[AbstractEmployee]) -> float:
        """Рассчитывает среднюю зарплату в отделе."""
        if not employees:
            return 0.0
        return DepartmentStatistics.calculate_total_salary(employees) / len(employees)