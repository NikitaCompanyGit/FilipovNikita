class EmployeeBuilder:
    def __init__(self, logger: ILogger, validator: EmployeeDataValidator):
        self._logger = logger
        self._validator = validator
        self._reset_data()

    def _reset_data(self):
        self._data = {
            'type': 'employee',
            'id': None,
            'name': None,
            'department': None,
            'base_salary': None,
            'bonus': None,
            'seniority': None,
            'tech_stack': [],
            'commission_rate': None,
        }

    def set_id(self, emp_id: int) -> 'EmployeeBuilder':
        self._data['id'] = emp_id
        self._logger.debug(f"ID: {emp_id}")
        return self

    def set_name(self, name: str) -> 'EmployeeBuilder':
        self._data['name'] = name.strip() if name else name
        self._logger.debug(f"Имя: {self._data['name']}")
        return self

    def set_department(self, department: str) -> 'EmployeeBuilder':
        self._data['department'] = department.strip() if department else department
        self._logger.debug(f"Отдел: {self._data['department']}")
        return self

    def set_base_salary(self, salary: float) -> 'EmployeeBuilder':
        self._data['base_salary'] = salary
        self._logger.debug(f"Зарплата: {salary}")
        return self

    def as_manager(self, bonus: float = 0.0) -> 'EmployeeBuilder':
        self._data['type'] = 'manager'
        self._data['bonus'] = bonus
        return self

    def as_developer(self, seniority: str = 'junior', 
                     tech_stack: Optional[List[str]] = None) -> 'EmployeeBuilder':
        self._data['type'] = 'developer'
        self._data['seniority'] = seniority
        self._data['tech_stack'] = tech_stack or ['Python']
        return self

    def as_salesperson(self, commission: float = 0.1) -> 'EmployeeBuilder':
        self._data['type'] = 'salesperson'
        self._data['commission_rate'] = commission
        return self

    def build(self) -> dict:
        self._logger.info(f"Построение {self._data['type']}: {self._data.get('name')}")
        self._validator.validate_employee_data(self._data)
        result = {k: v for k, v in self._data.items() 
                 if v is not None and (not isinstance(v, list) or len(v) > 0)}
        return result

    def reset(self) -> 'EmployeeBuilder':
        self._reset_data()
        return self