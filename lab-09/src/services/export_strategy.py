import os
import csv
import json
from abc import ABC, abstractmethod
from typing import List, Any

class IExportStrategy(ABC):
    """
    Абстрактный интерфейс для экспорта данных.
    Применяет паттерн Strategy (OCP).
    """

    @abstractmethod
    def export(self, data: List[Any], filename: str, headers: List[str]) -> None:
        """
        Экспортирует данные в файл.

        :param data: Список данных для экспорта.
        :param filename: Путь к файлу.
        :param headers: Заголовки столбцов.
        """
        pass


class CSVExportStrategy(IExportStrategy):
    """
    Стратегия экспорта в CSV формат.
    """

    def export(self, data: List[Any], filename: str, headers: List[str]) -> None:
        """
        Экспортирует данные в CSV с кодировкой utf-8-sig (для Excel).
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(headers)
            writer.writerows(data)

        print(f"[INFO] Данные экспортированы в CSV: {filename}")


class JSONExportStrategy(IExportStrategy):
    """
    Стратегия экспорта в JSON формат.
    """

    def export(self, data: List[Any], filename: str, headers: List[str]) -> None:
        """
        Экспортирует данные в JSON.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Преобразуем данные в список словарей
        json_data = []
        for row in data:
            json_data.append(dict(zip(headers, row)))

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        print(f"[INFO] Данные экспортированы в JSON: {filename}")


class CompanyExporter:
    """
    Экспортёр данных компании.
    Использует паттерн Strategy для гибкого выбора формата (OCP).
    """

    def __init__(self, strategy: IExportStrategy):
        """
        :param strategy: Стратегия экспорта (CSV, JSON, и т.д.).
        """
        self.strategy = strategy

    def export_employees(self, employees: List[Any], filename: str) -> None:
        """
        Экспортирует список сотрудников.
        """
        headers = ["ID", "Name", "Department", "Type", "Salary", "Info"]
        data = [
            [emp.id, emp.name, emp.department, emp.__class__.__name__, 
             emp.calculate_salary(), str(emp)]
            for emp in employees
        ]
        self.strategy.export(data, filename, headers)

    def export_projects(self, projects: List[Any], filename: str) -> None:
        """
        Экспортирует список проектов.
        """
        headers = ["ID", "Name", "Status", "Deadline", "Team Size", "Budget"]
        data = [
            [proj.id, proj.name, proj.status, 
             proj.deadline.strftime("%Y-%m-%d"),
             proj.get_team_size(), proj.calculate_total_salary()]
            for proj in projects
        ]
        self.strategy.export(data, filename, headers)