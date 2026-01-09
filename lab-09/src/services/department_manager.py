from typing import List
from organization.department import Department
from base.exceptions import DuplicateIdError, DepartmentNotFoundError

class DepartmentManager:
    """
    Менеджер для управления отделами компании.
    Отвечает ТОЛЬКО за операции с отделами (SRP).
    """

    def __init__(self):
        self.__departments: List[Department] = []

    def add_department(self, department: Department) -> None:
        """
        Добавляет новый отдел, проверяя уникальность названия.

        :raises DuplicateIdError: Если отдел с таким названием уже существует.
        """
        if any(d.name == department.name for d in self.__departments):
            raise DuplicateIdError(f"Отдел '{department.name}' уже существует.")
        self.__departments.append(department)

    def get_departments(self) -> List[Department]:
        """Возвращает список всех отделов."""
        return self.__departments

    def get_department_by_name(self, dept_name: str) -> Department:
        """
        Находит отдел по названию.

        :raises DepartmentNotFoundError: Если отдел не найден.
        """
        dept = next((d for d in self.__departments if d.name == dept_name), None)
        if not dept:
            raise DepartmentNotFoundError(f"Отдел '{dept_name}' не найден.")
        return dept

    def remove_department(self, dept_name: str) -> None:
        """
        Удаляет отдел по названию.

        :raises DepartmentNotFoundError: Если отдел не найден.
        """
        dept = self.get_department_by_name(dept_name)
        self.__departments.remove(dept)