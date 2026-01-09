from base.abstract_employee import AbstractEmployee

class DepartmentValidator:
    """
    Валидатор для операций с отделом.
    Отвечает ТОЛЬКО за проверку корректности операций (SRP).
    """

    @staticmethod
    def validate_employee(employee: AbstractEmployee) -> None:
        """
        Проверяет, что объект является сотрудником.

        :raises TypeError: Если объект не наследник AbstractEmployee.
        """
        if not isinstance(employee, AbstractEmployee):
            raise TypeError(
                f"В отдел можно добавлять только наследников AbstractEmployee. "
                f"Получен: {type(employee).__name__}"
            )

    @staticmethod
    def validate_employee_id(employee_id: int) -> None:
        """
        Проверяет корректность ID сотрудника.

        :raises ValueError: Если ID некорректен.
        """
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError(f"ID сотрудника должен быть положительным целым числом. Получено: {employee_id}")