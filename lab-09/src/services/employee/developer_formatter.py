from services.employee.base_formatter import BaseFormatter
from typing import Any

class DeveloperFormatter(BaseFormatter):
    """
    Форматтер для вывода информации о разработчиках.

    Наследует BaseFormatter и переопределяет метод _format_specific_info
    для добавления специфичной информации Developer.

    SOLID:
    - SRP: Отвечает только за форматирование вывода Developer
    - Template Method: Использует шаблон из BaseFormatter
    """

    def _format_specific_info(self, employee: Any) -> str:
        """
        Форматирует специфичную информацию о разработчике.

        Включает:
        - Тип сотрудника (Developer)
        - Уровень квалификации (Junior/Middle/Senior)
        - Стек технологий

        :param employee: Объект Developer.
        :returns: Форматированная строка.
        """
        seniority_display = employee.seniority_level.title()

        # Получаем список навыков через TechStackManager
        skills = employee.get_tech_stack()
        stack_str = ", ".join(skills) if skills else "Нет навыков"

        return (
            f" -> Тип: Developer ({seniority_display})\n"
            f" -> Стек: [{stack_str}]"
        )