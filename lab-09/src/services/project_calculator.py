from typing import List
from base.abstract_employee import AbstractEmployee

class ProjectCalculator:
    """
    Калькулятор для проектных расчётов.
    Отвечает ТОЛЬКО за вычисления (SRP).
    """

    @staticmethod
    def calculate_total_salary(team: List[AbstractEmployee]) -> float:
        """
        Рассчитывает бюджет зарплат (суммарный оклад всех участников).

        :param team: Список сотрудников команды.
        :returns: Суммарная зарплата.
        """
        return sum(emp.calculate_salary() for emp in team)

    @staticmethod
    def calculate_average_salary(team: List[AbstractEmployee]) -> float:
        """
        Рассчитывает среднюю зарплату в команде проекта.

        :returns: Средняя зарплата или 0.0, если команда пуста.
        """
        if not team:
            return 0.0
        return ProjectCalculator.calculate_total_salary(team) / len(team)