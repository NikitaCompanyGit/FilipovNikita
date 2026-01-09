from abc import ABC, abstractmethod
from typing import Any

class SalaryCalculationStrategy(ABC):
    """
    Абстрактная стратегия для расчёта зарплаты.

    Использует Strategy Pattern для инкапсуляции различных алгоритмов
    расчёта зарплаты, делая их взаимозаменяемыми.

    SOLID:
    - SRP: Отвечает только за расчёт зарплаты
    - OCP: Новые стратегии добавляются без изменения существующих
    - LSP: Все стратегии взаимозаменяемы
    - ISP: Минимальный интерфейс (только calculate)
    """

    @abstractmethod
    def calculate(self, employee: Any) -> float:
        """
        Рассчитывает зарплату для сотрудника.

        :param employee: Объект сотрудника.
        :returns: Рассчитанная зарплата.
        """
        pass


class BaseSalaryStrategy(SalaryCalculationStrategy):
    """
    Базовая стратегия расчёта зарплаты.

    Возвращает базовый оклад без дополнительных начислений.
    Используется для OrdinaryEmployee.
    """

    def calculate(self, employee: Any) -> float:
        """
        Возвращает базовый оклад сотрудника.

        :param employee: Объект сотрудника с атрибутом base_salary.
        :returns: Базовая зарплата.
        """
        return employee.base_salary


class BonusSalaryStrategy(SalaryCalculationStrategy):
    """
    Стратегия расчёта зарплаты с фиксированным бонусом.

    Формула: Оклад + Бонус
    Используется для Manager.
    """

    def calculate(self, employee: Any) -> float:
        """
        Рассчитывает зарплату как сумму оклада и бонуса.

        :param employee: Объект менеджера с атрибутами base_salary и bonus.
        :returns: Зарплата = base_salary + bonus.
        """
        return employee.base_salary + employee.bonus


class CommissionSalaryStrategy(SalaryCalculationStrategy):
    """
    Стратегия расчёта зарплаты с комиссией от продаж.

    Формула: Оклад + (Объем продаж × Процент комиссии)
    Используется для Salesperson.
    """

    def calculate(self, employee: Any) -> float:
        """
        Рассчитывает зарплату с учётом комиссии от продаж.

        :param employee: Объект продавца с атрибутами:
                        - base_salary
                        - sales_volume
                        - commission_rate
        :returns: Зарплата = base_salary + (sales_volume * commission_rate).
        """
        commission = employee.sales_volume * employee.commission_rate
        return employee.base_salary + commission


class SenioritySalaryStrategy(SalaryCalculationStrategy):
    """
    Стратегия расчёта зарплаты с множителем по уровню квалификации.

    Формула: Оклад × Коэффициент уровня
    Используется для Developer.
    """

    # Коэффициенты по уровням квалификации
    LEVEL_MULTIPLIERS = {
        "junior": 1.0,
        "middle": 1.5,
        "senior": 2.0
    }

    def calculate(self, employee: Any) -> float:
        """
        Рассчитывает зарплату с учётом уровня квалификации.

        :param employee: Объект разработчика с атрибутами:
                        - base_salary
                        - seniority_level
        :returns: Зарплата = base_salary * multiplier.
        """
        multiplier = self.LEVEL_MULTIPLIERS.get(
            employee.seniority_level, 
            1.0
        )
        return employee.base_salary * multiplier

    @classmethod
    def get_valid_levels(cls) -> set:
        """
        Возвращает множество допустимых уровней квалификации.

        :returns: Множество строк с уровнями ('junior', 'middle', 'senior').
        """
        return set(cls.LEVEL_MULTIPLIERS.keys())