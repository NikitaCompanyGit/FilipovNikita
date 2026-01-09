from typing import List, Dict
from base.abstract_employee import AbstractEmployee
from services.department_statistics import DepartmentStatistics
from services.department_search_service import DepartmentSearchService
from services.department_validator import DepartmentValidator
from repositories.department_repository import DepartmentRepository

class Department:
    """
    Класс, описывающий отдел компании (Department).

    РЕФАКТОРИНГ:
    ✅ SRP: Класс отвечает ТОЛЬКО за управление коллекцией сотрудников.
    ✅ Все вычисления делегированы в DepartmentStatistics.
    ✅ Весь поиск делегирован в DepartmentSearchService.
    ✅ Вся валидация делегирована в DepartmentValidator.
    ✅ Вся сериализация делегирована в DepartmentRepository.

    ДО рефакторинга: 200+ строк, 5 обязанностей
    ПОСЛЕ рефакторинга: ~80 строк, 1 обязанность
    """

    def __init__(self, name: str):
        """
        Инициализация отдела.

        :param name: Название отдела (уникальное в рамках компании).
        """
        self.name = name
        self.__employees: List[AbstractEmployee] = []

    # --- Управление сотрудниками (ЕДИНСТВЕННАЯ ОТВЕТСТВЕННОСТЬ) ---

    def add_employee(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника в отдел.

        :param employee: Объект сотрудника (наследник AbstractEmployee).
        :raises TypeError: Если переданный объект не является сотрудником.
        """
        DepartmentValidator.validate_employee(employee)
        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        """
        Удаляет сотрудника из отдела по его ID.
        Если сотрудник с таким ID не найден, список остается без изменений.
        """
        DepartmentValidator.validate_employee_id(employee_id)
        self.__employees = [e for e in self.__employees if e.id != employee_id]

    def get_employees(self) -> List[AbstractEmployee]:
        """Возвращает список всех сотрудников отдела."""
        return self.__employees

    # --- Делегирование расчётов (DepartmentStatistics) ---

    def calculate_total_salary(self) -> float:
        """
        Рассчитывает общий фонд оплаты труда (ФОТ) отдела.
        Делегирует вычисление в DepartmentStatistics.
        """
        return DepartmentStatistics.calculate_total_salary(self.__employees)

    def get_employee_count(self) -> Dict[str, int]:
        """
        Возвращает статистику по количеству сотрудников каждого типа.
        Делегирует вычисление в DepartmentStatistics.
        """
        return DepartmentStatistics.get_employee_count(self.__employees)

    def get_average_salary(self) -> float:
        """
        Рассчитывает среднюю зарплату в отделе.
        Делегирует вычисление в DepartmentStatistics.
        """
        return DepartmentStatistics.get_average_salary(self.__employees)

    # --- Делегирование поиска (DepartmentSearchService) ---

    def find_employee_by_id(self, employee_id: int):
        """
        Ищет сотрудника по ID.
        Делегирует поиск в DepartmentSearchService.
        """
        return DepartmentSearchService.find_employee_by_id(self.__employees, employee_id)

    def find_employees_by_type(self, type_name: str):
        """
        Ищет всех сотрудников определённого типа.
        Делегирует поиск в DepartmentSearchService.
        """
        return DepartmentSearchService.find_employees_by_type(self.__employees, type_name)

    # --- Делегирование сериализации (DepartmentRepository) ---

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет отдел в JSON-файл.
        Делегирует сохранение в DepartmentRepository.
        """
        DepartmentRepository.save_to_file(self.name, self.__employees, filename)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """
        Восстанавливает отдел из JSON-файла.
        Делегирует загрузку в DepartmentRepository.
        """
        data = DepartmentRepository.load_from_file(filename)
        dept = cls(data["department_name"])
        for emp in data["employees"]:
            dept.add_employee(emp)
        return dept

    # --- Магические методы (Protocol implementation) ---

    def __len__(self) -> int:
        """Возвращает количество сотрудников в отделе (поддержка len(dept))."""
        return len(self.__employees)

    def __getitem__(self, index) -> AbstractEmployee:
        """
        Обеспечивает доступ к сотрудникам по индексу (dept[0]).
        Позволяет итерироваться и обращаться к отделу как к списку.
        """
        return self.__employees[index]

    def __contains__(self, employee: AbstractEmployee) -> bool:
        """
        Проверяет принадлежность сотрудника отделу (поддержка оператора in).
        Пример: if employee in dept: ...
        """
        return employee in self.__employees

    def __iter__(self):
        """Возвращает итератор по сотрудникам (поддержка циклов for)."""
        return iter(self.__employees)

    def __str__(self):
        return f"Отдел '{self.name}' (Сотрудников: {len(self)})"