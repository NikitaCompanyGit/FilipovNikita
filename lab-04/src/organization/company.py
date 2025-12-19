import json
import os
import csv
from typing import List, Optional, Dict
from base.abstract_employee import AbstractEmployee
from organization.department import Department
from organization.project import Project
from base.exceptions import *
from factory import EmployeeFactory

class Company:
    """
    Класс Компании (Root Aggregator / Facade).
    
    Является корневым объектом системы.
    - Агрегирует Отделы (Departments).
    - Агрегирует Проекты (Projects).
    - Обеспечивает глобальную валидацию (уникальность ID).
    - Управляет зависимостями: запрещает удаление используемых данных.
    - Отвечает за полную сериализацию/десериализацию всей системы.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.__departments: List[Department] = []
        self.__projects: List[Project] = []

    # --- Управление отделами ---
    
    def add_department(self, department: Department) -> None:
        """Добавляет новый отдел, проверяя уникальность названия."""
        if any(d.name == department.name for d in self.__departments):
            raise DuplicateIdError(f"Отдел '{department.name}' уже существует.")
        self.__departments.append(department)

    def get_departments(self) -> List[Department]:
        return self.__departments

    def remove_department(self, dept_name: str) -> None:
        """
        Удаляет отдел.
        
        :raises DepartmentNotFoundError: Если отдел не найден.
        :raises DependencyError: Если в отделе есть сотрудники (защита данных).
        """
        dept = next((d for d in self.__departments if d.name == dept_name), None)
        if not dept:
            raise DepartmentNotFoundError(f"Отдел {dept_name} не найден.")
        
        if len(dept) > 0:
            raise DependencyError(f"Нельзя удалить отдел '{dept_name}', в нем есть сотрудники.")
        
        self.__departments.remove(dept)

    # --- Управление проектами ---
    
    def add_project(self, project: Project) -> None:
        """Добавляет проект, проверяя уникальность ID."""
        if any(p.id == project.id for p in self.__projects):
            raise DuplicateIdError(f"Проект с ID {project.id} уже существует.")
        self.__projects.append(project)

    def get_projects(self) -> List[Project]:
        return self.__projects

    # --- Работа с сотрудниками (Global Scope) ---
    
    def get_all_employees(self) -> List[AbstractEmployee]:
        """Возвращает плоский список всех сотрудников из всех отделов."""
        all_emps = []
        for dept in self.__departments:
            all_emps.extend(dept.get_employees())
        return all_emps

    def find_employee_by_id(self, emp_id: int) -> Optional[AbstractEmployee]:
        """Глобальный поиск сотрудника по ID во всех отделах."""
        for dept in self.__departments:
            found = dept.find_employee_by_id(emp_id)
            if found:
                return found
        return None

    def remove_employee_globally(self, emp_id: int) -> None:
        """
        Удаляет сотрудника из компании.
        
        :raises DependencyError: Если сотрудник занят в активном проекте.
        :raises EmployeeNotFoundError: Если сотрудник не найден.
        """
        # 1. Проверка ссылочной целостности: занятость в проектах
        for proj in self.__projects:
            if any(e.id == emp_id for e in proj.get_team()):
                raise DependencyError(f"Сотрудник {emp_id} занят в проекте '{proj.name}'. Сначала удалите его из команды.")

        # 2. Поиск и удаление
        employee = self.find_employee_by_id(emp_id)
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник {emp_id} не найден.")

        for dept in self.__departments:
            if employee in dept:
                dept.remove_employee(emp_id)
                return

    def calculate_total_monthly_cost(self) -> float:
        """Рассчитывает общие ежемесячные затраты на зарплаты по всей компании."""
        return sum(d.calculate_total_salary() for d in self.__departments)

    # --- Сериализация и Экспорт (Complex Logic) ---
    
    def save_to_json(self, filename: str) -> None:
        """
        Сохраняет полное состояние компании в JSON.
        - Сотрудники сохраняются внутри своих отделов (полные данные).
        - Проекты сохраняют только список ID своей команды (ссылки).
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            "company_name": self.name,
            "departments": [
                {
                    "name": dept.name,
                    "employees": [e.to_dict() for e in dept.get_employees()]
                } for dept in self.__departments
            ],
            "projects": [p.to_dict() for p in self.__projects]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Компания сохранена в {filename}")

    @classmethod
    def load_from_json(cls, filename: str) -> 'Company':
        """
        Восстанавливает компанию из JSON.
        
        Реализует сложную логику восстановления связей (Linkage):
        1. Загружаются отделы и создаются объекты сотрудников.
        2. Сотрудники индексируются в временную карту {ID: Объект}.
        3. Загружаются проекты.
        4. Команды проектов восстанавливаются путем поиска объектов сотрудников в карте по ID.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        company = cls(data["company_name"])
        
        # Временная карта для восстановления связей "многие-ко-многим" в проектах
        employee_map = {} 

        # 1. Восстанавливаем структуру: Компания -> Отделы -> Сотрудники
        for dept_data in data["departments"]:
            dept = Department(dept_data["name"])
            for emp_data in dept_data["employees"]:
                e_type = emp_data.pop("type")
                emp = EmployeeFactory.create_employee(e_type, **emp_data)
                dept.add_employee(emp)
                employee_map[emp.id] = emp # Регистрируем объект в карте
            company.add_department(dept)

        # 2. Восстанавливаем Проекты и линкуем (связываем) их с Сотрудниками
        for proj_data in data["projects"]:
            team_ids = proj_data.pop("team_ids")
            
            project = Project(
                proj_data["id"], 
                proj_data["name"], 
                proj_data["description"], 
                proj_data["deadline"], 
                proj_data["status"]
            )
            
            # Восстановление связей по ID
            for eid in team_ids:
                if eid in employee_map:
                    project.add_team_member(employee_map[eid])
                else:
                    print(f"[WARN] Сотрудник ID={eid} для проекта '{project.name}' не найден в штате.")
            
            company.add_project(project)

        return company

    def export_employees_csv(self, filename: str) -> None:
        """
        Экспорт полного списка сотрудников в CSV.
        Использует кодировку utf-8-sig для корректного открытия в Excel (Windows).
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["ID", "Name", "Department", "Type", "Salary", "Info"])
            
            for emp in self.get_all_employees():
                writer.writerow([
                    emp.id, 
                    emp.name, 
                    emp.department, 
                    emp.__class__.__name__, 
                    emp.calculate_salary(),
                    str(emp)
                ])
        print(f"[INFO] Отчет по сотрудникам: {filename}")

    def export_projects_csv(self, filename: str) -> None:
        """
        Экспорт списка проектов в CSV.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["ID", "Name", "Status", "Deadline", "Team Size", "Budget"])
            
            for proj in self.__projects:
                writer.writerow([
                    proj.id,
                    proj.name,
                    proj.status,
                    proj.deadline.strftime("%Y-%m-%d"),
                    proj.get_team_size(),
                    proj.calculate_total_salary()
                ])
        print(f"[INFO] Отчет по проектам: {filename}")
