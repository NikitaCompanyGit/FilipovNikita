from datetime import datetime
from typing import List, Optional
from base.abstract_employee import AbstractEmployee
from base.exceptions import InvalidStatusError, DuplicateIdError

class Project:
    """
    Класс Проекта.
    
    Реализует паттерн Композиция (с нюансом): проект содержит команду (Team),
    состоящую из сотрудников. 
    
    Особенности:
    - Жесткая валидация статусов (planning, active, completed, cancelled).
    - При сериализации сохраняет ТОЛЬКО ID сотрудников, чтобы избежать
      дублирования данных при сохранении всей компании (Reference storage).
    """
    
    VALID_STATUSES = {"planning", "active", "completed", "cancelled"}

    def __init__(self, project_id: int, name: str, description: str, deadline: str, status: str = "planning"):
        """
        Инициализация проекта.
        
        :param deadline: Дата дедлайна в формате строки 'YYYY-MM-DD'.
        :raises ValueError: Если формат даты неверен.
        """
        self.id = project_id
        self.name = name
        self.description = description
        
        try:
            if isinstance(deadline, str):
                self.deadline = datetime.strptime(deadline, "%Y-%m-%d")
            else:
                self.deadline = deadline
        except ValueError:
            raise ValueError("Формат даты должен быть YYYY-MM-DD")

        # Используем сеттер для валидации статуса
        self.status = status 
        self.__team: List[AbstractEmployee] = []

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str):
        """Устанавливает статус с проверкой на допустимые значения."""
        normalized = value.lower().strip()
        if normalized not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Статус '{value}' недопустим. Разрешены: {self.VALID_STATUSES}")
        self.__status = normalized

    def add_team_member(self, employee: AbstractEmployee) -> None:
        """
        Добавляет сотрудника в команду проекта.
        Игнорирует добавление, если сотрудник уже в команде.
        """
        if any(e.id == employee.id for e in self.__team):
            return 
        self.__team.append(employee)

    def remove_team_member(self, employee_id: int) -> None:
        """Удаляет сотрудника из команды по ID."""
        self.__team = [e for e in self.__team if e.id != employee_id]

    def get_team(self) -> List[AbstractEmployee]:
        """Возвращает список участников команды."""
        return self.__team

    def get_team_size(self) -> int:
        """Возвращает количество участников проекта."""
        return len(self.__team)

    def calculate_total_salary(self) -> float:
        """Рассчитывает бюджет зарплат (суммарный оклад всех участников)."""
        return sum(emp.calculate_salary() for emp in self.__team)

    def get_project_info(self) -> str:
        """Возвращает сводную информацию о проекте."""
        return (f"Проект: {self.name} (ID: {self.id})\n"
                f"Статус: {self.status.upper()} | Дедлайн: {self.deadline.strftime('%Y-%m-%d')}\n"
                f"Команда: {len(self.__team)} чел. | Бюджет ФОТ: {self.calculate_total_salary()} руб.")

    def to_dict(self) -> dict:
        """
        Сериализация проекта в словарь.
        
        ВАЖНО: Сохраняет список team_ids (ID сотрудников), а не полные объекты.
        Это позволяет избежать дублирования данных и циклических зависимостей
        при сохранении всей структуры компании.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "team_ids": [emp.id for emp in self.__team] # Храним только ссылки
        }

    def __str__(self):
        return f"Project '{self.name}' [{self.status}]"
