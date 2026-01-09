from datetime import datetime
from typing import Union, List
from base.abstract_employee import AbstractEmployee
from services.project_validator import ProjectValidator
from services.project_team_manager import ProjectTeamManager
from services.project_calculator import ProjectCalculator
from services.project_formatter import ProjectFormatter

class Project:
    """
    Класс Проекта.

    РЕФАКТОРИНГ:
    ✅ SRP: Класс отвечает ТОЛЬКО за управление данными проекта.
    ✅ Вся валидация делегирована в ProjectValidator.
    ✅ Управление командой делегировано в ProjectTeamManager.
    ✅ Все расчёты делегированы в ProjectCalculator.
    ✅ Форматирование вывода делегировано в ProjectFormatter.

    ДО рефакторинга: 150+ строк, 5 обязанностей
    ПОСЛЕ рефакторинга: ~70 строк, 1 обязанность (координация)
    """

    def __init__(
        self, 
        project_id: int, 
        name: str, 
        description: str, 
        deadline: Union[str, datetime], 
        status: str = "planning"
    ):
        """
        Инициализация проекта.

        :param project_id: Уникальный ID проекта.
        :param name: Название проекта.
        :param description: Описание проекта.
        :param deadline: Дедлайн в формате 'YYYY-MM-DD' или datetime.
        :param status: Статус проекта (по умолчанию 'planning').
        :raises ValueError: Если данные некорректны.
        """
        # Валидация всех полей
        self.id = ProjectValidator.validate_project_id(project_id)
        self.name = ProjectValidator.validate_project_name(name)
        self.description = description
        self.deadline = ProjectValidator.validate_deadline(deadline)

        # Инициализация сервисов
        self._team_manager = ProjectTeamManager()

        # Используем property setter для валидации статуса
        self.status = status

    # --- Property для статуса с валидацией ---

    @property
    def status(self) -> str:
        """Возвращает текущий статус проекта."""
        return self._status

    @status.setter
    def status(self, value: str):
        """
        Устанавливает статус с валидацией.
        Делегирует проверку в ProjectValidator.
        """
        self._status = ProjectValidator.validate_status(value)

    # --- Делегирование управления командой (ProjectTeamManager) ---

    def add_team_member(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника в команду проекта.
        Делегирует в ProjectTeamManager.
        """
        self._team_manager.add_member(employee)

    def remove_team_member(self, employee_id: int) -> None:
        """
        Удаляет сотрудника из команды по ID.
        Делегирует в ProjectTeamManager.
        """
        self._team_manager.remove_member(employee_id)

    def get_team(self) -> List[AbstractEmployee]:
        """
        Возвращает список участников команды.
        Делегирует в ProjectTeamManager.
        """
        return self._team_manager.get_team()

    def get_team_size(self) -> int:
        """
        Возвращает количество участников проекта.
        Делегирует в ProjectTeamManager.
        """
        return self._team_manager.get_team_size()

    # --- Делегирование расчётов (ProjectCalculator) ---

    def calculate_total_salary(self) -> float:
        """
        Рассчитывает бюджет зарплат проекта.
        Делегирует в ProjectCalculator.
        """
        return ProjectCalculator.calculate_total_salary(self._team_manager.get_team())

    def calculate_average_salary(self) -> float:
        """
        Рассчитывает среднюю зарплату в команде.
        Делегирует в ProjectCalculator.
        """
        return ProjectCalculator.calculate_average_salary(self._team_manager.get_team())

    # --- Делегирование форматирования (ProjectFormatter) ---

    def get_project_info(self) -> str:
        """
        Возвращает сводную информацию о проекте.
        Делегирует в ProjectFormatter.
        """
        return ProjectFormatter.format_project_info(
            self.name,
            self.id,
            self.status,
            self.deadline,
            self.get_team_size(),
            self.calculate_total_salary()
        )

    def get_team_info(self) -> str:
        """
        Возвращает информацию о команде проекта.
        Делегирует в ProjectFormatter.
        """
        return ProjectFormatter.format_team_list(self._team_manager.get_team())

    # --- Сериализация ---

    def to_dict(self) -> dict:
        """
        Сериализация проекта в словарь.

        ВАЖНО: Сохраняет список team_ids (ID сотрудников), а не полные объекты.
        Это позволяет избежать дублирования данных и циклических зависимостей.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "team_ids": self._team_manager.get_team_ids()
        }

    # --- Магические методы ---

    def __str__(self):
        return f"Project '{self.name}' [{self.status}]"

    def __repr__(self):
        return (
            f"Project(id={self.id}, name='{self.name}', "
            f"status='{self.status}', team_size={self.get_team_size()})"
        )