from base.abstract_employee import AbstractEmployee

class OrdinaryEmployee(AbstractEmployee):
    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return f"{super().__str__()} -> Тип: Штатный -> Итого: {self.calculate_salary()} руб."

    # --- ВАЖНО: Реализация абстрактного метода ---
    def to_dict(self) -> dict:
        return {
            "type": "employee",
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary
        }
