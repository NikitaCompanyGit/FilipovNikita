import json
import os
from typing import List, Optional, Dict
from base.abstract_employee import AbstractEmployee

class Department:
    """
    Класс, описывающий отдел компании (Department).
    
    Реализует паттерн Агрегация: отдел содержит коллекцию сотрудников.
    Обеспечивает управление этой коллекцией (добавление, удаление, поиск),
    а также предоставляет интерфейс для сериализации данных отдела в JSON.
    """

    def __init__(self, name: str):
        """
        Инициализация отдела.
        
        :param name: Название отдела (уникальное в рамках компании).
        """
        self.name = name
        # Приватный список для хранения сотрудников.
        # Используем аннотацию типов для ясности (List[AbstractEmployee]).
        self.__employees: List[AbstractEmployee] = []

    def add_employee(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника в отдел.
        
        :param employee: Объект сотрудника (наследник AbstractEmployee).
        :raises TypeError: Если переданный объект не является сотрудником.
        """
        if isinstance(employee, AbstractEmployee):
            self.__employees.append(employee)
        else:
            raise TypeError("В отдел можно добавлять только наследников AbstractEmployee")

    def remove_employee(self, employee_id: int) -> None:
        """
        Удаляет сотрудника из отдела по его уникальному идентификатору (ID).
        Если сотрудник с таким ID не найден, список остается без изменений.
        """
        self.__employees = [e for e in self.__employees if e.id != employee_id]

    def get_employees(self) -> List[AbstractEmployee]:
        """Возвращает список всех сотрудников отдела."""
        return self.__employees

    def calculate_total_salary(self) -> float:
        """
        Рассчитывает общий фонд оплаты труда (ФОТ) отдела.
        Использует полиморфизм: вызывает calculate_salary() для каждого сотрудника
        независимо от его конкретного типа (Manager, Developer и т.д.).
        """
        return sum(self.__employees)

    def get_employee_count(self) -> Dict[str, int]:
        """
        Возвращает статистику по количеству сотрудников каждого типа.
        Пример: {'Manager': 1, 'Developer': 5}
        """
        counts = {}
        for emp in self.__employees:
            type_name = emp.__class__.__name__
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Ищет сотрудника по ID.
        Возвращает объект сотрудника или None, если он не найден.
        """
        for emp in self.__employees:
            if emp.id == employee_id:
                return emp
        return None

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

    # --- Сериализация и Сохранение ---

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет данные отдела и всех его сотрудников в JSON-файл.
        Автоматически создает директорию для файла, если она не существует.
        
        :param filename: Путь к файлу (например, 'docs/json/dept.json').
        """
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"[INFO] Создана директория: {directory}")
            except OSError as e:
                print(f"[ERROR] Не удалось создать директорию {directory}: {e}")
                raise

        data = {
            "department_name": self.name,
            "employees": [emp.to_dict() for emp in self.__employees]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Отдел сохранен в файл: {filename}")

    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """
        Восстанавливает объект отдела из JSON-файла.
        Использует EmployeeFactory для создания конкретных объектов сотрудников.
        """
        from factory import EmployeeFactory
        
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл не найден: {filename}")

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dept = cls(data["department_name"])
        
        for emp_data in data["employees"]:
            # Извлекаем тип для фабрики, остальные поля передаем как kwargs
            emp_type = emp_data.pop("type")
            try:
                employee = EmployeeFactory.create_employee(emp_type, **emp_data)
                dept.add_employee(employee)
            except ValueError as e:
                print(f"[WARNING] Ошибка загрузки сотрудника: {e}")
        
        return dept
