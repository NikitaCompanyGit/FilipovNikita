from typing import List
from organization.department import Department
from organization.project import Project

class CostCalculator:
    """
    Калькулятор финансовых затрат компании.
    Отвечает ТОЛЬКО за расчёты бюджета (SRP).
    """

    @staticmethod
    def calculate_total_monthly_cost(departments: List[Department]) -> float:
        """
        Рассчитывает общие ежемесячные затраты на зарплаты по всей компании.

        :param departments: Список отделов компании.
        :returns: Суммарный ФОТ (фонд оплаты труда).
        """
        return sum(dept.calculate_total_salary() for dept in departments)

    @staticmethod
    def calculate_project_budgets(projects: List[Project]) -> dict:
        """
        Рассчитывает бюджет зарплат для каждого проекта.

        :returns: Словарь {project_name: budget}.
        """
        return {
            proj.name: proj.calculate_total_salary() 
            for proj in projects
        }

    @staticmethod
    def calculate_department_budgets(departments: List[Department]) -> dict:
        """
        Рассчитывает бюджет зарплат для каждого отдела.

        :returns: Словарь {department_name: budget}.
        """
        return {
            dept.name: dept.calculate_total_salary() 
            for dept in departments
        }