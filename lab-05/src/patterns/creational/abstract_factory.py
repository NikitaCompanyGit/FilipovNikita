# Abstract Factory (Абстрактная фабрика)
# =========================================
# Предоставляет интерфейс для создания семейств связанных или зависимых объектов
# без указания их конкретных классов.

from abc import ABC, abstractmethod
from typing import List

class CompanyFactory(ABC):
    """
    Абстрактная фабрика для создания компаний разных типов.
    Гарантирует, что все компоненты (сотрудники, отделы) согласованы между собой.
    """
    
    @abstractmethod
    def create_manager(self, emp_id: int, name: str, department: str,
                      base_salary: float, bonus: float) -> 'Manager':
        """Создание менеджера, специфичного для типа компании."""
        pass
    
    @abstractmethod
    def create_developer(self, emp_id: int, name: str, department: str,
                        base_salary: float, seniority: str,
                        tech_stack: List[str]) -> 'Developer':
        """Создание разработчика, специфичного для типа компании."""
        pass
    
    @abstractmethod
    def create_salesperson(self, emp_id: int, name: str, department: str,
                          base_salary: float, commission_rate: float) -> 'Salesperson':
        """Создание продавца, специфичного для типа компании."""
        pass
    
    @abstractmethod
    def create_department(self, name: str) -> 'Department':
        """Создание отдела, специфичного для типа компании."""
        pass
    
    @abstractmethod
    def create_project(self, project_id: int, name: str, description: str,
                      deadline: str) -> 'Project':
        """Создание проекта, специфичного для типа компании."""
        pass


class TechCompanyFactory(CompanyFactory):
    """
    Фабрика для создания компонентов ИТ-компании.
    Создает множество высокооплачиваемых разработчиков, проектов на cutting-edge технологиях.
    """
    
    def create_manager(self, emp_id: int, name: str, department: str,
                      base_salary: float, bonus: float) -> 'Manager':
        """
        Создание менеджера ИТ-компании.
        ИТ-менеджеры обычно имеют высокий бонус за достижение целей.
        """
        print(f"[TechCompanyFactory] Создание Tech-Manager: {name}")
        # Бонус для tech-компании повышен на 50% (мотивирующий фактор)
        tech_bonus = bonus * 1.5
        print(f"  Бонус увеличен до {tech_bonus} (ИТ-бонус: +50%)")
        # return Manager(emp_id, name, department, base_salary, tech_bonus)
        return f"Tech Manager({emp_id}, {name}, {department}, {base_salary}, {tech_bonus})"
    
    def create_developer(self, emp_id: int, name: str, department: str,
                        base_salary: float, seniority: str,
                        tech_stack: List[str]) -> 'Developer':
        """
        Создание разработчика ИТ-компании.
        Требует обязательно указать стек технологий (Python, Java, Go и т.д.)
        """
        print(f"[TechCompanyFactory] Создание Tech-Developer: {name} ({seniority})")
        # Для ИТ-компании обязателен стек технологий
        if not tech_stack:
            tech_stack = ['Python', 'Java']  # По умолчанию
            print(f"  Стек по умолчанию: {tech_stack}")
        # return Developer(emp_id, name, department, base_salary, seniority, tech_stack)
        return f"Tech Developer({emp_id}, {name}, {department}, {base_salary}, {seniority}, {tech_stack})"
    
    def create_salesperson(self, emp_id: int, name: str, department: str,
                          base_salary: float, commission_rate: float) -> 'Salesperson':
        """
        Создание продавца ИТ-компании (обычно продаёт программные решения).
        Комиссия зависит от выручки (выше, чем в обычных компаниях).
        """
        print(f"[TechCompanyFactory] Создание Tech-Salesperson: {name}")
        # Для ИТ-продавцов комиссия может быть выше (до 20%)
        tech_commission = min(commission_rate * 2, 0.20)
        print(f"  Комиссия: {tech_commission*100}% (ИТ-комиссия)")
        # return Salesperson(emp_id, name, department, base_salary, tech_commission)
        return f"Tech Salesperson({emp_id}, {name}, {department}, {base_salary}, {tech_commission})"
    
    def create_department(self, name: str) -> 'Department':
        """
        Создание отдела ИТ-компании.
        Отделы обычно ориентированы на технологические функции.
        """
        print(f"[TechCompanyFactory] Создание Tech-Department: {name}")
        # Типичные отделы: DEV, QA, DevOps, Data Science
        if name.upper() not in ['DEV', 'QA', 'DEVOPS', 'DATA_SCIENCE', 'SECURITY']:
            print(f"  Совет: В ИТ-компаниях типичные отделы: DEV, QA, DevOps, Data Science")
        # return Department(name)
        return f"Tech Department({name})"
    
    def create_project(self, project_id: int, name: str, description: str,
                      deadline: str) -> 'Project':
        """
        Создание проекта ИТ-компании.
        Проекты обычно связаны с разработкой ПО, облачными системами и т.д.
        """
        print(f"[TechCompanyFactory] Создание Tech-Project: {name}")
        # return Project(project_id, name, description, deadline, status="planning")
        return f"Tech Project({project_id}, {name}, {description}, {deadline})"


class SalesCompanyFactory(CompanyFactory):
    """
    Фабрика для создания компонентов Продажной компании.
    Создает множество продавцов, менеджеры по продажам, проекты по развитию рынков.
    """
    
    def create_manager(self, emp_id: int, name: str, department: str,
                      base_salary: float, bonus: float) -> 'Manager':
        """
        Создание менеджера Sales-компании.
        Sales-менеджеры получают бонусы за достижение плана продаж.
        """
        print(f"[SalesCompanyFactory] Создание Sales-Manager: {name}")
        # Бонус для sales-компании зависит от плана продаж (может быть выше)
        sales_bonus = bonus * 2.0  # Высокий бонус мотивирует продажи
        print(f"  Бонус увеличен до {sales_bonus} (Sales-бонус: +100%)")
        # return Manager(emp_id, name, department, base_salary, sales_bonus)
        return f"Sales Manager({emp_id}, {name}, {department}, {base_salary}, {sales_bonus})"
    
    def create_developer(self, emp_id: int, name: str, department: str,
                        base_salary: float, seniority: str,
                        tech_stack: List[str]) -> 'Developer':
        """
        Создание разработчика Sales-компании.
        В Sales-компаниях разработчики редки, но нужны для CRM систем и аналитики.
        """
        print(f"[SalesCompanyFactory] Создание Sales-Developer: {name}")
        # Разработчики в Sales-компаниях работают с CRM, аналитикой
        print(f"  Рекомендуемый стек: Python/SQL для работы с данными")
        # return Developer(emp_id, name, department, base_salary, seniority, tech_stack)
        return f"Sales Developer({emp_id}, {name}, {department}, {base_salary}, {seniority}, {tech_stack})"
    
    def create_salesperson(self, emp_id: int, name: str, department: str,
                          base_salary: float, commission_rate: float) -> 'Salesperson':
        """
        Создание продавца Sales-компании.
        Это главный кадровый ресурс в Sales-компаниях.
        """
        print(f"[SalesCompanyFactory] Создание Sales-Salesperson: {name}")
        # Для Sales-компаний комиссия стандартная (10-15%)
        sales_commission = min(commission_rate, 0.15)
        print(f"  Комиссия: {sales_commission*100}%")
        # return Salesperson(emp_id, name, department, base_salary, sales_commission)
        return f"Sales Salesperson({emp_id}, {name}, {department}, {base_salary}, {sales_commission})"
    
    def create_department(self, name: str) -> 'Department':
        """
        Создание отдела Sales-компании.
        Отделы ориентированы на географические регионы и линии продуктов.
        """
        print(f"[SalesCompanyFactory] Создание Sales-Department: {name}")
        # Типичные отделы: SALES_EU, SALES_ASIA, SALES_AMERICAS
        if 'SALES' not in name.upper():
            print(f"  Совет: В Sales-компаниях отделы обычно начинаются с SALES_")
        # return Department(name)
        return f"Sales Department({name})"
    
    def create_project(self, project_id: int, name: str, description: str,
                      deadline: str) -> 'Project':
        """
        Создание проекта Sales-компании.
        Проекты обычно связаны с открытием рынков, кампаниями по продажам.
        """
        print(f"[SalesCompanyFactory] Создание Sales-Project: {name}")
        # return Project(project_id, name, description, deadline, status="planning")
        return f"Sales Project({project_id}, {name}, {description}, {deadline})"


class CompanyBuilder:
    """
    Упрощённый конструктор компании с использованием Abstract Factory.
    """
    
    def __init__(self, factory: CompanyFactory):
        """
        Инициализация с выбранной фабрикой.
        
        Args:
            factory: Объект CompanyFactory для создания компонентов
        """
        self.factory = factory
        self.managers = []
        self.developers = []
        self.salespersons = []
        self.departments = []
        self.projects = []
    
    def add_manager(self, emp_id: int, name: str, department: str,
                   base_salary: float, bonus: float) -> 'CompanyBuilder':
        """Добавление менеджера через фабрику."""
        manager = self.factory.create_manager(emp_id, name, department, base_salary, bonus)
        self.managers.append(manager)
        return self
    
    def add_developer(self, emp_id: int, name: str, department: str,
                     base_salary: float, seniority: str,
                     tech_stack: List[str]) -> 'CompanyBuilder':
        """Добавление разработчика через фабрику."""
        developer = self.factory.create_developer(emp_id, name, department, base_salary, seniority, tech_stack)
        self.developers.append(developer)
        return self
    
    def add_salesperson(self, emp_id: int, name: str, department: str,
                       base_salary: float, commission_rate: float) -> 'CompanyBuilder':
        """Добавление продавца через фабрику."""
        salesperson = self.factory.create_salesperson(emp_id, name, department, base_salary, commission_rate)
        self.salespersons.append(salesperson)
        return self
    
    def add_department(self, name: str) -> 'CompanyBuilder':
        """Добавление отдела через фабрику."""
        department = self.factory.create_department(name)
        self.departments.append(department)
        return self
    
    def add_project(self, project_id: int, name: str, description: str,
                   deadline: str) -> 'CompanyBuilder':
        """Добавление проекта через фабрику."""
        project = self.factory.create_project(project_id, name, description, deadline)
        self.projects.append(project)
        return self
    
    def build(self) -> dict:
        """
        Построение объекта компании со всеми компонентами.
        
        Returns:
            Словарь с компонентами компании
        """
        return {
            'managers': self.managers,
            'developers': self.developers,
            'salespersons': self.salespersons,
            'departments': self.departments,
            'projects': self.projects,
        }
