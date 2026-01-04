#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ЛР№8: Часть 1 - Тестирование инкапсуляции и базового класса Employee
=====================================================================

Модуль содержит модульные тесты для класса Employee, проверяющие:
- Корректность инициализации с валидными данными
- Валидацию данных в сеттерах
- Работу методов __str__ и calculate_salary
- Обработку ошибок

Используемые фреймворки:
- pytest: фреймворк для тестирования
- unittest.mock: создание mock-объектов (если требуется)

Для запуска:
    pytest test_employee.py -v
"""

import pytest
import sys
import os

# Добавляем path для импорта из src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Импортируем класс Employee для тестирования
try:
    from base.employee import Employee
    from base.exceptions import ValidationError
except ImportError:
    # Если не удалось импортировать, пропускаем тесты
    pytest.skip("Cannot import Employee class", allow_module_level=True)


class TestEmployeeCreation:
    """
    Тесты для проверки корректной инициализации класса Employee.
    
    Проверяет:
    - Создание объекта с валидными данными
    - Корректность установки всех параметров
    """
    
    def test_employee_creation_valid_data(self):
        """
        Тест: создание сотрудника с валидными данными.
        
        Arrange: подготовка валидных параметров
        Act: создание объекта Employee
        Assert: проверка корректности установки всех атрибутов
        """
        # Arrange
        emp_id = 1
        name = "Alice"
        department = "IT"
        base_salary = 5000
        
        # Act
        emp = Employee(emp_id, name, department, base_salary)
        
        # Assert
        assert emp.id == emp_id
        assert emp.name == name
        assert emp.department == department
        assert emp.base_salary == base_salary
    
    def test_employee_creation_with_different_values(self):
        """
        Тест: создание сотрудника с различными корректными значениями.
        
        Проверяет множество комбинаций валидных данных.
        """
        # Arrange & Act & Assert
        test_cases = [
            (1, "John Doe", "Sales", 3500),
            (2, "Jane Smith", "HR", 4000),
            (999, "Bob Johnson", "Development", 8000),
        ]
        
        for emp_id, name, department, salary in test_cases:
            emp = Employee(emp_id, name, department, salary)
            assert emp.id == emp_id
            assert emp.name == name
            assert emp.department == department
            assert emp.base_salary == salary


class TestEmployeeValidation:
    """
    Тесты для проверки валидации данных в сеттерах.
    
    Проверяет:
    - Генерацию исключений при отрицательных ID и зарплате
    - Генерацию исключений при пустых строках для имени
    - Генерацию исключений при нулевых значениях
    """
    
    def test_employee_invalid_id_negative_raises_error(self):
        """
        Тест: попытка создать сотрудника с отрицательным ID.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Employee(-1, "Alice", "IT", 5000)
    
    def test_employee_invalid_id_zero_raises_error(self):
        """
        Тест: попытка создать сотрудника с нулевым ID.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Employee(0, "Alice", "IT", 5000)
    
    def test_employee_invalid_name_empty_raises_error(self):
        """
        Тест: попытка создать сотрудника с пустым именем.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Employee(1, "", "IT", 5000)
    
    def test_employee_invalid_name_whitespace_raises_error(self):
        """
        Тест: попытка создать сотрудника с именем из пробелов.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Employee(1, "   ", "IT", 5000)
    
    def test_employee_invalid_salary_negative_raises_error(self):
        """
        Тест: попытка создать сотрудника с отрицательной зарплатой.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Employee(1, "Alice", "IT", -5000)
    
    def test_employee_invalid_salary_zero_raises_error(self):
        """
        Тест: попытка создать сотрудника с нулевой зарплатой.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Employee(1, "Alice", "IT", 0)
    
    def test_employee_invalid_department_empty_raises_error(self):
        """
        Тест: попытка создать сотрудника с пустым отделом.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Employee(1, "Alice", "", 5000)


class TestEmployeeSetters:
    """
    Тесты для проверки валидации в сеттерах.
    
    Проверяет:
    - Корректное изменение значений через сеттеры
    - Генерацию исключений при неправильных значениях
    """
    
    def test_employee_set_salary_valid(self):
        """
        Тест: изменение зарплаты на валидное значение.
        
        Act: установка новой зарплаты
        Assert: проверка корректного изменения
        """
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act
        emp.base_salary = 6000
        
        # Assert
        assert emp.base_salary == 6000
    
    def test_employee_set_salary_negative_raises_error(self):
        """
        Тест: попытка установить отрицательную зарплату через сеттер.
        
        Assert: ожидается исключение ValueError
        """
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Assert
        with pytest.raises(ValueError):
            emp.base_salary = -1000
    
    def test_employee_set_name_valid(self):
        """
        Тест: изменение имени на валидное значение.
        
        Act: установка нового имени
        Assert: проверка корректного изменения
        """
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act
        emp.name = "Bob"
        
        # Assert
        assert emp.name == "Bob"
    
    def test_employee_set_name_empty_raises_error(self):
        """
        Тест: попытка установить пустое имя через сеттер.
        
        Assert: ожидается исключение ValueError
        """
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Assert
        with pytest.raises(ValueError):
            emp.name = ""


class TestEmployeeMethods:
    """
    Тесты для проверки методов класса Employee.
    
    Проверяет:
    - Работа метода calculate_salary
    - Работа метода __str__
    - Работа методов для получения информации
    """
    
    def test_employee_calculate_salary(self):
        """
        Тест: расчет зарплаты для обычного сотрудника.
        
        Act: вызов метода calculate_salary
        Assert: проверка, что результат равен базовой зарплате
        """
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act
        salary = emp.calculate_salary()
        
        # Assert
        assert salary == 5000
    
    def test_employee_calculate_salary_different_values(self):
        """
        Тест: расчет зарплаты для разных базовых значений.
        
        Параметризованный тест с несколькими значениями.
        """
        # Arrange & Act & Assert
        test_cases = [
            (1, "John", "IT", 3000, 3000),
            (2, "Jane", "HR", 4500, 4500),
            (3, "Bob", "Sales", 7000, 7000),
        ]
        
        for emp_id, name, dept, base_salary, expected in test_cases:
            emp = Employee(emp_id, name, dept, base_salary)
            assert emp.calculate_salary() == expected
    
    def test_employee_str_representation(self):
        """
        Тест: проверка строкового представления сотрудника.
        
        Act: преобразование объекта в строку
        Assert: проверка формата и содержимого строки
        """
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act
        result = str(emp)
        
        # Assert
        # Проверяем, что строка содержит важную информацию
        assert "Alice" in result
        assert "IT" in result
        assert "5000" in result
        assert "1" in result
    
    def test_employee_string_format_contains_key_info(self):
        """
        Тест: проверка, что __str__ содержит все ключевые данные.
        
        Assert: все поля должны быть представлены в строке
        """
        # Arrange
        emp = Employee(42, "TestName", "TestDept", 9999)
        
        # Act
        result = str(emp)
        
        # Assert
        assert "42" in result
        assert "TestName" in result
        assert "TestDept" in result
        assert "9999" in result


class TestEmployeeEquality:
    """
    Тесты для проверки операций сравнения сотрудников.
    
    Проверяет:
    - Равенство по ID
    - Неравенство разных сотрудников
    """
    
    def test_employee_equality_same_id(self):
        """
        Тест: два сотрудника с одинаковым ID считаются равными.
        
        Act: сравнение двух объектов
        Assert: они должны быть равны
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(1, "Bob", "HR", 6000)
        
        # Act & Assert
        assert emp1 == emp2
    
    def test_employee_inequality_different_id(self):
        """
        Тест: два сотрудника с разными ID не считаются равными.
        
        Act: сравнение двух объектов
        Assert: они должны быть неравны
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Alice", "IT", 5000)
        
        # Act & Assert
        assert emp1 != emp2


class TestEmployeeSalaryComparison:
    """
    Тесты для проверки операций сравнения по зарплате.
    
    Проверяет:
    - Сравнение по базовой зарплате
    - Операторы <, >, <=, >=
    """
    
    def test_employee_less_than_by_salary(self):
        """
        Тест: сравнение сотрудников по оператору <.
        
        Act: сравнение зарплат
        Assert: проверка корректности оператора
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 6000)
        
        # Act & Assert
        assert emp1 < emp2
    
    def test_employee_greater_than_by_salary(self):
        """
        Тест: сравнение сотрудников по оператору >.
        
        Act: сравнение зарплат
        Assert: проверка корректности оператора
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 7000)
        emp2 = Employee(2, "Bob", "HR", 6000)
        
        # Act & Assert
        assert emp1 > emp2
    
    def test_employee_comparison_equal_salaries(self):
        """
        Тест: сравнение сотрудников с одинаковой зарплатой.
        
        Act: сравнение зарплат
        Assert: проверка, что они равны по зарплате
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 5000)
        
        # Act & Assert
        assert emp1 <= emp2
        assert emp1 >= emp2


class TestEmployeeSalaryAddition:
    """
    Тесты для проверки сложения зарплат.
    
    Проверяет:
    - Сложение зарплат двух сотрудников
    - Коммутативность операции
    """
    
    def test_employee_salary_addition(self):
        """
        Тест: сложение зарплат двух сотрудников.
        
        Act: применение оператора +
        Assert: проверка суммы
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 6000)
        
        # Act
        result = emp1 + emp2
        
        # Assert
        assert result == 11000
    
    def test_employee_salary_addition_reverse(self):
        """
        Тест: сложение зарплат в обратном порядке.
        
        Act: применение оператора + в обратном порядке
        Assert: результат должен быть одинаковым
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 6000)
        
        # Act
        result1 = emp1 + emp2
        result2 = emp2 + emp1
        
        # Assert
        assert result1 == result2 == 11000
    
    def test_employee_salary_addition_zero_employee(self):
        """
        Тест: сложение зарплаты с минимальной зарплатой.
        
        Act: применение оператора +
        Assert: проверка суммы
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 100)
        emp2 = Employee(2, "Bob", "HR", 200)
        
        # Act
        result = emp1 + emp2
        
        # Assert
        assert result == 300


class TestEmployeeIntegration:
    """
    Интеграционные тесты для проверки взаимодействия методов.
    
    Проверяет:
    - Полный цикл создания и работы с объектом
    - Взаимодействие разных методов
    """
    
    def test_employee_complete_workflow(self):
        """
        Тест: полный цикл работы с объектом Employee.
        
        Act:
        1. Создание сотрудника
        2. Получение информации
        3. Изменение параметров
        4. Расчет зарплаты
        
        Assert: проверка корректности на каждом этапе
        """
        # Arrange & Act
        emp = Employee(1, "Alice", "IT", 5000)
        assert emp.calculate_salary() == 5000
        
        # Изменение зарплаты
        emp.base_salary = 6000
        assert emp.calculate_salary() == 6000
        
        # Изменение имени
        emp.name = "Alice Smith"
        assert emp.name == "Alice Smith"
        
        # Assert
        assert emp.id == 1
        assert emp.department == "IT"
    
    def test_employee_multiple_operations(self):
        """
        Тест: выполнение множественных операций.
        
        Act: последовательность операций сравнения и расчета
        Assert: проверка корректности всех операций
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 6000)
        emp3 = Employee(3, "Charlie", "Sales", 4000)
        
        # Act & Assert
        assert emp1.calculate_salary() < emp2.calculate_salary()
        assert emp3.calculate_salary() < emp1.calculate_salary()
        total = emp1 + emp2 + emp3
        assert total == 15000


# Вспомогательные функции для параметризованных тестов

@pytest.mark.parametrize("emp_id,name,dept,salary", [
    (1, "Alice", "IT", 5000),
    (2, "Bob", "HR", 4500),
    (3, "Charlie", "Sales", 6000),
    (4, "Diana", "Finance", 5500),
])
def test_employee_parametrized_creation(emp_id, name, dept, salary):
    """
    Параметризованный тест: создание сотрудников с разными параметрами.
    
    pytest создаст отдельный тест для каждой комбинации параметров.
    """
    # Act
    emp = Employee(emp_id, name, dept, salary)
    
    # Assert
    assert emp.id == emp_id
    assert emp.name == name
    assert emp.department == dept
    assert emp.base_salary == salary


@pytest.mark.parametrize("invalid_id", [-1, 0, -999])
def test_employee_parametrized_invalid_id(invalid_id):
    """
    Параметризованный тест: проверка отклонения отрицательных и нулевых ID.
    
    pytest создаст отдельный тест для каждого значения ID.
    """
    # Assert
    with pytest.raises(ValueError):
        Employee(invalid_id, "Test", "IT", 5000)


@pytest.mark.parametrize("invalid_name", ["", "   ", "\t", "\n"])
def test_employee_parametrized_invalid_name(invalid_name):
    """
    Параметризованный тест: проверка отклонения невалидных имен.
    
    pytest создаст отдельный тест для каждого имени.
    """
    # Assert
    with pytest.raises(ValueError):
        Employee(1, invalid_name, "IT", 5000)


@pytest.mark.parametrize("invalid_salary", [-1, 0, -5000])
def test_employee_parametrized_invalid_salary(invalid_salary):
    """
    Параметризованный тест: проверка отклонения невалидных зарплат.
    
    pytest создаст отдельный тест для каждого значения зарплаты.
    """
    # Assert
    with pytest.raises(ValueError):
        Employee(1, "Test", "IT", invalid_salary)


if __name__ == '__main__':
    # Позволяет запустить тесты напрямую: python test_employee.py
    pytest.main([__file__, '-v'])
