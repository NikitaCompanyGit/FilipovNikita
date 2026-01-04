# Factory Method (Фабричный метод) - Рефакторинг EmployeeFactory
# ================================================================
# Определяет интерфейс для создания объекта, но оставляет подклассам
# решение о том, какой класс инстанцировать.

from abc import ABC, abstractmethod
from typing import Dict, Any, List

# Предполагаем, что базовые классы импортируются из существующей ЛР№4
# from src.base.abstract_employee import AbstractEmployee
# from src.specialists.manager import Manager
# from src.specialists.developer import Developer
# from src.specialists.salesperson import Salesperson
# from src.specialists.ordinary_employee import OrdinaryEmployee

class EmployeeFactory(ABC):
    """
    Абстрактный базовый класс для фабрик сотрудников.
    Определяет интерфейс для создания объектов сотрудников.
    """
    
    @abstractmethod
    def create_employee(self, emp_id: int, name: str, department: str, 
                       base_salary: float, **kwargs) -> 'AbstractEmployee':
        """
        Абстрактный метод для создания сотрудника.
        Реализуется в конкретных фабриках.
        
        Args:
            emp_id: ID сотрудника
            name: Имя сотрудника
            department: Отдел
            base_salary: Базовая зарплата
            **kwargs: Дополнительные параметры для специфических типов
            
        Returns:
            Объект AbstractEmployee
        """
        pass
    
    @abstractmethod
    def get_employee_type(self) -> str:
        """
        Возвращает тип сотрудника, создаваемый этой фабрикой.
        
        Returns:
            Строка с типом сотрудника
        """
        pass


class ManagerFactory(EmployeeFactory):
    """Конкретная фабрика для создания менеджеров."""
    
    def create_employee(self, emp_id: int, name: str, department: str,
                       base_salary: float, **kwargs) -> 'Manager':
        """
        Создание менеджера с бонусом.
        
        Args:
            emp_id: ID менеджера
            name: Имя менеджера
            department: Отдел менеджера
            base_salary: Базовая зарплата
            **kwargs: Должен содержать 'bonus' - размер бонуса
            
        Returns:
            Объект Manager
        """
        bonus = kwargs.get('bonus', 0.0)
        print(f"[Factory] Создание Manager: {name}, бонус: {bonus}")
        # Предполагаемый импорт: from src.specialists.manager import Manager
        # return Manager(emp_id, name, department, base_salary, bonus)
        return f"Manager({emp_id}, {name}, {department}, {base_salary}, {bonus})"
    
    def get_employee_type(self) -> str:
        return "manager"


class DeveloperFactory(EmployeeFactory):
    """Конкретная фабрика для создания разработчиков."""
    
    def create_employee(self, emp_id: int, name: str, department: str,
                       base_salary: float, **kwargs) -> 'Developer':
        """
        Создание разработчика с уровнем квалификации.
        
        Args:
            emp_id: ID разработчика
            name: Имя разработчика
            department: Отдел (обычно DEV)
            base_salary: Базовая зарплата
            **kwargs: Должен содержать 'seniority' - уровень (junior/middle/senior),
                     'tech_stack' - список технологий
            
        Returns:
            Объект Developer
        """
        seniority = kwargs.get('seniority', 'junior')
        tech_stack = kwargs.get('tech_stack', [])
        print(f"[Factory] Создание Developer: {name}, уровень: {seniority}, стек: {tech_stack}")
        # Предполагаемый импорт: from src.specialists.developer import Developer
        # return Developer(emp_id, name, department, base_salary, seniority, tech_stack)
        return f"Developer({emp_id}, {name}, {department}, {base_salary}, {seniority}, {tech_stack})"
    
    def get_employee_type(self) -> str:
        return "developer"


class SalespersonFactory(EmployeeFactory):
    """Конкретная фабрика для создания продавцов."""
    
    def create_employee(self, emp_id: int, name: str, department: str,
                       base_salary: float, **kwargs) -> 'Salesperson':
        """
        Создание продавца с комиссией.
        
        Args:
            emp_id: ID продавца
            name: Имя продавца
            department: Отдел (обычно SALES)
            base_salary: Базовая зарплата
            **kwargs: Должен содержать 'commission_rate' - процент комиссии
            
        Returns:
            Объект Salesperson
        """
        commission_rate = kwargs.get('commission_rate', 0.0)
        print(f"[Factory] Создание Salesperson: {name}, комиссия: {commission_rate*100}%")
        # Предполагаемый импорт: from src.specialists.salesperson import Salesperson
        # return Salesperson(emp_id, name, department, base_salary, commission_rate)
        return f"Salesperson({emp_id}, {name}, {department}, {base_salary}, {commission_rate})"
    
    def get_employee_type(self) -> str:
        return "salesperson"


class OrdinaryEmployeeFactory(EmployeeFactory):
    """Конкретная фабрика для создания штатных сотрудников."""
    
    def create_employee(self, emp_id: int, name: str, department: str,
                       base_salary: float, **kwargs) -> 'OrdinaryEmployee':
        """
        Создание обычного штатного сотрудника.
        
        Args:
            emp_id: ID сотрудника
            name: Имя сотрудника
            department: Отдел сотрудника
            base_salary: Базовая зарплата
            **kwargs: Дополнительные параметры (не требуются)
            
        Returns:
            Объект OrdinaryEmployee
        """
        print(f"[Factory] Создание OrdinaryEmployee: {name}")
        # Предполагаемый импорт: from src.specialists.ordinary_employee import OrdinaryEmployee
        # return OrdinaryEmployee(emp_id, name, department, base_salary)
        return f"OrdinaryEmployee({emp_id}, {name}, {department}, {base_salary})"
    
    def get_employee_type(self) -> str:
        return "employee"


class EmployeeFactoryManager:
    """
    Менеджер фабрик сотрудников.
    Координирует создание сотрудников через подходящую фабрику.
    """
    
    def __init__(self):
        """Инициализация с регистрацией всех доступных фабрик."""
        # Регистр фабрик (тип -> фабрика)
        self._factories: Dict[str, EmployeeFactory] = {
            'manager': ManagerFactory(),
            'developer': DeveloperFactory(),
            'salesperson': SalespersonFactory(),
            'employee': OrdinaryEmployeeFactory(),
        }
    
    def register_factory(self, emp_type: str, factory: EmployeeFactory) -> None:
        """
        Регистрация новой фабрики для типа сотрудника.
        Позволяет расширять систему новыми типами сотрудников.
        
        Args:
            emp_type: Тип сотрудника (ключ)
            factory: Объект фабрики для этого типа
        """
        self._factories[emp_type] = factory
        print(f"[FactoryManager] Зарегистрирована фабрика для типа '{emp_type}'")
    
    def create_employee(self, emp_type: str, emp_id: int, name: str,
                       department: str, base_salary: float, **kwargs) -> 'AbstractEmployee':
        """
        Создание сотрудника указанного типа.
        
        Args:
            emp_type: Тип сотрудника (должен быть зарегистрирован)
            emp_id: ID сотрудника
            name: Имя сотрудника
            department: Отдел
            base_salary: Базовая зарплата
            **kwargs: Дополнительные параметры для конкретного типа
            
        Returns:
            Созданный объект сотрудника
            
        Raises:
            ValueError: Если тип сотрудника не зарегистрирован
        """
        if emp_type not in self._factories:
            raise ValueError(f"Неизвестный тип сотрудника: '{emp_type}'. "
                           f"Доступные типы: {list(self._factories.keys())}")
        
        factory = self._factories[emp_type]
        return factory.create_employee(emp_id, name, department, base_salary, **kwargs)
    
    def get_available_types(self) -> List[str]:
        """
        Получение списка доступных типов сотрудников.
        
        Returns:
            Список типов сотрудников
        """
        return list(self._factories.keys())
