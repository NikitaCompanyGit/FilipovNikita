"""  
test_part1_encapsulation.py - Тесты инкапсуляции (40+ тестов)

Проверяет:
- Создание сотрудников с валидацией
- Защиту приватных атрибутов
- Работу properties (getters/setters)
- Соответствие правилам инкапсуляции
"""

import pytest
import time
from contextlib import contextmanager
from src.base.employee import Employee
from src.base.exceptions import (
    EmployeeNotFoundError,
    DuplicateIdError,
    InvalidStatusError,
    DependencyError
)


# ═══════════════════════════════════════════════════════════
# ФИКСТУРЫ
# ═══════════════════════════════════════════════════════════

@pytest.fixture
def sample_employee_data():
    """Фикстура с тестовыми данными сотрудников"""
    return {
        "regular": {
            "emp_id": 1,
            "name": "Alice",
            "department": "IT",
            "base_salary": 5000
        },
        "manager": {
            "emp_id": 2,
            "name": "Bob",
            "department": "HR",
            "base_salary": 6000
        },
        "developer": {
            "emp_id": 3,
            "name": "Charlie",
            "department": "IT",
            "base_salary": 5500
        },
        "analyst": {
            "emp_id": 4,
            "name": "Diana",
            "department": "Finance",
            "base_salary": 4500
        }
    }


@pytest.fixture
def performance_timer():
    """Фикстура для измерения времени выполнения"""

    @contextmanager
    def timer():
        class Timer:
            def __init__(self):
                self.elapsed = 0

        timer_obj = Timer()
        start = time.time()
        yield timer_obj
        timer_obj.elapsed = time.time() - start

    return timer


# ═══════════════════════════════════════════════════════════
# UNIT-ТЕСТЫ
# ═══════════════════════════════════════════════════════════

@pytest.mark.unit
@pytest.mark.part1
class TestEmployeeCreation:
    """Тесты создания сотрудника (8 тестов)"""

    def test_valid_creation(self):
        """✅ Создание сотрудника с корректными данными"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000

    def test_creation_with_different_ids(self):
        """✅ Создание сотрудников с разными ID"""
        for i in range(1, 6):
            emp = Employee(emp_id=i, name=f"Employee{i}", department="IT", base_salary=5000)
            assert emp.id == i

    def test_creation_with_float_salary(self):
        """✅ Зарплата может быть float"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000.50)
        assert emp.base_salary == 5000.50

    def test_creation_with_special_chars_in_name(self):
        """✅ Имя может содержать специальные символы"""
        emp = Employee(emp_id=1, name="Alice-Marie O'Connor", department="IT", base_salary=5000)
        assert emp.name == "Alice-Marie O'Connor"

    def test_creation_with_unicode_department(self):
        """✅ Названия на кириллице"""
        emp = Employee(emp_id=1, name="Алиса", department="ИТ", base_salary=5000)
        assert emp.name == "Алиса"
        assert emp.department == "ИТ"

    def test_employee_string_representation(self):
        """✅ Строковое представление сотрудника"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        str_repr = str(emp)

        assert "Alice" in str_repr
        assert "IT" in str_repr
        assert "1" in str_repr

    def test_calculate_salary_base(self):
        """✅ Базовый расчет зарплаты"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        assert emp.calculate_salary() == 5000

    def test_equality_by_id(self):
        """✅ Сотрудники равны если у них одинаковые ID"""
        emp1 = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp2 = Employee(emp_id=1, name="Bob", department="HR", base_salary=4000)

        assert emp1 == emp2


@pytest.mark.unit
@pytest.mark.part1
class TestPropertyGettersSetter:
    """Тесты работы properties (12 тестов)"""

    def test_id_getter(self):
        """✅ Получение ID через property"""
        emp = Employee(emp_id=42, name="Alice", department="IT", base_salary=5000)
        assert emp.id == 42

    def test_name_getter(self):
        """✅ Получение имени через property"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        assert emp.name == "Alice"

    def test_department_getter(self):
        """✅ Получение отдела через property"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        assert emp.department == "IT"

    def test_salary_getter(self):
        """✅ Получение зарплаты через property"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        assert emp.base_salary == 5000

    def test_id_setter_valid(self):
        """✅ Установка корректного ID"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp.id = 99
        assert emp.id == 99

    def test_name_setter(self):
        """✅ Изменение имени"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp.name = "Bob"
        assert emp.name == "Bob"

    def test_department_setter(self):
        """✅ Изменение отдела"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp.department = "HR"
        assert emp.department == "HR"

    def test_salary_setter_valid(self):
        """✅ Установка корректной зарплаты"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp.base_salary = 6000
        assert emp.base_salary == 6000

    def test_setter_with_chained_changes(self):
        """✅ Множественные изменения"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        emp.name = "Bob"
        emp.department = "HR"
        emp.base_salary = 6000

        assert emp.name == "Bob"
        assert emp.department == "HR"
        assert emp.base_salary == 6000

    def test_setter_preserves_other_attributes(self):
        """✅ Изменение одного атрибута не влияет на другие"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        original_id = emp.id
        original_salary = emp.base_salary

        emp.name = "Bob"

        assert emp.id == original_id
        assert emp.base_salary == original_salary

    def test_multiple_employees_independent_properties(self):
        """✅ Properties разных сотрудников независимы"""
        emp1 = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp2 = Employee(emp_id=2, name="Bob", department="HR", base_salary=4000)

        emp1.name = "NewAlice"
        emp1.base_salary = 6000

        assert emp1.name == "NewAlice"
        assert emp1.base_salary == 6000

        assert emp2.name == "Bob"
        assert emp2.base_salary == 4000


@pytest.mark.unit
@pytest.mark.part1
class TestValidation:
    """Тесты валидации данных (10 тестов)"""

    def test_invalid_id_negative(self):
        """❌ ID не может быть отрицательным"""
        with pytest.raises(ValueError, match="ID должен быть"):
            Employee(emp_id=-1, name="Alice", department="IT", base_salary=5000)

    def test_invalid_id_zero(self):
        """❌ ID не может быть нулём"""
        with pytest.raises(ValueError):
            Employee(emp_id=0, name="Alice", department="IT", base_salary=5000)

    def test_invalid_salary_negative(self):
        """❌ Зарплата не может быть отрицательной"""
        with pytest.raises(ValueError, match="Зарплата"):
            Employee(emp_id=1, name="Alice", department="IT", base_salary=-5000)

    def test_invalid_salary_zero(self):
        """❌ Зарплата не может быть нулём"""
        with pytest.raises(ValueError):
            Employee(emp_id=1, name="Alice", department="IT", base_salary=0)

    def test_setter_invalid_id(self):
        """❌ Сеттер ID валидирует значение"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with pytest.raises(ValueError):
            emp.id = -10

    def test_setter_invalid_salary(self):
        """❌ Сеттер зарплаты валидирует значение"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with pytest.raises(ValueError):
            emp.base_salary = -1000

    def test_validation_error_message(self):
        """❌ Сообщение об ошибке информативно"""
        with pytest.raises(ValueError) as exc_info:
            Employee(emp_id=-5, name="Alice", department="IT", base_salary=5000)

        error_msg = str(exc_info.value)
        assert "ID" in error_msg or "id" in error_msg

    @pytest.mark.parametrize("invalid_salary", [-100, -1, 0])
    def test_multiple_invalid_salaries(self, invalid_salary):
        """❌ Все отрицательные и нулевые зарплаты отклоняются"""
        with pytest.raises(ValueError):
            Employee(emp_id=1, name="Alice", department="IT", base_salary=invalid_salary)

    @pytest.mark.parametrize("valid_salary", [0.01, 1, 1000, 1000000, 1000000.99])
    def test_multiple_valid_salaries(self, valid_salary):
        """✅ Все положительные зарплаты принимаются"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=valid_salary)
        assert emp.base_salary == valid_salary

    def test_type_error_on_wrong_id_type(self):
        """❌ ID должен быть целым числом"""
        with pytest.raises((TypeError, ValueError)):
            Employee(emp_id="abc", name="Alice", department="IT", base_salary=5000)


@pytest.mark.unit
@pytest.mark.part1
class TestPrivateAttributeProtection:
    """Тесты защиты приватных атрибутов (10 тестов)"""

    def test_cannot_access_private_id(self):
        """❌ Нельзя получить __id напрямую"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with pytest.raises(AttributeError):
            _ = emp.__id

    def test_cannot_access_private_name(self):
        """❌ Нельзя получить __name напрямую"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with pytest.raises(AttributeError):
            _ = emp.__name

    def test_cannot_access_private_department(self):
        """❌ Нельзя получить __department напрямую"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with pytest.raises(AttributeError):
            _ = emp.__department

    def test_cannot_access_private_salary(self):
        """❌ Нельзя получить __base_salary напрямую"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with pytest.raises(AttributeError):
            _ = emp.__base_salary

    def test_cannot_set_private_id_directly(self):
        """❌ Нельзя установить __id напрямую"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with pytest.raises(AttributeError):
            emp.__id = 999

    def test_cannot_modify_private_salary_directly(self):
        """❌ Нельзя изменить __base_salary напрямую"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        original_salary = emp.base_salary

        # Попытка прямого доступа не сработает
        with pytest.raises(AttributeError):
            emp.__base_salary = 10000

        # Зарплата не изменилась
        assert emp.base_salary == original_salary

    def test_property_prevents_invalid_modification(self):
        """❌ Даже через property нельзя установить невалидные данные"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        # Попытка установить отрицательную зарплату
        with pytest.raises(ValueError):
            emp.base_salary = -100

        # Зарплата не изменилась
        assert emp.base_salary == 5000

    def test_no_public_id_attribute(self):
        """✅ Нет публичного атрибута 'id' (только property)"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        # Через property работает
        assert emp.id == 1

        # Прямой доступ к __dict__ не содержит 'id'
        assert 'id' not in emp.__dict__ or '__id' in emp.__dict__

    def test_encapsulation_with_multiple_instances(self):
        """✅ Инкапсуляция работает для всех экземпляров"""
        emp1 = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp2 = Employee(emp_id=2, name="Bob", department="HR", base_salary=4000)

        # Оба защищены
        with pytest.raises(AttributeError):
            _ = emp1.__id

        with pytest.raises(AttributeError):
            _ = emp2.__id


# ═══════════════════════════════════════════════════════════
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ PART 1
# ═══════════════════════════════════════════════════════════

@pytest.mark.integration
@pytest.mark.part1
class TestEmployeeIntegration:
    """Интеграционные тесты инкапсуляции (5 тестов)"""

    def test_create_and_modify_workflow(self):
        """✅ Полный цикл создания и модификации"""
        # Создание
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        # Проверка
        assert emp.id == 1
        assert emp.calculate_salary() == 5000

        # Модификация через properties
        emp.base_salary = 6000

        # Проверка изменения
        assert emp.base_salary == 6000
        assert emp.calculate_salary() == 6000

    def test_batch_employee_creation(self, sample_employee_data):
        """✅ Создание множества сотрудников"""
        employees = []

        for emp_type, data in sample_employee_data.items():
            emp = Employee(
                emp_id=data["emp_id"],
                name=data["name"],
                department=data["department"],
                base_salary=data["base_salary"]
            )
            employees.append(emp)

        assert len(employees) == 4
        assert all(isinstance(e, Employee) for e in employees)

    def test_employee_data_isolation(self):
        """✅ Данные сотрудников изолированы"""
        emp1 = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)
        emp2 = Employee(emp_id=2, name="Bob", department="IT", base_salary=4000)

        # Изменение emp1 не влияет на emp2
        emp1.base_salary = 10000
        emp1.name = "NewAlice"

        assert emp2.base_salary == 4000
        assert emp2.name == "Bob"

    def test_validation_prevents_bad_state(self):
        """✅ Валидация предотвращает неправильное состояние"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        # Попытка установить невалидные значения
        with pytest.raises(ValueError):
            emp.base_salary = -100

        with pytest.raises(ValueError):
            emp.id = 0

        # Состояние не изменилось
        assert emp.id == 1
        assert emp.base_salary == 5000

    def test_property_access_performance(self, performance_timer):
        """✅ Доступ через properties быстрый"""
        emp = Employee(emp_id=1, name="Alice", department="IT", base_salary=5000)

        with performance_timer() as timer:
            for _ in range(10000):
                _ = emp.id
                _ = emp.name
                _ = emp.base_salary

        # 30000 операций должны быть быстрыми
        assert timer.elapsed < 0.1  # Менее 100ms


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
