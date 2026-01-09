"""
МодульEmployee - РЕФАКТОРЕННАЯ ВЕРСИЯ

Класс отвечает ИСКЛЮЧИТЕЛЬНО за хранение и валидацию данных.
Валидация выделена в отдельный класс (SRP).
Использует Dependency Injection для валидатора (DIP).

Сравнение:
ДО:  Employee - класс + валидация + сообщения об ошибках (45 строк)
ПОСЛЕ: Employee - только данные (25 строк) + Validator - только валидация (40 строк)
"""

from typing import Optional
from validators import EmployeeValidator, ValidationError


class Employee:
    """
    Базовый класс-сущность (Entity). РЕФАКТОРЕННАЯ ВЕРСИЯ.
    
    Отвечает ИСКЛЮЧИТЕЛЬНО за хранение данных и их валидацию.
    Не содержит бизнес-логики или расчета зарплат.
    
    Валидация выделена в отдельный класс EmployeeValidator.
    """
    
    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        validator: Optional[EmployeeValidator] = None
    ) -> None:
        """
        Инициализирует нового сотрудника.
        
        Args:
            emp_id: Уникальный идентификатор
            name: Имя сотрудника
            department: Отдел
            base_salary: Базовый оклад
            validator: Объект валидатора (DIP)
        
        Raises:
            ValidationError: Если какие-то данные невалидны
        """
        self.validator = validator or EmployeeValidator()
        
        # Валидация при установке (через setter)
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary
    
    # ========== Properties с валидацией (через Validator) ==========
    
    @property
    def id(self) -> int:
        """Получить ID сотрудника."""
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        """Установить и валидировать ID.
        
        Args:
            value: Новое значение ID
        
        Raises:
            ValidationError: Если ID невалиден
        """
        self.__id = self.validator.validate_id(value)
    
    @property
    def name(self) -> str:
        """Получить имя сотрудника."""
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить и валидировать имя.
        
        Args:
            value: Новое значение имени
        
        Raises:
            ValidationError: Если имя невалидно
        """
        self.__name = self.validator.validate_name(value)
    
    @property
    def department(self) -> str:
        """Получить название отдела."""
        return self.__department
    
    @department.setter
    def department(self, value: str) -> None:
        """Установить и валидировать отдел.
        
        Args:
            value: Новое значение отдела
        
        Raises:
            ValidationError: Если отдел невалиден
        """
        self.__department = self.validator.validate_department(value)
    
    @property
    def base_salary(self) -> float:
        """Получить базовый оклад."""
        return self.__base_salary
    
    @base_salary.setter
    def base_salary(self, value: float) -> None:
        """Установить и валидировать базовый оклад.
        
        Args:
            value: Новое значение зарплаты
        
        Raises:
            ValidationError: Если зарплата невалидна
        """
        self.__base_salary = self.validator.validate_salary(value)
    
    def __str__(self) -> str:
        """Строковое представление сотрудника."""
        return (
            f"Сотрудник [id: {self.id}, имя: {self.name}, "
            f"отдел: {self.department}]"
        )
    
    def __repr__(self) -> str:
        """Подробное представление сотрудника."""
        return (
            f"Employee(emp_id={self.id}, name='{self.name}', "
            f"department='{self.department}', base_salary={self.base_salary})"
        )