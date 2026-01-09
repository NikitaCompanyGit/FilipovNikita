from typing import Dict, Any
from base.abstract_employee import AbstractEmployee
from services.employee.salary_strategy import BaseSalaryStrategy
from services.employee.employee_serializer import EmployeeSerializer

class OrdinaryEmployee(AbstractEmployee):
    """
    Класс обычного сотрудника (без специализации).

    ОБНОВЛЕНИЕ:
    ✅ Интеграция с BaseSalaryStrategy для расчёта зарплаты.
    ✅ Интеграция с EmployeeSerializer для сериализации.
    ✅ Единообразный интерфейс со всеми специалистами.

    ПРИМЕЧАНИЕ:
    OrdinaryEmployee - базовый сотрудник без специфичных атрибутов.
    Не требует валидатора (валидация только базовых полей в AbstractEmployee).
    Не требует форматтера (использует get_info() из AbstractEmployee).

    ДО обновления: 20 строк, прямой расчёт зарплаты
    ПОСЛЕ обновления: 25 строк, использование Strategy Pattern
    """

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float
    ):
        """
        Инициализация обычного сотрудника.

        :param emp_id: Уникальный ID сотрудника.
        :param name: ФИО сотрудника.
        :param department: Отдел.
        :param base_salary: Базовый оклад.
        """
        super().__init__(emp_id, name, department, base_salary)

        # Инициализация стратегии расчёта зарплаты
        self._salary_strategy = BaseSalaryStrategy()

    # --- Делегирование расчёта зарплаты (BaseSalaryStrategy) ---

    def calculate_salary(self) -> float:
        """
        Рассчитывает зарплату (возвращает базовый оклад).
        Делегирует в BaseSalaryStrategy для единообразия.

        Формула: base_salary

        :returns: Базовая зарплата.
        """
        return self._salary_strategy.calculate(self)

    # --- Сериализация с использованием EmployeeSerializer ---

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует данные сотрудника в словарь.

        Использует EmployeeSerializer для базовых полей.
        OrdinaryEmployee не имеет дополнительных полей.

        :returns: Словарь с данными сотрудника.
        """
        data = EmployeeSerializer.serialize_base_fields(self)
        return EmployeeSerializer.add_employee_type(data, "employee")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrdinaryEmployee':
        """
        Создаёт объект OrdinaryEmployee из словаря.

        Используется фабрикой для десериализации.

        :param data: Словарь с данными сотрудника.
        :returns: Объект OrdinaryEmployee.
        """
        return cls(
            emp_id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"]
        )

    # --- Магические методы ---

    def __repr__(self):
        return (
            f"OrdinaryEmployee(id={self.id}, name='{self.name}', "
            f"department='{self.department}')"
        )