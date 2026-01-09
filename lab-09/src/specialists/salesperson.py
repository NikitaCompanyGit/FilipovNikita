from typing import Dict, Any
from base.abstract_employee import AbstractEmployee
from services.employee.sales_tracker import SalesTracker
from services.employee.salary_strategy import CommissionSalaryStrategy
from services.employee.salesperson_formatter import SalespersonFormatter
from services.employee.employee_serializer import EmployeeSerializer

class Salesperson(AbstractEmployee):
    """
    Класс Продавца.

    РЕФАКТОРИНГ:
    ✅ SRP: Класс отвечает ТОЛЬКО за управление данными продавца.
    ✅ Валидация делегирована в SalesValidator (через SalesTracker).
    ✅ Управление продажами делегировано в SalesTracker.
    ✅ Расчёт зарплаты делегирован в CommissionSalaryStrategy.
    ✅ Форматирование делегировано в SalespersonFormatter.
    ✅ Сериализация использует EmployeeSerializer.

    ДО рефакторинга: 100 строк, 5 обязанностей
    ПОСЛЕ рефакторинга: ~50 строк, 1 обязанность (координация)
    """

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        sales_volume: float = 0.0,
        commission_rate: float = 0.0
    ):
        """
        Инициализация продавца.

        :param emp_id: Уникальный ID сотрудника.
        :param name: ФИО продавца.
        :param department: Отдел.
        :param base_salary: Базовый оклад.
        :param sales_volume: Объём продаж (по умолчанию 0).
        :param commission_rate: Процент комиссии (например, 0.15 = 15%).
        """
        super().__init__(emp_id, name, department, base_salary)

        # Инициализация трекера продаж
        self._sales_tracker = SalesTracker(sales_volume, commission_rate)

        # Инициализация стратегии расчёта зарплаты
        self._salary_strategy = CommissionSalaryStrategy()

        # Инициализация форматтера
        self._formatter = SalespersonFormatter()

    # --- Делегирование управления продажами (SalesTracker) ---

    @property
    def sales_volume(self) -> float:
        """
        Возвращает текущий объём продаж.
        Делегирует в SalesTracker.
        """
        return self._sales_tracker.sales_volume

    @sales_volume.setter
    def sales_volume(self, value: float):
        """
        Устанавливает объём продаж с валидацией.
        Делегирует в SalesTracker.
        """
        self._sales_tracker.sales_volume = value

    @property
    def commission_rate(self) -> float:
        """
        Возвращает текущий процент комиссии.
        Делегирует в SalesTracker.
        """
        return self._sales_tracker.commission_rate

    @commission_rate.setter
    def commission_rate(self, value: float):
        """
        Устанавливает процент комиссии с валидацией.
        Делегирует в SalesTracker.
        """
        self._sales_tracker.commission_rate = value

    def add_sale(self, amount: float) -> None:
        """
        Добавляет новую продажу к общему объёму.
        Делегирует в SalesTracker.

        :param amount: Сумма продажи.
        """
        self._sales_tracker.add_sale(amount)

    def reset_sales(self) -> float:
        """
        Сбрасывает объём продаж.
        Делегирует в SalesTracker.

        :returns: Предыдущий объём продаж.
        """
        return self._sales_tracker.reset_sales()

    def get_sales_stats(self) -> Dict[str, Any]:
        """
        Возвращает статистику продаж.
        Делегирует в SalesTracker.

        :returns: Словарь с данными о продажах.
        """
        return self._sales_tracker.get_sales_stats()

    def set_commission_rate_percent(self, percent: float) -> None:
        """
        Устанавливает процент комиссии в процентах.
        Делегирует в SalesTracker.

        :param percent: Процент комиссии (например, 15 = 15%).
        """
        self._sales_tracker.set_commission_rate_percent(percent)

    # --- Делегирование расчёта зарплаты (CommissionSalaryStrategy) ---

    def calculate_salary(self) -> float:
        """
        Рассчитывает зарплату с учётом комиссии от продаж.
        Делегирует в CommissionSalaryStrategy.

        Формула: base_salary + (sales_volume × commission_rate)

        :returns: Общая зарплата.
        """
        return self._salary_strategy.calculate(self)

    # --- Делегирование форматирования (SalespersonFormatter) ---

    def get_info(self) -> str:
        """
        Возвращает детальную информацию о продавце.
        Делегирует в SalespersonFormatter.

        :returns: Форматированная строка.
        """
        return self._formatter.get_info(self)

    # --- Сериализация с использованием EmployeeSerializer ---

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует данные продавца в словарь.

        Использует EmployeeSerializer для базовых полей
        и добавляет специфичные поля Salesperson.

        :returns: Словарь с данными продавца.
        """
        data = EmployeeSerializer.serialize_base_fields(self)
        data.update({
            "sales_volume": self.sales_volume,
            "commission_rate": self.commission_rate
        })
        return EmployeeSerializer.add_employee_type(data, "salesperson")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Salesperson':
        """
        Создаёт объект Salesperson из словаря.

        Используется фабрикой для десериализации.

        :param data: Словарь с данными продавца.
        :returns: Объект Salesperson.
        """
        return cls(
            emp_id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            sales_volume=data.get("sales_volume", 0.0),
            commission_rate=data.get("commission_rate", 0.0)
        )

    # --- Магические методы ---

    def __repr__(self):
        return (
            f"Salesperson(id={self.id}, name='{self.name}', "
            f"sales={self.sales_volume:.2f}, "
            f"rate={self.commission_rate:.2%})"
        )