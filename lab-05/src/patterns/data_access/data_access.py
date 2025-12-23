# Data Access Patterns (Паттерны доступа к данным)
# =================================================
# Repository, Unit of Work, Specification

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic
from dataclasses import dataclass

# ======================== SPECIFICATION (СПЕЦИФИКАЦИЯ) ========================

class Specification(ABC):
    """
    Абстрактная спецификация для фильтрации объектов.
    Инкапсулирует критерии поиска.
    """
    
    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        """
        Проверить, удовлетворяет ли объект спецификации.
        
        Args:
            candidate: Объект для проверки
            
        Returns:
            True если объект соответствует критериям
        """
        pass
    
    @abstractmethod
    def get_sql(self) -> str:
        """
        Получить SQL-представление спецификации.
        
        Returns:
            SQL WHERE-clause
        """
        pass
    
    def and_spec(self, other: 'Specification') -> 'CompositeSpecification':
        """Логическое И между спецификациями."""
        return AndSpecification(self, other)
    
    def or_spec(self, other: 'Specification') -> 'CompositeSpecification':
        """Логическое ИЛИ между спецификациями."""
        return OrSpecification(self, other)
    
    def not_spec(self) -> 'CompositeSpecification':
        """Логическое НЕ спецификации."""
        return NotSpecification(self)


class CompositeSpecification(Specification):
    """Абстрактная составная спецификация."""
    pass


class SalarySpecification(Specification):
    """Спецификация для фильтрации по зарплате."""
    
    def __init__(self, min_salary: float = 0, max_salary: float = float('inf')):
        """
        Инициализация спецификации зарплаты.
        
        Args:
            min_salary: Минимальная зарплата
            max_salary: Максимальная зарплата
        """
        self.min_salary = min_salary
        self.max_salary = max_salary
    
    def is_satisfied_by(self, candidate: Dict[str, Any]) -> bool:
        """Проверка зарплаты."""
        salary = candidate.get('base_salary', 0)
        return self.min_salary <= salary <= self.max_salary
    
    def get_sql(self) -> str:
        """SQL запрос для фильтрации по зарплате."""
        return f"WHERE base_salary BETWEEN {self.min_salary} AND {self.max_salary}"


class DepartmentSpecification(Specification):
    """Спецификация для фильтрации по отделу."""
    
    def __init__(self, department: str):
        """
        Инициализация спецификации отдела.
        
        Args:
            department: Название отдела
        """
        self.department = department
    
    def is_satisfied_by(self, candidate: Dict[str, Any]) -> bool:
        """Проверка отдела."""
        return candidate.get('department') == self.department
    
    def get_sql(self) -> str:
        """SQL запрос для фильтрации по отделу."""
        return f"WHERE department = '{self.department}'"


class EmployeeTypeSpecification(Specification):
    """Спецификация для фильтрации по типу сотрудника."""
    
    def __init__(self, emp_type: str):
        """
        Инициализация спецификации типа.
        
        Args:
            emp_type: Тип сотрудника (manager, developer, salesperson и т.д.)
        """
        self.emp_type = emp_type
    
    def is_satisfied_by(self, candidate: Dict[str, Any]) -> bool:
        """Проверка типа сотрудника."""
        return candidate.get('type') == self.emp_type
    
    def get_sql(self) -> str:
        """SQL запрос для фильтрации по типу."""
        return f"WHERE type = '{self.emp_type}'"


class SkillSpecification(Specification):
    """Спецификация для фильтрации по навыкам."""
    
    def __init__(self, required_skill: str):
        """
        Инициализация спецификации навыка.
        
        Args:
            required_skill: Необходимый навык (Python, Java и т.д.)
        """
        self.required_skill = required_skill
    
    def is_satisfied_by(self, candidate: Dict[str, Any]) -> bool:
        """Проверка наличия навыка."""
        skills = candidate.get('tech_stack', [])
        return self.required_skill in skills
    
    def get_sql(self) -> str:
        """SQL запрос для поиска по навыкам."""
        return f"WHERE tech_stack LIKE '%{self.required_skill}%'"


class AndSpecification(CompositeSpecification):
    """Составная спецификация - логическое И."""
    
    def __init__(self, left: Specification, right: Specification):
        """Инициализация с двумя спецификациями."""
        self.left = left
        self.right = right
    
    def is_satisfied_by(self, candidate: Any) -> bool:
        """Проверка обеих спецификаций."""
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)
    
    def get_sql(self) -> str:
        """SQL запрос с AND."""
        left_sql = self.left.get_sql()
        right_sql = self.right.get_sql()
        return f"{left_sql} AND {right_sql.replace('WHERE', '').strip()}"


class OrSpecification(CompositeSpecification):
    """Составная спецификация - логическое ИЛИ."""
    
    def __init__(self, left: Specification, right: Specification):
        """Инициализация с двумя спецификациями."""
        self.left = left
        self.right = right
    
    def is_satisfied_by(self, candidate: Any) -> bool:
        """Проверка хотя бы одной спецификации."""
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(candidate)
    
    def get_sql(self) -> str:
        """SQL запрос с OR."""
        left_sql = self.left.get_sql()
        right_sql = self.right.get_sql()
        return f"{left_sql} OR {right_sql.replace('WHERE', '').strip()}"


class NotSpecification(CompositeSpecification):
    """Составная спецификация - логическое НЕ."""
    
    def __init__(self, spec: Specification):
        """Инициализация со спецификацией."""
        self.spec = spec
    
    def is_satisfied_by(self, candidate: Any) -> bool:
        """Проверка отрицания спецификации."""
        return not self.spec.is_satisfied_by(candidate)
    
    def get_sql(self) -> str:
        """SQL запрос с NOT."""
        sql = self.spec.get_sql()
        return f"NOT ({sql})"


# ======================== REPOSITORY (РЕПОЗИТОРИЙ) ========================

class Repository(ABC, Generic[TypeVar('T')]):
    """
    Абстрактный репозиторий для работы с данными.
    Инкапсулирует логику доступа к данным.
    """
    
    @abstractmethod
    def add(self, item: Any) -> None:
        """Добавить элемент."""
        pass
    
    @abstractmethod
    def remove(self, item_id: int) -> None:
        """Удалить элемент."""
        pass
    
    @abstractmethod
    def find_by_id(self, item_id: int) -> Optional[Any]:
        """Найти элемент по ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Any]:
        """Получить все элементы."""
        pass
    
    @abstractmethod
    def find_by_specification(self, spec: Specification) -> List[Any]:
        """Найти элементы по спецификации."""
        pass


class EmployeeRepository(Repository):
    """Репозиторий для управления сотрудниками."""
    
    def __init__(self):
        """Инициализация репозитория."""
        self._employees: Dict[int, Dict[str, Any]] = {}
        self._next_id = 1
        print("[EmployeeRepository] Инициализирован")
    
    def add(self, employee: Dict[str, Any]) -> None:
        """
        Добавить сотрудника.
        
        Args:
            employee: Словарь с данными сотрудника
        """
        emp_id = employee.get('id') or self._next_id
        self._employees[emp_id] = employee
        if emp_id >= self._next_id:
            self._next_id = emp_id + 1
        print(f"[EmployeeRepository] Добавлен сотрудник: {employee.get('name')} (ID: {emp_id})")
    
    def remove(self, emp_id: int) -> None:
        """
        Удалить сотрудника.
        
        Args:
            emp_id: ID сотрудника
        """
        if emp_id in self._employees:
            name = self._employees[emp_id].get('name')
            del self._employees[emp_id]
            print(f"[EmployeeRepository] Удалён сотрудник: {name}")
    
    def find_by_id(self, emp_id: int) -> Optional[Dict[str, Any]]:
        """
        Найти сотрудника по ID.
        
        Args:
            emp_id: ID сотрудника
            
        Returns:
            Словарь с данными сотрудника или None
        """
        return self._employees.get(emp_id)
    
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Получить всех сотрудников.
        
        Returns:
            Список сотрудников
        """
        return list(self._employees.values())
    
    def find_by_specification(self, spec: Specification) -> List[Dict[str, Any]]:
        """
        Найти сотрудников по спецификации.
        
        Args:
            spec: Спецификация для фильтрации
            
        Returns:
            Список сотрудников, соответствующих спецификации
        """
        print(f"[EmployeeRepository] Поиск по спецификации: {spec.get_sql()}")
        return [emp for emp in self._employees.values() if spec.is_satisfied_by(emp)]


class DepartmentRepository(Repository):
    """Репозиторий для управления отделами."""
    
    def __init__(self):
        """Инициализация репозитория."""
        self._departments: Dict[int, Dict[str, Any]] = {}
        self._next_id = 1
        print("[DepartmentRepository] Инициализирован")
    
    def add(self, department: Dict[str, Any]) -> None:
        """
        Добавить отдел.
        
        Args:
            department: Словарь с данными отдела
        """
        dept_id = department.get('id') or self._next_id
        self._departments[dept_id] = department
        if dept_id >= self._next_id:
            self._next_id = dept_id + 1
        print(f"[DepartmentRepository] Добавлен отдел: {department.get('name')}")
    
    def remove(self, dept_id: int) -> None:
        """
        Удалить отдел.
        
        Args:
            dept_id: ID отдела
        """
        if dept_id in self._departments:
            name = self._departments[dept_id].get('name')
            del self._departments[dept_id]
            print(f"[DepartmentRepository] Удалён отдел: {name}")
    
    def find_by_id(self, dept_id: int) -> Optional[Dict[str, Any]]:
        """
        Найти отдел по ID.
        
        Args:
            dept_id: ID отдела
            
        Returns:
            Словарь с данными отдела или None
        """
        return self._departments.get(dept_id)
    
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Получить все отделы.
        
        Returns:
            Список отделов
        """
        return list(self._departments.values())
    
    def find_by_specification(self, spec: Specification) -> List[Dict[str, Any]]:
        """
        Найти отделы по спецификации.
        
        Args:
            spec: Спецификация для фильтрации
            
        Returns:
            Список отделов, соответствующих спецификации
        """
        return [dept for dept in self._departments.values() if spec.is_satisfied_by(dept)]


# ======================== UNIT OF WORK (ЕДИНИЦА РАБОТЫ) ========================

class UnitOfWork:
    """
    Паттерн Unit of Work для управления транзакциями.
    Гарантирует консистентность при комплексных операциях.
    """
    
    def __init__(self, employee_repo: EmployeeRepository, 
                 department_repo: DepartmentRepository):
        """
        Инициализация Unit of Work.
        
        Args:
            employee_repo: Репозиторий сотрудников
            department_repo: Репозиторий отделов
        """
        self.employees = employee_repo
        self.departments = department_repo
        self._transaction_active = False
        self._changes: List[Dict[str, Any]] = []
    
    def begin_transaction(self) -> None:
        """Начать транзакцию."""
        self._transaction_active = True
        self._changes.clear()
        print("[UnitOfWork] Транзакция начата")
    
    def register_new(self, entity_type: str, entity: Dict[str, Any]) -> None:
        """
        Регистрировать новую сущность.
        
        Args:
            entity_type: Тип сущности (employee, department)
            entity: Данные сущности
        """
        if not self._transaction_active:
            raise RuntimeError("Транзакция не начата")
        
        self._changes.append({
            'type': 'insert',
            'entity_type': entity_type,
            'entity': entity
        })
        print(f"[UnitOfWork] Зарегистрирована вставка: {entity_type}")
    
    def register_dirty(self, entity_type: str, entity_id: int, changes: Dict[str, Any]) -> None:
        """
        Регистрировать изменение сущности.
        
        Args:
            entity_type: Тип сущности
            entity_id: ID сущности
            changes: Изменения
        """
        if not self._transaction_active:
            raise RuntimeError("Транзакция не начата")
        
        self._changes.append({
            'type': 'update',
            'entity_type': entity_type,
            'entity_id': entity_id,
            'changes': changes
        })
        print(f"[UnitOfWork] Зарегистрировано обновление: {entity_type} ID={entity_id}")
    
    def register_removed(self, entity_type: str, entity_id: int) -> None:
        """
        Регистрировать удаление сущности.
        
        Args:
            entity_type: Тип сущности
            entity_id: ID сущности
        """
        if not self._transaction_active:
            raise RuntimeError("Транзакция не начата")
        
        self._changes.append({
            'type': 'delete',
            'entity_type': entity_type,
            'entity_id': entity_id
        })
        print(f"[UnitOfWork] Зарегистрировано удаление: {entity_type} ID={entity_id}")
    
    def commit(self) -> bool:
        """
        Подтвердить транзакцию (выполнить все изменения).
        
        Returns:
            True если успешно, False иначе
        """
        if not self._transaction_active:
            raise RuntimeError("Транзакция не начата")
        
        print(f"\n[UnitOfWork] Подтверждение {len(self._changes)} изменений...")
        
        try:
            for change in self._changes:
                if change['type'] == 'insert':
                    if change['entity_type'] == 'employee':
                        self.employees.add(change['entity'])
                    elif change['entity_type'] == 'department':
                        self.departments.add(change['entity'])
                
                elif change['type'] == 'update':
                    print(f"  [UnitOfWork] Обновление: {change['entity_type']} -> {change['changes']}")
                
                elif change['type'] == 'delete':
                    if change['entity_type'] == 'employee':
                        self.employees.remove(change['entity_id'])
                    elif change['entity_type'] == 'department':
                        self.departments.remove(change['entity_id'])
            
            self._transaction_active = False
            self._changes.clear()
            print("[UnitOfWork] ✓ Транзакция успешно подтверждена\n")
            return True
        
        except Exception as e:
            self.rollback()
            print(f"[UnitOfWork] ✗ Ошибка при подтверждении: {e}")
            return False
    
    def rollback(self) -> None:
        """Откатить транзакцию (отменить все изменения)."""
        print(f"[UnitOfWork] Откат {len(self._changes)} изменений...")
        self._transaction_active = False
        self._changes.clear()
        print("[UnitOfWork] Транзакция отменена\n")
