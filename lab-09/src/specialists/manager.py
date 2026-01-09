from typing import Dict, Any
from base.abstract_employee import AbstractEmployee
from services.employee.manager_validator import ManagerValidator
from services.employee.salary_strategy import BonusSalaryStrategy
from services.employee.manager_formatter import ManagerFormatter
from services.employee.employee_serializer import EmployeeSerializer

class Manager(AbstractEmployee):
    """
    Класс Менеджера.

    РЕФАКТОРИНГ:
    ✅ SRP: Класс отвечает ТОЛЬКО за управление данными менеджера.
    ✅ Валидация делегирована в ManagerValidator.
    ✅ Расчёт зарплаты делегирован в BonusSalaryStrategy.
    ✅ Форматирование делегировано в ManagerFormatter.
    ✅ Сериализация использует EmployeeSerializer.

    ДО рефакторинга: 60 строк, 4 обязанности
    ПОСЛЕ рефакторинга: ~35 строк, 1 обязанность (координация)

    ПРИМЕЧАНИЕ:
    Manager - самый простой специалист, имеет только один специфичный
    атрибут (bonus), поэтому не требует отдельного менеджера данных
    (как TechStackManager или SalesTracker).
    """

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        bonus: float = 0.0
    ):
        """
        Инициализация менеджера.

        :param emp_id: Уникальный ID сотрудника.
        :param name: ФИО менеджера.
        :param department: Отдел.
        :param base_salary: Базовый оклад.
        :param bonus: Размер бонуса (по умолчанию 0).
        """
        super().__init__(emp_id, name, department, base_salary)

        # Валидация и установка бонуса
        self.bonus = bonus

        # Инициализация стратегии расчёта зарплаты
        self._salary_strategy = BonusSalaryStrategy()

        # Инициализация форматтера
        self._formatter = ManagerFormatter()

    # --- Property для bonus с валидацией ---

    @property
    def bonus(self) -> float:
        """Возвращает размер бонуса менеджера."""
        return self._bonus

    @bonus.setter
    def bonus(self, value: float):
        """
        Устанавливает размер бонуса с валидацией.
        Делегирует проверку в ManagerValidator.

        :param value: Размер бонуса.
        :raises ValueError: Если бонус невалиден.
        """
        self._bonus = ManagerValidator.validate_bonus(value)

    # --- Делегирование расчёта зарплаты (BonusSalaryStrategy) ---

    def calculate_salary(self) -> float:
        """
        Рассчитывает зарплату с учётом бонуса.
        Делегирует в BonusSalaryStrategy.

        Формула: base_salary + bonus

        :returns: Общая зарплата.
        """
        return self._salary_strategy.calculate(self)

    # --- Делегирование форматирования (ManagerFormatter) ---

    def get_info(self) -> str:
        """
        Возвращает детальную информацию о менеджере.
        Делегирует в ManagerFormatter.

        :returns: Форматированная строка.
        """
        return self._formatter.get_info(self)

    # --- Сериализация с использованием EmployeeSerializer ---

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует данные менеджера в словарь.

        Использует EmployeeSerializer для базовых полей
        и добавляет специфичное поле Manager.

        :returns: Словарь с данными менеджера.
        """
        data = EmployeeSerializer.serialize_base_fields(self)
        data["bonus"] = self.bonus
        return EmployeeSerializer.add_employee_type(data, "manager")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Manager':
        """
        Создаёт объект Manager из словаря.

        Используется фабрикой для десериализации.

        :param data: Словарь с данными менеджера.
        :returns: Объект Manager.
        """
        return cls(
            emp_id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            bonus=data.get("bonus", 0.0)
        )

    # --- Магические методы ---

    def __repr__(self):
        return (
            f"Manager(id={self.id}, name='{self.name}', "
            f"bonus={self.bonus:.2f})"
        )