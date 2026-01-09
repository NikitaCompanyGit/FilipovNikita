from services.employee.base_validator import BaseValidator
from services.employee.salary_strategy import SenioritySalaryStrategy

class DeveloperValidator(BaseValidator):
    """
    Валидатор для разработчиков.

    Наследует BaseValidator и добавляет специфичные проверки
    для Developer (валидация уровня квалификации).

    SOLID:
    - SRP: Отвечает только за валидацию Developer
    - OCP: Расширяет BaseValidator без изменений базового класса
    - ISP: Предоставляет только нужные методы для Developer
    """

    @staticmethod
    def validate_seniority_level(value: str) -> str:
        """
        Проверяет корректность уровня квалификации разработчика.

        Использует список допустимых уровней из SenioritySalaryStrategy,
        обеспечивая единый источник истины (DRY).

        :param value: Уровень квалификации ('junior', 'middle', 'senior').
        :returns: Нормализованное значение (lowercase).
        :raises ValueError: Если уровень недопустим.
        """
        valid_levels = SenioritySalaryStrategy.get_valid_levels()

        return BaseValidator.validate_choice(
            value=value,
            field_name="Уровень квалификации (seniority_level)",
            valid_choices=valid_levels,
            case_sensitive=False
        )

    @staticmethod
    def validate_skill_name(skill: str) -> str:
        """
        Проверяет корректность названия навыка.

        :param skill: Название технологии/навыка.
        :returns: Очищенное название навыка.
        :raises ValueError: Если навык пустая строка.
        """
        return BaseValidator.validate_string_not_empty(
            value=skill,
            field_name="Название навыка"
        )