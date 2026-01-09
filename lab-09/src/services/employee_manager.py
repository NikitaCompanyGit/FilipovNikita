from typing import List, Optional
from base.abstract_employee import AbstractEmployee
from organization.department import Department

class EmployeeManager:
    """
    Менеджер для глобального управления сотрудниками компании.
    Отвечает ТОЛЬКО за операции с сотрудниками на уровне компании (SRP).
    """

    def __init__(self, departments: List[Department]):
        """
        :param departments: Ссылка на список отделов компании.
        """
        self._departments = departments

    def get_all_employees(self) -> List[AbstractEmployee]:
        """
        Возвращает плоский список всех сотрудников из всех отделов.
        """
        all_emps = []
        for dept in self._departments:
            all_emps.extend(dept.get_employees())
        return all_emps

    def find_employee_by_id(self, emp_id: int) -> Optional[AbstractEmployee]:
        """
        Глобальный поиск сотрудника по ID во всех отделах.

        :returns: Сотрудник или None, если не найден.
        """
        for dept in self._departments:
            found = dept.find_employee_by_id(emp_id)
            if found:
                return found
        return None

    def find_department_for_employee(self, emp_id: int) -> Optional[Department]:
        """
        Находит отдел, в котором работает сотрудник с указанным ID.

        :returns: Отдел или None, если сотрудник не найден.
        """
        for dept in self._departments:
            if dept.find_employee_by_id(emp_id):
                return dept
        return None

    def remove_employee_from_department(self, emp_id: int, dept: Department) -> None:
        """
        Удаляет сотрудника из указанного отдела.

        :param emp_id: ID сотрудника.
        :param dept: Отдел, из которого удаляется сотрудник.
        """
        dept.remove_employee(emp_id)