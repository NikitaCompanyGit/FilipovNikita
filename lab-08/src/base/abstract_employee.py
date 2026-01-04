"""
Модуль abstract_employee.py
===========================
Определяет абстрактный интерфейс сотрудника, являющийся контрактом для всех
специализированных ролей (менеджеров, разработчиков и т.д.).

Этот модуль связывает уровень данных (Employee) с бизнес-логикой,
обязывая наследников реализовать ключевые методы расчета зарплаты и сериализации.
"""

from abc import ABC, abstractmethod
from base.employee import Employee

class AbstractEmployee(Employee, ABC):
    """
    Абстрактный базовый класс сотрудника (Interface Layer).
    
    Наследуется от Employee (хранение данных) и ABC (абстракция).
    Определяет обязательный интерфейс, который должны реализовать все конкретные
    типы сотрудников, а также предоставляет общую реализацию магических методов
    для сравнения и арифметических операций.
    """
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """
        Рассчитывает итоговую зарплату сотрудника.
        
        Реализация зависит от конкретной роли (фикрованный оклад, бонусы,
        проценты с продаж, почасовая оплата и т.д.).
        
        :return: Итоговая сумма зарплаты (float).
        """
        pass

    @abstractmethod
    def get_info(self) -> str:
        """
        Возвращает форматированную строку с полной информацией о сотруднике.
        
        :return: Строка с описанием (имя, отдел, зарплата, спец. параметры).
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Сериализует объект сотрудника в словарь (для сохранения в JSON).
        
        :return: Словарь с данными сотрудника, включая поле 'type' для восстановления.
        """
        pass

    # --- Магические методы (Полиморфизм) ---

    def __eq__(self, other):
        """
        Проверяет равенство двух сотрудников.
        Сотрудники считаются равными, если у них совпадает уникальный ID.
        """
        if isinstance(other, AbstractEmployee):
            return self.id == other.id
        return False

    def __lt__(self, other):
        """
        Определяет порядок сортировки сотрудников (меньше чем).
        Сравнение производится по размеру итоговой зарплаты.
        Позволяет использовать sorted() и list.sort().
        """
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() < other.calculate_salary()
        return NotImplemented

    def __add__(self, other):
        """
        Позволяет складывать сотрудника с другим сотрудником или числом.
        
        1. Employee + Employee -> Сумма их зарплат (float).
        2. Employee + int/float -> Зарплата + число (float).
        """
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() + other.calculate_salary()
        elif isinstance(other, (int, float)):
            return self.calculate_salary() + other
        return NotImplemented

    def __radd__(self, other):
        """
        Поддержка правостороннего сложения (int + Employee).
        Необходима для корректной работы встроенной функции sum(), 
        которая начинает суммирование с 0.
        """
        if isinstance(other, (int, float)):
            return other + self.calculate_salary()
        return NotImplemented
