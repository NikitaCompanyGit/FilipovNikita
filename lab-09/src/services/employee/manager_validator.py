from services.employee.base_validator import BaseValidator

class ManagerValidator(BaseValidator):
    """
    Валидатор для менеджеров.

    Наследует BaseValidator и добавляет специфичные проверки
    для Manager (валидация бонуса).

    SOLID:
    - SRP: Отвечает только за валидацию Manager
    - OCP: Расширяет BaseValidator без изменений базового класса
    - ISP: Предоставляет только нужные методы для Manager
    """

    @staticmethod
    def validate_bonus(value: float) -> float:
        """
        Проверяет корректность бонуса менеджера.

        Бонус должен быть неотрицательным числом.

        :param value: Размер бонуса.
        :returns: Валидное значение типа float.
        :raises ValueError: Если бонус отрицательный.
        """
        return BaseValidator.validate_positive_number(
            value=value,
            field_name="Бонус менеджера (bonus)",
            allow_zero=True  # Разрешаем 0 (менеджер без бонуса в периоде)
        )