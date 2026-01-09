from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseFormatter(ABC):
    """
    Базовый форматтер для вывода информации о сотрудниках.

    Использует Template Method Pattern для создания единой структуры
    вывода, позволяя подклассам кастомизировать конкретные детали.

    SOLID:
    - SRP: Отвечает только за форматирование вывода
    - OCP: Расширяется через наследование без изменений
    - Template Method: get_info() - шаблонный метод
    """

    def get_info(self, employee: Any) -> str:
        """
        Шаблонный метод для форматирования информации о сотруднике.

        Использует Template Method Pattern:
        1. Базовая информация (общая часть)
        2. Специфичная информация (переопределяется подклассами)
        3. Итоговая зарплата (общая часть)

        :param employee: Объект сотрудника.
        :returns: Форматированная строка.
        """
        base_info = self._format_base_info(employee)
        specific_info = self._format_specific_info(employee)
        salary_info = self._format_salary_info(employee)

        return f"{base_info}\n{specific_info}\n{salary_info}"

    def _format_base_info(self, employee: Any) -> str:
        """
        Форматирует базовую информацию (ID, имя, отдел).
        Общая для всех типов сотрудников.
        """
        return str(employee)  # Использует __str__() из AbstractEmployee

    @abstractmethod
    def _format_specific_info(self, employee: Any) -> str:
        """
        Форматирует специфичную информацию о сотруднике.

        ПЕРЕОПРЕДЕЛЯЕТСЯ в подклассах для каждого типа сотрудника:
        - Developer: уровень + стек технологий
        - Salesperson: продажи + комиссия
        - Manager: бонус

        :param employee: Объект сотрудника.
        :returns: Форматированная строка со специфичной информацией.
        """
        pass

    def _format_salary_info(self, employee: Any) -> str:
        """
        Форматирует информацию о зарплате.
        Общая для всех типов сотрудников.
        """
        salary = employee.calculate_salary()
        return f" -> Итоговая выплата: {salary:.2f} руб."

    @staticmethod
    def format_dict(data: Dict[str, Any], indent: int = 0) -> str:
        """
        Вспомогательный метод для форматирования словарей.

        :param data: Словарь для форматирования.
        :param indent: Уровень отступа.
        :returns: Форматированная строка.
        """
        lines = []
        prefix = "  " * indent

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(BaseFormatter.format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}: [{', '.join(map(str, value))}]")
            else:
                lines.append(f"{prefix}{key}: {value}")

        return "\n".join(lines)