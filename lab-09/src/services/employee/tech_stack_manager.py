from typing import List
from services.employee.developer_validator import DeveloperValidator

class TechStackManager:
    """
    Менеджер стека технологий разработчика.

    Отвечает ТОЛЬКО за управление списком навыков/технологий.
    Обеспечивает инкапсуляцию и контроль над добавлением/удалением.

    SOLID:
    - SRP: Отвечает только за управление tech_stack
    - Encapsulation: Скрывает внутреннюю структуру хранения
    """

    def __init__(self, initial_skills: List[str] = None):
        """
        Инициализация менеджера стека технологий.

        :param initial_skills: Начальный список навыков (по умолчанию пустой).
        """
        self._tech_stack: List[str] = []

        if initial_skills:
            for skill in initial_skills:
                self.add_skill(skill)

    def add_skill(self, skill: str) -> None:
        """
        Добавляет новый навык в стек технологий.

        Проверяет валидность и игнорирует дубликаты.

        :param skill: Название технологии.
        :raises ValueError: Если навык невалиден (пустая строка).
        """
        validated_skill = DeveloperValidator.validate_skill_name(skill)

        # Игнорируем дубликаты (case-insensitive)
        if not self.has_skill(validated_skill):
            self._tech_stack.append(validated_skill)

    def remove_skill(self, skill: str) -> bool:
        """
        Удаляет навык из стека технологий.

        :param skill: Название технологии для удаления.
        :returns: True, если навык был удалён, False, если не найден.
        """
        original_length = len(self._tech_stack)
        self._tech_stack = [
            s for s in self._tech_stack 
            if s.lower() != skill.lower()
        ]
        return len(self._tech_stack) < original_length

    def has_skill(self, skill: str) -> bool:
        """
        Проверяет наличие навыка в стеке (case-insensitive).

        :param skill: Название технологии.
        :returns: True, если навык присутствует.
        """
        return any(s.lower() == skill.lower() for s in self._tech_stack)

    def get_skills(self) -> List[str]:
        """
        Возвращает список всех навыков (копия для защиты от изменений).

        :returns: Копия списка навыков.
        """
        return self._tech_stack.copy()

    def get_skills_count(self) -> int:
        """
        Возвращает количество навыков в стеке.

        :returns: Число навыков.
        """
        return len(self._tech_stack)

    def clear_skills(self) -> None:
        """
        Очищает весь стек технологий.
        """
        self._tech_stack.clear()

    def __iter__(self):
        """
        Поддержка итератора для перебора навыков.

        Позволяет использовать: for skill in tech_stack_manager
        """
        return iter(self._tech_stack)

    def __len__(self):
        """
        Возвращает количество навыков при вызове len().
        """
        return len(self._tech_stack)

    def __contains__(self, skill: str):
        """
        Поддержка оператора 'in' для проверки наличия навыка.

        Позволяет использовать: if "Python" in tech_stack_manager
        """
        return self.has_skill(skill)