from base.abstract_employee import AbstractEmployee

class Salesperson(AbstractEmployee):
    """
    Класс Продавца (Salesperson).
    
    Особенности:
    - Зарплата динамическая: База + (Объем продаж * Процент комиссии).
    - Позволяет обновлять текущий объем продаж (накопительно).
    """

    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, 
                 commission_rate: float, sales_volume: float = 0.0):
        """
        Инициализация продавца.
        
        :param commission_rate: Процент комиссии (от 0.0 до 1.0).
        :param sales_volume: Начальный объем продаж (по умолчанию 0).
        """
        super().__init__(emp_id, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume

    @property
    def commission_rate(self) -> float:
        return self.__commission_rate

    @commission_rate.setter
    def commission_rate(self, value: float):
        """Устанавливает комиссию. Значение должно быть дробным от 0.0 до 1.0."""
        if not isinstance(value, (int, float)):
            raise ValueError("Комиссия должна быть числом.")
        if not (0 <= value <= 1.0):
            raise ValueError(f"Комиссия должна быть в диапазоне от 0.0 до 1.0. Получено: {value}")
        self.__commission_rate = float(value)

    @property
    def sales_volume(self) -> float:
        return self.__sales_volume

    @sales_volume.setter
    def sales_volume(self, value: float):
        """Устанавливает объем продаж. Не может быть отрицательным."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Объем продаж не может быть отрицательным.")
        self.__sales_volume = float(value)

    def update_sales(self, amount: float) -> None:
        """
        Увеличивает текущий объем продаж на указанную сумму.
        Используется при совершении новых сделок.
        """
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Сумма добавления продаж должна быть положительной.")
        self.__sales_volume += float(amount)

    def calculate_salary(self) -> float:
        """
        Рассчитывает зарплату.
        Формула: Оклад + (Продажи * Комиссия).
        """
        return self.base_salary + (self.sales_volume * self.commission_rate)

    def get_info(self) -> str:
        """
        Возвращает детальную информацию о продавце, включая текущие показатели продаж.
        """
        return (f"{super().__str__()}\n"
                f"   -> Тип: Salesperson\n"
                f"   -> Продажи: {self.sales_volume}\n"
                f"   -> Комиссия: {self.commission_rate * 100}%\n"
                f"   -> Итоговая выплата: {self.calculate_salary()} руб.")

    def to_dict(self) -> dict:
        """
        Сериализует данные продавца.
        Сохраняет текущий объем продаж и ставку комиссии.
        """
        return {
            "type": "salesperson",
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary,
            "commission": self.commission_rate,
            "sales_volume": self.sales_volume
        }
