from typing import List, Optional
from organization.project import Project
from base.exceptions import DuplicateIdError

class ProjectManager:
    """
    Менеджер для управления проектами компании.
    Отвечает ТОЛЬКО за операции с проектами (SRP).
    """

    def __init__(self):
        self.__projects: List[Project] = []

    def add_project(self, project: Project) -> None:
        """
        Добавляет проект, проверяя уникальность ID.

        :raises DuplicateIdError: Если проект с таким ID уже существует.
        """
        if any(p.id == project.id for p in self.__projects):
            raise DuplicateIdError(f"Проект с ID {project.id} уже существует.")
        self.__projects.append(project)

    def get_projects(self) -> List[Project]:
        """Возвращает список всех проектов."""
        return self.__projects

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Находит проект по ID.

        :returns: Проект или None, если не найден.
        """
        return next((p for p in self.__projects if p.id == project_id), None)

    def remove_project(self, project_id: int) -> None:
        """
        Удаляет проект по ID.

        :raises ValueError: Если проект не найден.
        """
        project = self.get_project_by_id(project_id)
        if not project:
            raise ValueError(f"Проект с ID {project_id} не найден.")
        self.__projects.remove(project)