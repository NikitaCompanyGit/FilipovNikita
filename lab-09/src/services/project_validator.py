from datetime import datetime
from typing import Union
from base.exceptions import InvalidStatusError

class ProjectValidator:
    """
    Валидатор для проектов.
    Отвечает ТОЛЬКО за валидацию данных проекта (SRP).
    """

    VALID_STATUSES = {"planning", "active", "completed", "cancelled"}

    @staticmethod
    def validate_status(status: str) -> str:
        """
        Проверяет корректность статуса проекта.

        :param status: Статус для проверки.
        :returns: Нормализованный статус (lowercase).
        :raises InvalidStatusError: Если статус недопустим.
        """
        normalized = status.lower().strip()
        if normalized not in ProjectValidator.VALID_STATUSES:
            raise InvalidStatusError(
                f"Статус '{status}' недопустим. "
                f"Разрешены: {ProjectValidator.VALID_STATUSES}"
            )
        return normalized

    @staticmethod
    def validate_deadline(deadline: Union[str, datetime]) -> datetime:
        """
        Проверяет и преобразует дату дедлайна.

        :param deadline: Дата в формате строки 'YYYY-MM-DD' или datetime.
        :returns: Объект datetime.
        :raises ValueError: Если формат даты неверен.
        """
        if isinstance(deadline, datetime):
            return deadline

        if isinstance(deadline, str):
            try:
                return datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"Неверный формат даты '{deadline}'. "
                    f"Ожидается 'YYYY-MM-DD'."
                )

        raise TypeError(
            f"deadline должен быть строкой или datetime, "
            f"получен: {type(deadline).__name__}"
        )

    @staticmethod
    def validate_project_id(project_id: int) -> int:
        """
        Проверяет корректность ID проекта.

        :raises ValueError: Если ID некорректен.
        """
        if not isinstance(project_id, int) or project_id <= 0:
            raise ValueError(
                f"ID проекта должен быть положительным целым числом. "
                f"Получено: {project_id}"
            )
        return project_id

    @staticmethod
    def validate_project_name(name: str) -> str:
        """
        Проверяет корректность названия проекта.

        :raises ValueError: Если название пустое.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название проекта не может быть пустым.")
        return name.strip()