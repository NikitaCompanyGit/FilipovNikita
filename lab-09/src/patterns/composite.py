class ValidationError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(f"Ошибки валидации: {', '.join(errors)}")

class IValidator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> List[str]:
        pass

class PositiveIntegerValidator(IValidator):
    def __init__(self, field_name: str):
        self.field_name = field_name

    def validate(self, value: Any) -> List[str]:
        errors = []
        if value is None:
            errors.append(f"{self.field_name} не установлен")
        elif not isinstance(value, int):
            errors.append(f"{self.field_name} должен быть целым числом")
        elif value <= 0:
            errors.append(f"{self.field_name} должен быть положительным")
        return errors

class NonEmptyStringValidator(IValidator):
    def __init__(self, field_name: str):
        self.field_name = field_name

    def validate(self, value: Any) -> List[str]:
        errors = []
        if value is None:
            errors.append(f"{self.field_name} не установлен")
        elif not isinstance(value, str):
            errors.append(f"{self.field_name} должен быть строкой")
        elif len(value.strip()) == 0:
            errors.append(f"{self.field_name} не может быть пустым")
        return errors

class NonNegativeFloatValidator(IValidator):
    def __init__(self, field_name: str):
        self.field_name = field_name

    def validate(self, value: Any) -> List[str]:
        errors = []
        if value is None:
            errors.append(f"{self.field_name} не установлен")
        elif not isinstance(value, (int, float)):
            errors.append(f"{self.field_name} должен быть числом")
        elif value < 0:
            errors.append(f"{self.field_name} не может быть отрицательным")
        return errors

class RangeValidator(IValidator):
    def __init__(self, field_name: str, min_val: float, max_val: float):
        self.field_name = field_name
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value: Any) -> List[str]:
        errors = []
        if value is None:
            errors.append(f"{self.field_name} не установлен")
        elif not isinstance(value, (int, float)):
            errors.append(f"{self.field_name} должен быть числом")
        elif not (self.min_val <= value <= self.max_val):
            errors.append(f"{self.field_name} должен быть в [{self.min_val}, {self.max_val}]")
        return errors

class EnumValidator(IValidator):
    def __init__(self, field_name: str, valid_values: set):
        self.field_name = field_name
        self.valid_values = valid_values

    def validate(self, value: Any) -> List[str]:
        errors = []
        if value is None:
            errors.append(f"{self.field_name} не установлен")
        elif value not in self.valid_values:
            errors.append(f"Неверный {self.field_name}: {value}")
        return errors

class EmployeeDataValidator:
    def __init__(self):
        self._validators = {
            'id': PositiveIntegerValidator('ID'),
            'name': NonEmptyStringValidator('Имя'),
            'department': NonEmptyStringValidator('Отдел'),
            'base_salary': NonNegativeFloatValidator('Базовая зарплата'),
        }

        self._type_validators = {
            'manager': {
                'bonus': NonNegativeFloatValidator('Бонус'),
            },
            'developer': {
                'seniority': EnumValidator('Уровень', {'junior', 'middle', 'senior'}),
            },
            'salesperson': {
                'commission_rate': RangeValidator('Комиссия', 0.0, 1.0),
            }
        }

    def validate_employee_data(self, data: dict) -> None:
        all_errors = []

        for field, validator in self._validators.items():
            errors = validator.validate(data.get(field))
            all_errors.extend(errors)

        emp_type = data.get('type', 'employee')
        if emp_type in self._type_validators:
            for field, validator in self._type_validators[emp_type].items():
                errors = validator.validate(data.get(field))
                all_errors.extend(errors)

        if all_errors:
            raise ValidationError(all_errors)