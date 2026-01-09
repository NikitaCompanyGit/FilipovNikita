from typing import Dict, Any

class EmployeeSerializer:
    """
    Сервис для сериализации данных сотрудников.

    Предоставляет общие методы для преобразования объектов сотрудников
    в словари (для JSON, CSV, etc.) и обратно.

    SOLID:
    - SRP: Отвечает только за сериализацию/десериализацию
    - OCP: Легко расширяется для новых типов сотрудников
    """

    @staticmethod
    def serialize_base_fields(employee: Any) -> Dict[str, Any]:
        """
        Сериализует базовые поля, общие для всех сотрудников.

        :param employee: Объект сотрудника.
        :returns: Словарь с базовыми полями (id, name, department, base_salary).
        """
        return {
            "id": employee.id,
            "name": employee.name,
            "department": employee.department,
            "base_salary": employee.base_salary
        }

    @staticmethod
    def add_employee_type(data: Dict[str, Any], employee_type: str) -> Dict[str, Any]:
        """
        Добавляет поле 'type' в словарь данных.

        Используется для идентификации типа сотрудника при десериализации.

        :param data: Словарь с данными сотрудника.
        :param employee_type: Тип сотрудника ('employee', 'manager', 'developer', etc.).
        :returns: Обновлённый словарь.
        """
        data["type"] = employee_type
        return data

    @staticmethod
    def serialize_list_field(items: list) -> list:
        """
        Сериализует список элементов.

        Используется для сохранения списков (например, tech_stack у Developer).

        :param items: Список элементов.
        :returns: Сериализованный список.
        """
        return list(items) if items else []

    @staticmethod
    def deserialize_list_field(data: Dict[str, Any], field_name: str) -> list:
        """
        Десериализует поле-список из словаря.

        :param data: Словарь с данными.
        :param field_name: Название поля.
        :returns: Список или пустой список, если поле отсутствует.
        """
        return data.get(field_name, [])