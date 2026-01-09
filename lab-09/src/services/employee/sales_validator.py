from services.employee.base_validator import BaseValidator

class SalesValidator(BaseValidator):
    """
    Валидатор для продавцов.

    Наследует BaseValidator и добавляет специфичные проверки
    для Salesperson (валидация объёма продаж и процента комиссии).

    SOLID:
    - SRP: Отвечает только за валидацию Salesperson
    - OCP: Расширяет BaseValidator без изменений базового класса
    - ISP: Предоставляет только нужные методы для Salesperson
    """

    # Константы для валидации
    MIN_COMMISSION_RATE = 0.0
    MAX_COMMISSION_RATE = 1.0  # 100%

    @staticmethod
    def validate_sales_volume(value: float) -> float:
        """
        Проверяет корректность объёма продаж.

        Объём продаж должен быть неотрицательным числом.

        :param value: Объём продаж.
        :returns: Валидное значение типа float.
        :raises ValueError: Если объём продаж отрицательный.
        """
        return BaseValidator.validate_positive_number(
            value=value,
            field_name="Объём продаж (sales_volume)",
            allow_zero=True  # Разрешаем 0 (новый продавец)
        )

    @staticmethod
    def validate_commission_rate(value: float) -> float:
        """
        Проверяет корректность процента комиссии.

        Комиссия должна быть в диапазоне [0.0, 1.0] (0% - 100%).

        :param value: Процент комиссии (например, 0.15 = 15%).
        :returns: Валидное значение типа float.
        :raises ValueError: Если комиссия вне диапазона.
        """
        return BaseValidator.validate_range(
            value=value,
            field_name="Процент комиссии (commission_rate)",
            min_value=SalesValidator.MIN_COMMISSION_RATE,
            max_value=SalesValidator.MAX_COMMISSION_RATE,
            inclusive=True
        )

    @staticmethod
    def validate_sale_amount(amount: float) -> float:
        """
        Проверяет корректность суммы отдельной продажи.

        :param amount: Сумма продажи.
        :returns: Валидное значение типа float.
        :raises ValueError: Если сумма неположительная.
        """
        return BaseValidator.validate_positive_number(
            value=amount,
            field_name="Сумма продажи",
            allow_zero=False  # Продажа не может быть нулевой
        )