import json
import os
from typing import List, Dict, Any
from base.abstract_employee import AbstractEmployee
from factory import EmployeeFactory

class DepartmentRepository:
    """
    Репозиторий для сохранения и загрузки отдела.
    Отвечает ТОЛЬКО за работу с файлами (SRP).
    """

    @staticmethod
    def _ensure_directory(filename: str) -> None:
        """Создаёт директорию для файла, если она не существует."""
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"[INFO] Создана директория: {directory}")
            except OSError as e:
                print(f"[ERROR] Не удалось создать директорию {directory}: {e}")
                raise

    @staticmethod
    def save_to_file(
        department_name: str, 
        employees: List[AbstractEmployee], 
        filename: str
    ) -> None:
        """
        Сохраняет данные отдела в JSON-файл.

        :param department_name: Название отдела.
        :param employees: Список сотрудников отдела.
        :param filename: Путь к файлу (например, 'docs/json/dept.json').
        """
        DepartmentRepository._ensure_directory(filename)

        data = {
            "department_name": department_name,
            "employees": [emp.to_dict() for emp in employees]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[INFO] Отдел сохранен в файл: {filename}")

    @staticmethod
    def load_from_file(filename: str) -> Dict[str, Any]:
        """
        Загружает данные отдела из JSON-файла.

        :param filename: Путь к файлу.
        :returns: Словарь с ключами 'department_name' и 'employees'.
        :raises FileNotFoundError: Если файл не найден.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл не найден: {filename}")

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Восстановление объектов сотрудников через фабрику
        employees = []
        for emp_data in data["employees"]:
            emp_type = emp_data.pop("type")
            try:
                employee = EmployeeFactory.create_employee(emp_type, **emp_data)
                employees.append(employee)
            except ValueError as e:
                print(f"[WARNING] Ошибка загрузки сотрудника: {e}")

        return {
            "department_name": data["department_name"],
            "employees": employees
        }