from typing import Dict, Any
from services.employee.sales_validator import SalesValidator

class SalesTracker:
    """
    Трекер продаж для продавца.

    Отвечает ТОЛЬКО за управление данными о продажах:
    - Общий объём продаж
    - Процент комиссии
    - История изменений (опционально)

    SOLID:
    - SRP: Отвечает только за управление данными продаж
    - Encapsulation: Скрывает внутреннюю структуру хранения
    """

    def __init__(self, initial_volume: float = 0.0, commission_rate: float = 0.0):
        """
        Инициализация трекера продаж.

        :param initial_volume: Начальный объём продаж (по умолчанию 0).
        :param commission_rate: Процент комиссии (например, 0.15 = 15%).
        """
        self._sales_volume = SalesValidator.validate_sales_volume(initial_volume)
        self._commission_rate = SalesValidator.validate_commission_rate(commission_rate)

    # --- Property для sales_volume ---

    @property
    def sales_volume(self) -> float:
        """Возвращает текущий объём продаж."""
        return self._sales_volume

    @sales_volume.setter
    def sales_volume(self, value: float):
        """
        Устанавливает объём продаж с валидацией.

        :param value: Новый объём продаж.
        :raises ValueError: Если значение невалидно.
        """
        self._sales_volume = SalesValidator.validate_sales_volume(value)

    # --- Property для commission_rate ---

    @property
    def commission_rate(self) -> float:
        """Возвращает текущий процент комиссии."""
        return self._commission_rate

    @commission_rate.setter
    def commission_rate(self, value: float):
        """
        Устанавливает процент комиссии с валидацией.

        :param value: Новый процент комиссии (0.0 - 1.0).
        :raises ValueError: Если значение невалидно.
        """
        self._commission_rate = SalesValidator.validate_commission_rate(value)

    # --- Методы управления продажами ---

    def add_sale(self, amount: float) -> None:
        """
        Добавляет новую продажу к общему объёму.

        :param amount: Сумма продажи.
        :raises ValueError: Если сумма невалидна.
        """
        validated_amount = SalesValidator.validate_sale_amount(amount)
        self._sales_volume += validated_amount

    def reset_sales(self) -> float:
        """
        Сбрасывает объём продаж (например, в начале нового периода).

        :returns: Предыдущий объём продаж перед сбросом.
        """
        old_volume = self._sales_volume
        self._sales_volume = 0.0
        return old_volume

    def calculate_commission(self) -> float:
        """
        Рассчитывает комиссию на основе текущих продаж.

        Формула: sales_volume × commission_rate

        :returns: Сумма комиссии.
        """
        return self._sales_volume * self._commission_rate

    def get_sales_stats(self) -> Dict[str, Any]:
        """
        Возвращает статистику продаж.

        :returns: Словарь с данными о продажах:
                 - volume: общий объём продаж
                 - rate: процент комиссии
                 - commission: рассчитанная комиссия
                 - rate_percent: процент комиссии в процентах
        """
        return {
            "volume": self._sales_volume,
            "rate": self._commission_rate,
            "commission": self.calculate_commission(),
            "rate_percent": f"{self._commission_rate * 100:.1f}%"
        }

    def set_commission_rate_percent(self, percent: float) -> None:
        """
        Устанавливает процент комиссии в процентах (для удобства).

        :param percent: Процент комиссии (например, 15 = 15%).
        :raises ValueError: Если процент вне диапазона [0, 100].
        """
        if not isinstance(percent, (int, float)):
            raise ValueError(
                f"Процент должен быть числом. Получено: {type(percent).__name__}"
            )

        if not (0 <= percent <= 100):
            raise ValueError(
                f"Процент комиссии должен быть в диапазоне [0, 100]. "
                f"Получено: {percent}"
            )

        self._commission_rate = percent / 100.0

    # --- Магические методы ---

    def __repr__(self):
        return (
            f"SalesTracker(volume={self._sales_volume:.2f}, "
            f"rate={self._commission_rate:.2%})"
        )