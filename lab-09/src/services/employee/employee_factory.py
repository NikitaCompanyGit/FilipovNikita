from typing import Dict, Any, Optional
from base.abstract_employee import AbstractEmployee

class EmployeeFactory:
    """
    Фабрика для создания объектов сотрудников.

    Использует Factory Pattern для централизованного создания
    различных типов сотрудников на основе данных (словаря).

    SOLID:
    - SRP: Отвечает только за создание сотрудников
    - OCP: Легко добавлять новые типы через регистрацию
    - DIP: Зависит от абстракции (AbstractEmployee)

    ПАТТЕРН: Factory Method + Registry Pattern
    """

    def __init__(self):
        """
        Инициализация фабрики.

        _registry: Словарь {тип_сотрудника: класс_сотрудника}
        Позволяет регистрировать новые типы динамически.
        """
        self._registry: Dict[str, type] = {}

    def register(self, employee_type: str, employee_class: type) -> None:
        """
        Регистрирует новый тип сотрудника в фабрике.

        :param employee_type: Строковый идентификатор типа (например, 'manager').
        :param employee_class: Класс сотрудника для создания.
        """
        self._registry[employee_type.lower()] = employee_class

    def create(self, data: Dict[str, Any]) -> Optional[AbstractEmployee]:
        """
        Создаёт объект сотрудника на основе данных.

        :param data: Словарь с данными сотрудника.
                     Обязательно должен содержать поле 'type'.
        :returns: Объект сотрудника или None, если тип не зарегистрирован.
        :raises KeyError: Если в данных отсутствует поле 'type'.
        """
        employee_type = data.get("type")

        if not employee_type:
            raise KeyError("Отсутствует поле 'type' в данных сотрудника.")

        employee_class = self._registry.get(employee_type.lower())

        if not employee_class:
            raise ValueError(
                f"Неизвестный тип сотрудника: '{employee_type}'. "
                f"Зарегистрированные типы: {list(self._registry.keys())}"
            )

        # Вызываем метод from_dict класса сотрудника
        return employee_class.from_dict(data)

    def get_registered_types(self) -> list:
        """
        Возвращает список зарегистрированных типов сотрудников.

        :returns: Список строк с типами сотрудников.
        """
        return list(self._registry.keys())

    def is_registered(self, employee_type: str) -> bool:
        """
        Проверяет, зарегистрирован ли тип сотрудника.

        :param employee_type: Тип для проверки.
        :returns: True, если зарегистрирован, иначе False.
        """
        return employee_type.lower() in self._registry


# Глобальный экземпляр фабрики (Singleton Pattern)
employee_factory = EmployeeFactory()


# --- Пример использования (в отдельном модуле инициализации) ---
"""
from specialists.ordinary_employee import OrdinaryEmployee
from specialists.manager import Manager
from specialists.developer import Developer
from specialists.salesperson import Salesperson

# Регистрация всех типов сотрудников при старте приложения
employee_factory.register("employee", OrdinaryEmployee)
employee_factory.register("manager", Manager)
employee_factory.register("developer", Developer)
employee_factory.register("salesperson", Salesperson)

# Использование:
data = {
    "type": "manager",
    "id": 1,
    "name": "Alice",
    "department": "Sales",
    "base_salary": 50000,
    "bonus": 10000
}

manager = employee_factory.create(data)