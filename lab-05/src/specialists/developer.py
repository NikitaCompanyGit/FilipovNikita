from base.abstract_employee import AbstractEmployee

class Developer(AbstractEmployee):
    """
    Класс Разработчика.
    
    Особенности:
    - Зарплата зависит от уровня квалификации (Seniority: junior/middle/senior).
    - Хранит стек технологий (tech_stack).
    - Поддерживает протокол итератора для перебора навыков.
    """
    
    # Коэффициенты умножения оклада в зависимости от уровня
    LEVEL_MULTIPLIERS = {
        "junior": 1.0,
        "middle": 1.5,
        "senior": 2.0
    }

    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, 
                 seniority_level: str, tech_stack: list[str] = None):
        """
        Инициализация разработчика.
        
        :param seniority_level: Уровень ('junior', 'middle', 'senior').
        :param tech_stack: Список технологий (строк).
        """
        super().__init__(emp_id, name, department, base_salary)
        self.seniority_level = seniority_level
        self.__tech_stack = tech_stack if tech_stack is not None else []

    @property
    def seniority_level(self) -> str:
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value: str):
        """
        Устанавливает уровень квалификации.
        Проверяет, допустим ли переданный уровень (согласно LEVEL_MULTIPLIERS).
        """
        if not isinstance(value, str):
            raise ValueError("Уровень должен быть строкой.")
        
        normalized_value = value.lower().strip()
        if normalized_value not in self.LEVEL_MULTIPLIERS:
            valid_levels = list(self.LEVEL_MULTIPLIERS.keys())
            raise ValueError(f"Недопустимый уровень: '{value}'. Доступны: {valid_levels}")
        
        self.__seniority_level = normalized_value

    def add_skill(self, new_skill: str) -> None:
        """
        Добавляет новый навык в стек технологий.
        Игнорирует дубликаты и пустые строки.
        """
        if new_skill and isinstance(new_skill, str):
            if new_skill not in self.__tech_stack:
                self.__tech_stack.append(new_skill)

    def calculate_salary(self) -> float:
        """
        Рассчитывает зарплату с учетом коэффициента уровня (Seniority Multiplier).
        """
        multiplier = self.LEVEL_MULTIPLIERS[self.seniority_level]
        return self.base_salary * multiplier

    def get_info(self) -> str:
        """
        Возвращает информацию о разработчике, включая уровень и стек технологий.
        """
        stack_str = ", ".join(self.__tech_stack)
        return (f"{super().__str__()}\n"
                f"   -> Тип: Developer ({self.seniority_level.title()})\n"
                f"   -> Стек: [{stack_str}]\n"
                f"   -> Итоговая выплата: {self.calculate_salary()} руб.")

    def to_dict(self) -> dict:
        """
        Сериализует данные разработчика.
        Сохраняет уровень квалификации и список технологий.
        """
        return {
            "type": "developer",
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary,
            "seniority": self.seniority_level,
            "tech_stack": self.__tech_stack
        }

    def __iter__(self):
        """
        Реализация протокола итератора.
        Позволяет перебирать стек технологий разработчика в циклах (for skill in dev).
        """
        return iter(self.__tech_stack)
