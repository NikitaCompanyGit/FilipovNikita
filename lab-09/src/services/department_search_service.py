from typing import List, Optional
from base.abstract_employee import AbstractEmployee

class DepartmentSearchService:
    """
    Сервис для поиска сотрудников в отделе.
    Отвечает ТОЛЬКО за поисковые операции (SRP).
    """

    @staticmethod
    def find_employee_by_id(
        employees: List[AbstractEmployee], 
        employee_id: int
    ) -> Optional[AbstractEmployee]:
        """
        Ищет сотрудника по ID.
        Возвращает объект сотрудника или None, если не найден.
        """
        for emp in employees:
            if emp.id == employee_id:
                return emp
        return None

    @staticmethod
    def find_employees_by_type(
        employees: List[AbstractEmployee], 
        type_name: str
    ) -> List[AbstractEmployee]:
        """
        Ищет всех сотрудников определённого типа.
        Пример: find_employees_by_type(employees, 'Developer')
        """
        return [emp for emp in employees if emp.__class__.__name__ == type_name]

    @staticmethod
    def find_employees_by_name(
        employees: List[AbstractEmployee], 
        name: str
    ) -> List[AbstractEmployee]:
        """
        Ищет сотрудников по имени (регистронезависимо).
        """
        name_lower = name.lower()
        return [emp for emp in employees if name_lower in emp.name.lower()]