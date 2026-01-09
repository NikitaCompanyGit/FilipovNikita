from services.employee.base_formatter import BaseFormatter
from typing import Any

class ManagerFormatter(BaseFormatter):
    """
    Форматтер для вывода информации о менеджерах.

    Наследует BaseFormatter и переопределяет метод _format_specific_info
    для добавления специфичной информации Manager.

    SOLID:
    - SRP: Отвечает только за форматирование вывода Manager
    - Template Method: Использует шаблон из BaseFormatter
    """

    def _format_specific_info(self, employee: Any) -> str:
        """
        Форматирует специфичную информацию о менеджере.

        Включает:
        - Тип сотрудника (Manager)
        - Размер бонуса

        :param employee: Объект Manager.
        :returns: Форматированная строка.
        """
        return (
            f" -> Тип: Manager\n"
            f" -> Бонус: {employee.bonus:.2f} руб."
        )