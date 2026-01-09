from typing import List, Dict, Any
from base.abstract_employee import AbstractEmployee
from services.employee.developer_validator import DeveloperValidator
from services.employee.tech_stack_manager import TechStackManager
from services.employee.salary_strategy import SenioritySalaryStrategy
from services.employee.developer_formatter import DeveloperFormatter
from services.employee.employee_serializer import EmployeeSerializer

class Developer(AbstractEmployee):
    """
    Класс Разработчика.

    РЕФАКТОРИНГ:
    ✅ SRP: Класс отвечает ТОЛЬКО за управление данными разработчика.
    ✅ Валидация делегирована в DeveloperValidator.
    ✅ Управление навыками делегировано в TechStackManager.
    ✅ Расчёт зарплаты делегирован в SenioritySalaryStrategy.
    ✅ Форматирование делегировано в DeveloperFormatter.
    ✅ Сериализация использует EmployeeSerializer.

    ДО рефакторинга: 110 строк, 5 обязанностей
    ПОСЛЕ рефакторинга: ~60 строк, 1 обязанность (координация)
    """

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        seniority_level: str,
        tech_stack: List[str] = None
    ):
        """
        Инициализация разработчика.

        :param emp_id: Уникальный ID сотрудника.
        :param name: ФИО разработчика.
        :param department: Отдел.
        :param base_salary: Базовый оклад.
        :param seniority_level: Уровень ('junior', 'middle', 'senior').
        :param tech_stack: Список технологий (необязательно).
        """
        super().__init__(emp_id, name, department, base_salary)

        # Валидация и установка уровня квалификации
        self.seniority_level = seniority_level

        # Инициализация менеджера стека технологий
        self._tech_stack_manager = TechStackManager(tech_stack)

        # Инициализация стратегии расчёта зарплаты
        self._salary_strategy = SenioritySalaryStrategy()

        # Инициализация форматтера
        self._formatter = DeveloperFormatter()

    # --- Property для seniority_level с валидацией ---

    @property
    def seniority_level(self) -> str:
        """Возвращает уровень квалификации разработчика."""
        return self._seniority_level

    @seniority_level.setter
    def seniority_level(self, value: str):
        """
        Устанавливает уровень квалификации с валидацией.
        Делегирует проверку в DeveloperValidator.
        """
        self._seniority_level = DeveloperValidator.validate_seniority_level(value)

    # --- Делегирование управления навыками (TechStackManager) ---

    def add_skill(self, skill: str) -> None:
        """
        Добавляет новый навык в стек технологий.
        Делегирует в TechStackManager.

        :param skill: Название технологии.
        """
        self._tech_stack_manager.add_skill(skill)

    def remove_skill(self, skill: str) -> bool:
        """
        Удаляет навык из стека.
        Делегирует в TechStackManager.

        :param skill: Название технологии.
        :returns: True, если навык был удалён.
        """
        return self._tech_stack_manager.remove_skill(skill)

    def get_tech_stack(self) -> List[str]:
        """
        Возвращает список всех навыков.
        Делегирует в TechStackManager.

        :returns: Список навыков.
        """
        return self._tech_stack_manager.get_skills()

    def has_skill(self, skill: str) -> bool:
        """
        Проверяет наличие навыка.
        Делегирует в TechStackManager.

        :param skill: Название технологии.
        :returns: True, если навык присутствует.
        """
        return self._tech_stack_manager.has_skill(skill)

    # --- Делегирование расчёта зарплаты (SenioritySalaryStrategy) ---

    def calculate_salary(self) -> float:
        """
        Рассчитывает зарплату с учётом уровня квалификации.
        Делегирует в SenioritySalaryStrategy.

        :returns: Зарплата = base_salary * multiplier.
        """
        return self._salary_strategy.calculate(self)

    # --- Делегирование форматирования (DeveloperFormatter) ---

    def get_info(self) -> str:
        """
        Возвращает детальную информацию о разработчике.
        Делегирует в DeveloperFormatter.

        :returns: Форматированная строка.
        """
        return self._formatter.get_info(self)

    # --- Сериализация с использованием EmployeeSerializer ---

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует данные разработчика в словарь.

        Использует EmployeeSerializer для базовых полей
        и добавляет специфичные поля Developer.

        :returns: Словарь с данными разработчика.
        """
        data = EmployeeSerializer.serialize_base_fields(self)
        data.update({
            "seniority": self.seniority_level,
            "tech_stack": self._tech_stack_manager.get_skills()
        })
        return EmployeeSerializer.add_employee_type(data, "developer")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Developer':
        """
        Создаёт объект Developer из словаря.

        Используется фабрикой для десериализации.

        :param data: Словарь с данными разработчика.
        :returns: Объект Developer.
        """
        tech_stack = EmployeeSerializer.deserialize_list_field(data, "tech_stack")

        return cls(
            emp_id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            seniority_level=data["seniority"],
            tech_stack=tech_stack
        )

    # --- Поддержка итератора (для обратной совместимости) ---

    def __iter__(self):
        """
        Позволяет перебирать стек технологий: for skill in developer.
        Делегирует в TechStackManager.
        """
        return iter(self._tech_stack_manager)

    # --- Магические методы ---

    def __repr__(self):
        return (
            f"Developer(id={self.id}, name='{self.name}', "
            f"seniority='{self.seniority_level}', "
            f"skills={len(self._tech_stack_manager)})"
        )