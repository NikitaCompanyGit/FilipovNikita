"""
Модуль employee.py
==================
Определяет корневой класс иерархии данных.

Этот модуль отвечает за уровень данных (Data Layer). Он инкапсулирует
базовые атрибуты сотрудника и обеспечивает их валидацию (проверку типов
и диапазонов значений) в момент создания или изменения объекта.
"""

class Employee:
    """
    Базовый класс-сущность (Entity).
    
    Отвечает ИСКЛЮЧИТЕЛЬНО за хранение данных и их валидацию.
    Не содержит абстрактных методов и бизнес-логики расчета зарплат.
    Используется как родитель для AbstractEmployee.
    """
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        """
        Инициализирует нового сотрудника.
        Атрибуты устанавливаются через сеттеры для немедленной валидации.
        """
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary

    # --- Свойства (Getters & Setters) ---

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        """
        Устанавливает уникальный идентификатор.
        Валидация: Должен быть положительным целым числом.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"ID должен быть положительным целым числом. Получено: {value}")
        self.__id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        """
        Устанавливает имя сотрудника.
        Валидация: Не может быть пустой строкой или состоять только из пробелов.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя сотрудника не может быть пустой строкой.")
        self.__name = value.strip()

    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value: str):
        """
        Устанавливает название отдела.
        Валидация: Должно быть строкой.
        """
        if not isinstance(value, str):
            raise ValueError("Название отдела должно быть строкой.")
        self.__department = value.strip()

    @property
    def base_salary(self) -> float:
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value: float):
        """
        Устанавливает базовый оклад.
        Валидация: Должен быть неотрицательным числом.
        """
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Базовая зарплата должна быть положительным числом. Получено: {value}")
        self.__base_salary = float(value)

    def __str__(self):
        return f"Сотрудник [id: {self.id}, имя: {self.name}, отдел: {self.department}]"
