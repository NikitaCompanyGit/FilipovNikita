from typing import Any, Union

class BaseValidator:
    """
    Базовый валидатор для общих проверок сотрудников.

    Предоставляет переиспользуемые методы валидации,
    которые используются всеми специализированными валидаторами.

    SOLID:
    - SRP: Отвечает только за валидацию данных
    - OCP: Легко расширяется через наследование
    - DRY: Устраняет дублирование валидационного кода
    """

    @staticmethod
    def validate_positive_number(
        value: Any, 
        field_name: str,
        allow_zero: bool = False
    ) -> float:
        """
        Проверяет, что значение является положительным числом.

        :param value: Значение для проверки.
        :param field_name: Название поля (для сообщения об ошибке).
        :param allow_zero: Разрешить ноль (по умолчанию False).
        :returns: Валидное число типа float.
        :raises ValueError: Если значение не число или отрицательное.
        """
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"{field_name} должен быть числом. "
                f"Получено: {type(value).__name__}"
            )

        min_value = 0 if allow_zero else 0.0
        comparison = ">=" if allow_zero else ">"

        if value < min_value or (not allow_zero and value == 0):
            raise ValueError(
                f"{field_name} должен быть {comparison} {min_value}. "
                f"Получено: {value}"
            )

        return float(value)

    @staticmethod
    def validate_range(
        value: Union[int, float],
        field_name: str,
        min_value: float,
        max_value: float,
        inclusive: bool = True
    ) -> float:
        """
        Проверяет, что значение находится в заданном диапазоне.

        :param value: Значение для проверки.
        :param field_name: Название поля.
        :param min_value: Минимальное значение.
        :param max_value: Максимальное значение.
        :param inclusive: Включать границы (по умолчанию True).
        :returns: Валидное число типа float.
        :raises ValueError: Если значение вне диапазона.
        """
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"{field_name} должен быть числом. "
                f"Получено: {type(value).__name__}"
            )

        if inclusive:
            if not (min_value <= value <= max_value):
                raise ValueError(
                    f"{field_name} должен быть в диапазоне "
                    f"[{min_value}, {max_value}]. Получено: {value}"
                )
        else:
            if not (min_value < value < max_value):
                raise ValueError(
                    f"{field_name} должен быть в диапазоне "
                    f"({min_value}, {max_value}). Получено: {value}"
                )

        return float(value)

    @staticmethod
    def validate_string_not_empty(value: Any, field_name: str) -> str:
        """
        Проверяет, что значение - непустая строка.

        :param value: Значение для проверки.
        :param field_name: Название поля.
        :returns: Очищенная строка (без пробелов по краям).
        :raises ValueError: Если не строка или пустая.
        """
        if not isinstance(value, str):
            raise ValueError(
                f"{field_name} должен быть строкой. "
                f"Получено: {type(value).__name__}"
            )

        stripped = value.strip()
        if not stripped:
            raise ValueError(f"{field_name} не может быть пустым.")

        return stripped

    @staticmethod
    def validate_choice(
        value: Any,
        field_name: str,
        valid_choices: set,
        case_sensitive: bool = False
    ) -> str:
        """
        Проверяет, что значение входит в список допустимых вариантов.

        :param value: Значение для проверки.
        :param field_name: Название поля.
        :param valid_choices: Множество допустимых значений.
        :param case_sensitive: Учитывать регистр (по умолчанию False).
        :returns: Нормализованное значение.
        :raises ValueError: Если значение не в списке допустимых.
        """
        if not isinstance(value, str):
            raise ValueError(
                f"{field_name} должен быть строкой. "
                f"Получено: {type(value).__name__}"
            )

        normalized = value if case_sensitive else value.lower().strip()
        comparison_set = valid_choices if case_sensitive else {
            choice.lower() for choice in valid_choices
        }

        if normalized not in comparison_set:
            raise ValueError(
                f"{field_name} должен быть одним из: {valid_choices}. "
                f"Получено: '{value}'"
            )

        return normalized