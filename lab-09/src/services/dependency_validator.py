from typing import List
from organization.department import Department
from organization.project import Project
from base.exceptions import DependencyError, EmployeeNotFoundError

class DependencyValidator:
    """
    Валидатор зависимостей в компании.
    Отвечает ТОЛЬКО за проверку ссылочной целостности (SRP).
    """

    @staticmethod
    def validate_department_removal(dept: Department) -> None:
        """
        Проверяет, можно ли удалить отдел.

        :raises DependencyError: Если в отделе есть сотрудники.
        """
        if len(dept) > 0:
            raise DependencyError(
                f"Нельзя удалить отдел '{dept.name}', в нем есть {len(dept)} сотрудник(ов)."
            )

    @staticmethod
    def validate_employee_removal(emp_id: int, projects: List[Project]) -> None:
        """
        Проверяет, можно ли удалить сотрудника.

        :raises DependencyError: Если сотрудник занят в проектах.
        """
        occupied_projects = []
        for proj in projects:
            if any(e.id == emp_id for e in proj.get_team()):
                occupied_projects.append(proj.name)

        if occupied_projects:
            raise DependencyError(
                f"Сотрудник {emp_id} занят в проектах: {', '.join(occupied_projects)}. "
                f"Сначала удалите его из команд."
            )

    @staticmethod
    def validate_employee_exists(employee, emp_id: int) -> None:
        """
        Проверяет, что сотрудник существует.

        :raises EmployeeNotFoundError: Если сотрудник не найден.
        """
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {emp_id} не найден.")