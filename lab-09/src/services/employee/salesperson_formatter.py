from services.employee.base_formatter import BaseFormatter
from typing import Any

class SalespersonFormatter(BaseFormatter):
    """
    Форматтер для вывода информации о продавцах.

    Наследует BaseFormatter и переопределяет метод _format_specific_info
    для добавления специфичной информации Salesperson.

    SOLID:
    - SRP: Отвечает только за форматирование вывода Salesperson
    - Template Method: Использует шаблон из BaseFormatter
    """

    def _format_specific_info(self, employee: Any) -> str:
        """
        Форматирует специфичную информацию о продавце.

        Включает:
        - Тип сотрудника (Salesperson)
        - Объём продаж
        - Процент комиссии
        - Рассчитанная комиссия

        :param employee: Объект Salesperson.
        :returns: Форматированная строка.
        """
        # Получаем статистику продаж через SalesTracker
        stats = employee.get_sales_stats()

        return (
            f" -> Тип: Salesperson\n"
            f" -> Продажи: {stats['volume']:.2f} руб.\n"
            f" -> Комиссия: {stats['rate_percent']} "
            f"({stats['commission']:.2f} руб.)"
        )