from typing import List
from base.abstract_employee import AbstractEmployee

class ProjectTeamManager:
    """
    Менеджер команды проекта.
    Отвечает ТОЛЬКО за управление участниками (SRP).
    """

    def __init__(self):
        self._team: List[AbstractEmployee] = []

    def add_member(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника в команду проекта.
        Игнорирует добавление, если сотрудник уже в команде.
        """
        if not self.is_member(employee.id):
            self._team.append(employee)

    def remove_member(self, employee_id: int) -> None:
        """Удаляет сотрудника из команды по ID."""
        self._team = [e for e in self._team if e.id != employee_id]

    def get_team(self) -> List[AbstractEmployee]:
        """Возвращает список участников команды."""
        return self._team

    def get_team_size(self) -> int:
        """Возвращает количество участников проекта."""
        return len(self._team)

    def is_member(self, employee_id: int) -> bool:
        """Проверяет, является ли сотрудник участником команды."""
        return any(e.id == employee_id for e in self._team)

    def get_team_ids(self) -> List[int]:
        """Возвращает список ID сотрудников команды."""
        return [emp.id for emp in self._team]