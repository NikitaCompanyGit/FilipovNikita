# Builder (Строитель)
# ====================
# Отделяет конструирование сложного объекта от его представления,
# позволяя пошагово строить объект.

from typing import List, Optional

class EmployeeBuilder:
    """
    Паттерн Builder для пошагового создания объектов сотрудников.
    Реализует fluent-интерфейс (method chaining) для удобства использования.
    """
    
    def __init__(self):
        """Инициализация builder с пустыми значениями."""
        self._id: Optional[int] = None
        self._name: Optional[str] = None
        self._department: Optional[str] = None
        self._base_salary: Optional[float] = None
        self._employee_type: str = "employee"  # По умолчанию обычный сотрудник
        
        # Дополнительные параметры для специфических типов
        self._bonus: Optional[float] = None
        self._seniority: Optional[str] = None
        self._tech_stack: List[str] = []
        self._commission_rate: Optional[float] = None
    
    def set_id(self, emp_id: int) -> 'EmployeeBuilder':
        """
        Установить ID сотрудника.
        
        Args:
            emp_id: Уникальный идентификатор сотрудника
            
        Returns:
            self для chaining
        """
        if emp_id <= 0:
            raise ValueError(f"ID должен быть положительным, получено: {emp_id}")
        self._id = emp_id
        print(f"  [Builder] Установлен ID: {emp_id}")
        return self
    
    def set_name(self, name: str) -> 'EmployeeBuilder':
        """
        Установить имя сотрудника.
        
        Args:
            name: Полное имя сотрудника
            
        Returns:
            self для chaining
        """
        if not name or len(name.strip()) == 0:
            raise ValueError("Имя не может быть пустым")
        self._name = name.strip()
        print(f"  [Builder] Установлено имя: {self._name}")
        return self
    
    def set_department(self, department: str) -> 'EmployeeBuilder':
        """
        Установить отдел сотрудника.
        
        Args:
            department: Название отдела
            
        Returns:
            self для chaining
        """
        if not department or len(department.strip()) == 0:
            raise ValueError("Отдел не может быть пустым")
        self._department = department.strip()
        print(f"  [Builder] Установлен отдел: {self._department}")
        return self
    
    def set_base_salary(self, base_salary: float) -> 'EmployeeBuilder':
        """
        Установить базовую зарплату.
        
        Args:
            base_salary: Базовая зарплата в тысячах (обычно)
            
        Returns:
            self для chaining
        """
        if base_salary < 0:
            raise ValueError(f"Зарплата не может быть отрицательной: {base_salary}")
        self._base_salary = base_salary
        print(f"  [Builder] Установлена базовая зарплата: {base_salary}")
        return self
    
    def as_manager(self, bonus: float = 0.0) -> 'EmployeeBuilder':
        """
        Установить тип сотрудника как менеджер.
        
        Args:
            bonus: Размер бонуса менеджера
            
        Returns:
            self для chaining
        """
        if bonus < 0:
            raise ValueError(f"Бонус не может быть отрицательным: {bonus}")
        self._employee_type = "manager"
        self._bonus = bonus
        print(f"  [Builder] Тип: Manager, бонус: {bonus}")
        return self
    
    def as_developer(self, seniority: str = "junior", 
                    tech_stack: Optional[List[str]] = None) -> 'EmployeeBuilder':
        """
        Установить тип сотрудника как разработчик.
        
        Args:
            seniority: Уровень: junior/middle/senior
            tech_stack: Список технологий (Python, Java, Go и т.д.)
            
        Returns:
            self для chaining
        """
        valid_seniorities = {"junior", "middle", "senior"}
        if seniority not in valid_seniorities:
            raise ValueError(f"Неверный уровень: {seniority}. "
                           f"Допустимые: {valid_seniorities}")
        
        self._employee_type = "developer"
        self._seniority = seniority
        self._tech_stack = tech_stack if tech_stack else ["Python"]
        print(f"  [Builder] Тип: Developer, уровень: {seniority}, стек: {self._tech_stack}")
        return self
    
    def as_salesperson(self, commission_rate: float = 0.1) -> 'EmployeeBuilder':
        """
        Установить тип сотрудника как продавец.
        
        Args:
            commission_rate: Процент комиссии (0.0 - 1.0)
            
        Returns:
            self для chaining
        """
        if not (0.0 <= commission_rate <= 1.0):
            raise ValueError(f"Комиссия должна быть в диапазоне 0.0-1.0: {commission_rate}")
        
        self._employee_type = "salesperson"
        self._commission_rate = commission_rate
        print(f"  [Builder] Тип: Salesperson, комиссия: {commission_rate*100}%")
        return self
    
    def add_skill(self, skill: str) -> 'EmployeeBuilder':
        """
        Добавить технологию/навык (для разработчиков).
        
        Args:
            skill: Название технологии (Python, Java, JavaScript и т.д.)
            
        Returns:
            self для chaining
        """
        if skill not in self._tech_stack:
            self._tech_stack.append(skill)
            print(f"  [Builder] Добавлен навык: {skill}")
        return self
    
    def add_skills(self, skills: List[str]) -> 'EmployeeBuilder':
        """
        Добавить несколько технологий/навыков.
        
        Args:
            skills: Список технологий
            
        Returns:
            self для chaining
        """
        for skill in skills:
            self.add_skill(skill)
        return self
    
    def validate(self) -> None:
        """
        Проверка, что все обязательные поля заполнены.
        
        Raises:
            ValueError: Если какое-то обязательное поле не установлено
        """
        errors = []
        
        if self._id is None:
            errors.append("ID не установлен")
        if self._name is None:
            errors.append("Имя не установлено")
        if self._department is None:
            errors.append("Отдел не установлен")
        if self._base_salary is None:
            errors.append("Базовая зарплата не установлена")
        
        # Проверка специфических полей
        if self._employee_type == "manager" and self._bonus is None:
            errors.append("Бонус менеджера не установлен")
        elif self._employee_type == "developer" and self._seniority is None:
            errors.append("Уровень разработчика не установлен")
        elif self._employee_type == "salesperson" and self._commission_rate is None:
            errors.append("Комиссия продавца не установлена")
        
        if errors:
            raise ValueError("Ошибки валидации: " + ", ".join(errors))
    
    def build(self) -> dict:
        """
        Построить объект сотрудника после проверки всех данных.
        
        Returns:
            Словарь с полными данными сотрудника
            
        Raises:
            ValueError: Если данные неполные или невалидные
        """
        self.validate()
        
        print(f"\n[Builder] Построение сотрудника {self._employee_type}: {self._name}")
        
        # Базовый объект сотрудника
        employee_data = {
            'type': self._employee_type,
            'id': self._id,
            'name': self._name,
            'department': self._department,
            'base_salary': self._base_salary,
        }
        
        # Добавляем специфические поля
        if self._employee_type == "manager":
            employee_data['bonus'] = self._bonus
        elif self._employee_type == "developer":
            employee_data['seniority'] = self._seniority
            employee_data['tech_stack'] = self._tech_stack
        elif self._employee_type == "salesperson":
            employee_data['commission_rate'] = self._commission_rate
        
        print(f"[Builder] Готово! Построен объект: {employee_data}")
        return employee_data
    
    def reset(self) -> 'EmployeeBuilder':
        """
        Очистить builder для создания нового сотрудника.
        
        Returns:
            self для chaining
        """
        self.__init__()
        print("[Builder] Builder очищен для новой сборки")
        return self


class EmployeeDirector:
    """
    Директор для управления процессом построения сотрудников.
    Упрощает создание стандартных конфигураций.
    """
    
    def __init__(self, builder: EmployeeBuilder):
        """
        Инициализация директора с builder.
        
        Args:
            builder: Объект EmployeeBuilder для построения
        """
        self.builder = builder
    
    def build_junior_developer(self, emp_id: int, name: str, 
                              department: str = "DEV") -> dict:
        """
        Стандартная конфигурация для junior разработчика.
        
        Args:
            emp_id: ID сотрудника
            name: Имя сотрудника
            department: Отдел (по умолчанию DEV)
            
        Returns:
            Построенный объект сотрудника
        """
        print(f"\n[Director] Построение Junior Developer...")
        return (self.builder
                .reset()
                .set_id(emp_id)
                .set_name(name)
                .set_department(department)
                .set_base_salary(3000)  # Стандартная зарплата junior
                .as_developer("junior", ["Python", "Git"])
                .build())
    
    def build_senior_developer(self, emp_id: int, name: str,
                              department: str = "DEV",
                              tech_stack: Optional[List[str]] = None) -> dict:
        """
        Стандартная конфигурация для senior разработчика.
        
        Args:
            emp_id: ID сотрудника
            name: Имя сотрудника
            department: Отдел (по умолчанию DEV)
            tech_stack: Список технологий
            
        Returns:
            Построенный объект сотрудника
        """
        print(f"\n[Director] Построение Senior Developer...")
        if tech_stack is None:
            tech_stack = ["Python", "Java", "SQL", "Docker", "Kubernetes"]
        
        return (self.builder
                .reset()
                .set_id(emp_id)
                .set_name(name)
                .set_department(department)
                .set_base_salary(8000)  # Высокая зарплата для senior
                .as_developer("senior", tech_stack)
                .build())
    
    def build_sales_manager(self, emp_id: int, name: str,
                           department: str = "SALES") -> dict:
        """
        Стандартная конфигурация для менеджера по продажам.
        
        Args:
            emp_id: ID сотрудника
            name: Имя сотрудника
            department: Отдел (по умолчанию SALES)
            
        Returns:
            Построенный объект сотрудника
        """
        print(f"\n[Director] Построение Sales Manager...")
        return (self.builder
                .reset()
                .set_id(emp_id)
                .set_name(name)
                .set_department(department)
                .set_base_salary(4000)  # Базовая зарплата для менеджера
                .as_manager(bonus=2000)  # Высокий бонус за продажи
                .build())
    
    def build_sales_representative(self, emp_id: int, name: str,
                                  department: str = "SALES") -> dict:
        """
        Стандартная конфигурация для продавца.
        
        Args:
            emp_id: ID сотрудника
            name: Имя сотрудника
            department: Отдел (по умолчанию SALES)
            
        Returns:
            Построенный объект сотрудника
        """
        print(f"\n[Director] Построение Sales Representative...")
        return (self.builder
                .reset()
                .set_id(emp_id)
                .set_name(name)
                .set_department(department)
                .set_base_salary(2500)  # Базовая зарплата для продавца
                .as_salesperson(commission_rate=0.15)  # 15% комиссия
                .build())
