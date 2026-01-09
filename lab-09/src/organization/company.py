from typing import List
from organization.department import Department
from organization.project import Project
from services.department_manager import DepartmentManager
from services.project_manager import ProjectManager
from services.employee_manager import EmployeeManager
from services.dependency_validator import DependencyValidator
from services.cost_calculator import CostCalculator
from services.company_serializer import CompanySerializer
from services.export_strategy import CompanyExporter, CSVExportStrategy

class Company:
    """
    Класс Компании (Facade / Coordinator).

    РЕФАКТОРИНГ:
    ✅ SRP: Класс отвечает ТОЛЬКО за координацию сервисов.
    ✅ DIP: Зависит от абстракций (сервисов), а не от деталей.
    ✅ OCP: Легко добавить новые функции через сервисы.

    ДО рефакторинга: 300+ строк, 8 обязанностей
    ПОСЛЕ рефакторинга: ~80 строк, 1 обязанность (координация)
    """

    def __init__(self, name: str):
        self.name = name

        # Инициализация сервисов (Dependency Injection)
        self._dept_manager = DepartmentManager()
        self._proj_manager = ProjectManager()
        self._emp_manager = EmployeeManager(self._dept_manager.get_departments())

    # --- Делегирование операций с отделами ---

    def add_department(self, department: Department) -> None:
        """Добавляет отдел. Делегирует в DepartmentManager."""
        self._dept_manager.add_department(department)

    def get_departments(self) -> List[Department]:
        """Возвращает список отделов. Делегирует в DepartmentManager."""
        return self._dept_manager.get_departments()

    def remove_department(self, dept_name: str) -> None:
        """
        Удаляет отдел с проверкой зависимостей.
        Делегирует в DepartmentManager + DependencyValidator.
        """
        dept = self._dept_manager.get_department_by_name(dept_name)
        DependencyValidator.validate_department_removal(dept)
        self._dept_manager.remove_department(dept_name)

    # --- Делегирование операций с проектами ---

    def add_project(self, project: Project) -> None:
        """Добавляет проект. Делегирует в ProjectManager."""
        self._proj_manager.add_project(project)

    def get_projects(self) -> List[Project]:
        """Возвращает список проектов. Делегирует в ProjectManager."""
        return self._proj_manager.get_projects()

    # --- Делегирование операций с сотрудниками ---

    def get_all_employees(self):
        """Возвращает всех сотрудников. Делегирует в EmployeeManager."""
        return self._emp_manager.get_all_employees()

    def find_employee_by_id(self, emp_id: int):
        """Ищет сотрудника по ID. Делегирует в EmployeeManager."""
        return self._emp_manager.find_employee_by_id(emp_id)

    def remove_employee_globally(self, emp_id: int) -> None:
        """
        Удаляет сотрудника с проверкой зависимостей.
        Делегирует в EmployeeManager + DependencyValidator.
        """
        # 1. Проверка зависимостей
        DependencyValidator.validate_employee_removal(
            emp_id, 
            self._proj_manager.get_projects()
        )

        # 2. Поиск сотрудника
        employee = self._emp_manager.find_employee_by_id(emp_id)
        DependencyValidator.validate_employee_exists(employee, emp_id)

        # 3. Удаление
        dept = self._emp_manager.find_department_for_employee(emp_id)
        if dept:
            self._emp_manager.remove_employee_from_department(emp_id, dept)

    # --- Делегирование расчётов ---

    def calculate_total_monthly_cost(self) -> float:
        """Рассчитывает ФОТ компании. Делегирует в CostCalculator."""
        return CostCalculator.calculate_total_monthly_cost(
            self._dept_manager.get_departments()
        )

    # --- Делегирование сериализации ---

    def save_to_json(self, filename: str) -> None:
        """Сохраняет компанию в JSON. Делегирует в CompanySerializer."""
        CompanySerializer.save_to_json(
            self.name,
            self._dept_manager.get_departments(),
            self._proj_manager.get_projects(),
            filename
        )

    @classmethod
    def load_from_json(cls, filename: str) -> 'Company':
        """Загружает компанию из JSON. Делегирует в CompanySerializer."""
        data = CompanySerializer.load_from_json(filename)

        company = cls(data["company_name"])
        for dept in data["departments"]:
            company.add_department(dept)
        for proj in data["projects"]:
            company.add_project(proj)

        return company

    # --- Делегирование экспорта (Strategy Pattern) ---

    def export_employees_csv(self, filename: str) -> None:
        """Экспортирует сотрудников в CSV. Делегирует в CompanyExporter."""
        exporter = CompanyExporter(CSVExportStrategy())
        exporter.export_employees(self.get_all_employees(), filename)

    def export_projects_csv(self, filename: str) -> None:
        """Экспортирует проекты в CSV. Делегирует в CompanyExporter."""
        exporter = CompanyExporter(CSVExportStrategy())
        exporter.export_projects(self._proj_manager.get_projects(), filename)