"""Валидаторы данных."""
from typing import Any

class ValidationError(ValueError):
    pass

class EmployeeValidator:
    ERROR_MESSAGES = {
        'id_invalid': "ID должен быть положительным целым числом. Получено: {value}",
        'name_empty': "Имя сотрудника не может быть пустой строкой.",
        'department_invalid': "Название отдела должно быть строкой.",
        'salary_invalid': "Базовая зарплата должна быть положительным числом. Получено: {value}",
    }
    
    @staticmethod
    def validate_id(value: Any) -> int:
        if not isinstance(value, int) or value <= 0:
            raise ValidationError(EmployeeValidator.ERROR_MESSAGES['id_invalid'].format(value=value))
        return value
    
    @staticmethod
    def validate_name(value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(EmployeeValidator.ERROR_MESSAGES['name_empty'])
        return value.strip()
    
    @staticmethod
    def validate_department(value: Any) -> str:
        if not isinstance(value, str):
            raise ValidationError(EmployeeValidator.ERROR_MESSAGES['department_invalid'])
        return value.strip()
    
    @staticmethod
    def validate_salary(value: Any) -> float:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValidationError(EmployeeValidator.ERROR_MESSAGES['salary_invalid'].format(value=value))
        return float(value)