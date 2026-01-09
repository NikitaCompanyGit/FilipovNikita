from datetime import datetime
from typing import List
from base.abstract_employee import AbstractEmployee

class ProjectFormatter:
    """
    Форматтер для проектной информации.
    Отвечает ТОЛЬКО за форматирование вывода (SRP).
    """

    @staticmethod
    def format_project_info(
        name: str,
        project_id: int,
        status: str,
        deadline: datetime,
        team_size: int,
        budget: float
    ) -> str:
        """
        Возвращает сводную информацию о проекте.

        :returns: Форматированная строка с информацией.
        """
        return (
            f"Проект: {name} (ID: {project_id})\n"
            f"Статус: {status.upper()} | "
            f"Дедлайн: {deadline.strftime('%Y-%m-%d')}\n"
            f"Команда: {team_size} чел. | "
            f"Бюджет ФОТ: {budget:.2f} руб."
        )

    @staticmethod
    def format_team_list(team: List[AbstractEmployee]) -> str:
        """
        Форматирует список участников команды.

        :returns: Строка со списком сотрудников.
        """
        if not team:
            return "Команда пуста"

        lines = ["Участники команды:"]
        for i, emp in enumerate(team, 1):
            lines.append(f"  {i}. {emp.name} (ID: {emp.id}) - {emp.__class__.__name__}")

        return "\n".join(lines)