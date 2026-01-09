from typing import Dict, List
from base.abstract_employee import AbstractEmployee
from organization.department import Department
from organization.project import Project

class LinkResolver:
    """
    Сервис для восстановления связей между объектами при десериализации.
    Отвечает ТОЛЬКО за восстановление ссылок (SRP).
    """

    @staticmethod
    def build_employee_map(departments: List[Department]) -> Dict[int, AbstractEmployee]:
        """
        Создаёт карту {employee_id: employee_object} из всех отделов.

        :returns: Словарь для быстрого поиска сотрудников по ID.
        """
        employee_map = {}
        for dept in departments:
            for emp in dept.get_employees():
                employee_map[emp.id] = emp
        return employee_map

    @staticmethod
    def restore_project_links(
        project: Project, 
        team_ids: List[int], 
        employee_map: Dict[int, AbstractEmployee]
    ) -> None:
        """
        Восстанавливает команду проекта по списку ID сотрудников.

        :param project: Объект проекта.
        :param team_ids: Список ID сотрудников команды.
        :param employee_map: Карта {id: employee}.
        """
        for emp_id in team_ids:
            if emp_id in employee_map:
                project.add_team_member(employee_map[emp_id])
            else:
                print(
                    f"[WARN] Сотрудник ID={emp_id} для проекта '{project.name}' "
                    f"не найден в штате."
                )