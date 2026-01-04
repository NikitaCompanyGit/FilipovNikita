from base.abstract_employee import AbstractEmployee

class Manager(AbstractEmployee):
    """
    Класс Менеджера.
    
    Особенность:
    - Имеет фиксированный бонус к зарплате (атрибут `bonus`).
    - Зарплата рассчитывается как сумма оклада и бонуса.
    """
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, bonus: float):
        """
        Инициализация менеджера.
        
        :param bonus: Размер фиксированного бонуса (должен быть >= 0).
        """
        super().__init__(emp_id, name, department, base_salary)
        self.bonus = bonus

    @property
    def bonus(self) -> float:
        return self.__bonus

    @bonus.setter
    def bonus(self, value: float):
        """Устанавливает бонус с проверкой на неотрицательность."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Бонус должен быть положительным числом. Получено: {value}")
        self.__bonus = float(value)

    def calculate_salary(self) -> float:
        """
        Рассчитывает итоговую зарплату менеджера.
        Формула: Базовая ставка + Бонус.
        """
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        """
        Возвращает расширенную информацию о менеджере, включая размер бонуса.
        """
        return (f"{super().__str__()}\n"
                f"   -> Тип: Manager\n"
                f"   -> Бонус: {self.bonus}\n"
                f"   -> Итоговая выплата: {self.calculate_salary()} руб.")

    def to_dict(self) -> dict:
        """
        Сериализует данные менеджера.
        Сохраняет поле 'bonus', необходимое для восстановления объекта.
        """
        return {
            "type": "manager",
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary,
            "bonus": self.bonus
        }
