import json
import os
from typing import List
from organization.department import Department
from organization.project import Project
from services.link_resolver import LinkResolver
from factory import EmployeeFactory

class CompanySerializer:
    """
    Сериализатор для сохранения и загрузки компании в JSON.
    Отвечает ТОЛЬКО за JSON операции (SRP).
    """

    @staticmethod
    def save_to_json(
        company_name: str,
        departments: List[Department],
        projects: List[Project],
        filename: str
    ) -> None:
        """
        Сохраняет полное состояние компании в JSON.

        :param company_name: Название компании.
        :param departments: Список отделов.
        :param projects: Список проектов.
        :param filename: Путь к файлу.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        data = {
            "company_name": company_name,
            "departments": [
                {
                    "name": dept.name,
                    "employees": [e.to_dict() for e in dept.get_employees()]
                } for dept in departments
            ],
            "projects": [p.to_dict() for p in projects]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[INFO] Компания сохранена в {filename}")

    @staticmethod
    def load_from_json(filename: str) -> dict:
        """
        Загружает компанию из JSON.

        :returns: Словарь с ключами: company_name, departments, projects.
        :raises FileNotFoundError: Если файл не найден.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 1. Восстанавливаем отделы и сотрудников
        departments = []
        for dept_data in data["departments"]:
            dept = Department(dept_data["name"])
            for emp_data in dept_data["employees"]:
                e_type = emp_data.pop("type")
                emp = EmployeeFactory.create_employee(e_type, **emp_data)
                dept.add_employee(emp)
            departments.append(dept)

        # 2. Создаём карту сотрудников для восстановления связей
        employee_map = LinkResolver.build_employee_map(departments)

        # 3. Восстанавливаем проекты
        projects = []
        for proj_data in data["projects"]:
            team_ids = proj_data.pop("team_ids")
            project = Project(
                proj_data["id"],
                proj_data["name"],
                proj_data["description"],
                proj_data["deadline"],
                proj_data["status"]
            )
            # Восстановление связей с сотрудниками
            LinkResolver.restore_project_links(project, team_ids, employee_map)
            projects.append(project)

        return {
            "company_name": data["company_name"],
            "departments": departments,
            "projects": projects
        }