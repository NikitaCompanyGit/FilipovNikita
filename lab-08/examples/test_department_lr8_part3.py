#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ЛР№8: Часть 3 - Тестирование полиморфизма и магических методов
=============================================================

Модуль содержит комплексные тесты для проверки:
- Полиморфного поведения класса Department
- Магических методов (__eq__, __lt__, __add__)
- Магических методов итерации (__iter__, __len__, __contains__)
- Сериализации и десериализации
- Сортировки

Для запуска:
    pytest test_department.py -v
"""

import pytest
import sys
import os
import json
import tempfile

# Добавляем path для импорта из src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Импортируем классы для тестирования
try:
    from base.employee import Employee
    from specialists.manager import Manager
    from specialists.developer import Developer
    from specialists.salesperson import Salesperson
    from organization.department import Department
except ImportError as e:
    pytest.skip(f"Cannot import classes: {e}", allow_module_level=True)


class TestDepartmentEmployeeManagement:
    """
    Тесты для проверки управления сотрудниками в отделе.
    
    Проверяет:
    - Добавление сотрудников
    - Удаление сотрудников
    - Получение списка сотрудников
    - Поиск по ID
    """
    
    def test_department_add_employee(self):
        """
        Тест: добавление сотрудника в отдел.
        
        Arrange: создание отдела и сотрудника
        Act: добавление сотрудника в отдел
        Assert: сотрудник должен быть в отделе
        """
        # Arrange
        dept = Department("Development")
        emp = Employee(1, "Alice", "DEV", 5000)
        
        # Act
        dept.add_employee(emp)
        
        # Assert
        assert emp in dept.get_employees()
        assert len(dept.get_employees()) == 1
    
    def test_department_add_multiple_employees(self):
        """
        Тест: добавление нескольких сотрудников в отдел.
        
        Arrange: создание отдела и нескольких сотрудников
        Act: добавление всех сотрудников
        Assert: все должны быть в отделе
        """
        # Arrange
        dept = Department("Development")
        employees = [
            Employee(1, "Alice", "DEV", 5000),
            Employee(2, "Bob", "DEV", 6000),
            Employee(3, "Charlie", "DEV", 7000),
        ]
        
        # Act
        for emp in employees:
            dept.add_employee(emp)
        
        # Assert
        assert len(dept.get_employees()) == 3
        for emp in employees:
            assert emp in dept.get_employees()
    
    def test_department_remove_employee(self):
        """
        Тест: удаление сотрудника из отдела.
        
        Arrange: отдел с сотрудниками
        Act: удаление одного сотрудника
        Assert: сотрудник должен быть удален
        """
        # Arrange
        dept = Department("Development")
        emp1 = Employee(1, "Alice", "DEV", 5000)
        emp2 = Employee(2, "Bob", "DEV", 6000)
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        # Act
        dept.remove_employee(1)
        
        # Assert
        assert len(dept.get_employees()) == 1
        assert emp1 not in dept.get_employees()
        assert emp2 in dept.get_employees()
    
    def test_department_find_employee_by_id(self):
        """
        Тест: поиск сотрудника по ID.
        
        Arrange: отдел с сотрудниками
        Act: поиск конкретного сотрудника
        Assert: найденный сотрудник должен совпадать
        """
        # Arrange
        dept = Department("Development")
        emp1 = Employee(1, "Alice", "DEV", 5000)
        emp2 = Employee(2, "Bob", "DEV", 6000)
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        # Act
        found = dept.find_employee_by_id(2)
        
        # Assert
        assert found is not None
        assert found.name == "Bob"
        assert found.id == 2


class TestDepartmentPolymorphicBehavior:
    """
    Тесты для проверки полиморфного поведения при работе с разными типами сотрудников.
    
    Проверяет:
    - Расчет общей зарплаты для разных типов
    - Полиморфный вызов calculate_salary
    """
    
    def test_department_calculate_total_salary_polymorphic(self):
        """
        Тест: расчет общей зарплаты отдела (полиморфно).
        
        Arrange: отдел с разными типами сотрудников
        Act: расчет общей зарплаты
        Assert: результат должен быть суммой индивидуальных зарплат
        """
        # Arrange
        dept = Department("Development")
        manager = Manager(1, "Alice", "DEV", 5000, 1000)
        developer = Developer(2, "Bob", "DEV", 5000, "senior", ["Python"])
        dept.add_employee(manager)
        dept.add_employee(developer)
        
        # Act
        total = dept.calculate_total_salary()
        
        # Assert
        # Manager: 5000 + 1000 = 6000
        # Developer senior: 5000 * 2.0 = 10000
        # Total: 16000
        assert total == 16000
    
    def test_department_salary_calculation_complex_team(self):
        """
        Тест: расчет зарплаты сложной команды.
        
        Arrange: отдел с 4 разными типами сотрудников
        Act: расчет общей зарплаты
        Assert: проверка корректности суммирования
        """
        # Arrange
        dept = Department("Mixed")
        manager = Manager(1, "Alice", "Mgmt", 5000, 1000)
        dev_senior = Developer(2, "Bob", "Dev", 5000, "senior", ["Python"])
        dev_junior = Developer(3, "Charlie", "Dev", 5000, "junior", ["Python"])
        salesperson = Salesperson(4, "Diana", "Sales", 4000, 0.1, 50000)
        
        for emp in [manager, dev_senior, dev_junior, salesperson]:
            dept.add_employee(emp)
        
        # Act
        total = dept.calculate_total_salary()
        
        # Assert
        # Manager: 6000
        # Dev senior: 10000
        # Dev junior: 5000
        # Salesperson: 4000 + 50000*0.1 = 9000
        # Total: 30000
        assert total == 30000
    
    def test_department_get_employee_count_by_type(self):
        """
        Тест: получение количества сотрудников по типам.
        
        Arrange: отдел с разными типами
        Act: получение статистики
        Assert: проверка подсчета
        """
        # Arrange
        dept = Department("Mixed")
        dept.add_employee(Manager(1, "Alice", "Mgmt", 5000, 1000))
        dept.add_employee(Developer(2, "Bob", "Dev", 5000, "senior", ["Python"]))
        dept.add_employee(Developer(3, "Charlie", "Dev", 5000, "junior", ["Python"]))
        dept.add_employee(Salesperson(4, "Diana", "Sales", 4000, 0.1, 50000))
        
        # Act
        stats = dept.get_employee_count()
        
        # Assert
        assert stats.get("Manager", 0) == 1
        assert stats.get("Developer", 0) == 2
        assert stats.get("Salesperson", 0) == 1


class TestDepartmentMagicalMethods:
    """
    Тесты для проверки магических методов класса Department.
    
    Проверяет:
    - __len__: количество сотрудников
    - __getitem__: получение сотрудника по индексу
    - __contains__: проверка наличия сотрудника
    """
    
    def test_department_len_magic_method(self):
        """
        Тест: магический метод __len__.
        
        Arrange: отдел с сотрудниками
        Act: получение длины через len()
        Assert: результат должен быть количеством сотрудников
        """
        # Arrange
        dept = Department("Development")
        employees = [
            Employee(1, "Alice", "DEV", 5000),
            Employee(2, "Bob", "DEV", 6000),
            Employee(3, "Charlie", "DEV", 7000),
        ]
        for emp in employees:
            dept.add_employee(emp)
        
        # Act
        length = len(dept)
        
        # Assert
        assert length == 3
    
    def test_department_getitem_magic_method(self):
        """
        Тест: магический метод __getitem__.
        
        Arrange: отдел с сотрудниками
        Act: получение сотрудника по индексу
        Assert: должен вернуться правильный сотрудник
        """
        # Arrange
        dept = Department("Development")
        emp1 = Employee(1, "Alice", "DEV", 5000)
        emp2 = Employee(2, "Bob", "DEV", 6000)
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        # Act & Assert
        assert dept[0].name == "Alice"
        assert dept[1].name == "Bob"
    
    def test_department_contains_magic_method(self):
        """
        Тест: магический метод __contains__.
        
        Arrange: отдел с сотрудниками
        Act: проверка наличия сотрудника
        Assert: должна вернуться истина для присутствующего
        """
        # Arrange
        dept = Department("Development")
        emp = Employee(1, "Alice", "DEV", 5000)
        dept.add_employee(emp)
        
        # Act & Assert
        assert emp in dept
        
        other_emp = Employee(2, "Bob", "DEV", 6000)
        assert other_emp not in dept


class TestDepartmentIteration:
    """
    Тесты для проверки итерации по отделу.
    
    Проверяет:
    - Итерация через for loop
    - Использование list() для конвертации в список
    """
    
    def test_department_iteration(self):
        """
        Тест: итерация по сотрудникам отдела.
        
        Arrange: отдел с сотрудниками
        Act: итерация через for loop
        Assert: все сотрудники должны быть обработаны
        """
        # Arrange
        dept = Department("Development")
        employees = [
            Employee(1, "Alice", "DEV", 5000),
            Employee(2, "Bob", "DEV", 6000),
            Employee(3, "Charlie", "DEV", 7000),
        ]
        for emp in employees:
            dept.add_employee(emp)
        
        # Act
        count = 0
        for employee in dept:
            count += 1
            assert employee in employees
        
        # Assert
        assert count == 3
    
    def test_department_iteration_empty(self):
        """
        Тест: итерация по пустому отделу.
        
        Arrange: пустой отдел
        Act: попытка итерации
        Assert: цикл не должен выполниться
        """
        # Arrange
        dept = Department("Development")
        
        # Act
        count = 0
        for _ in dept:
            count += 1
        
        # Assert
        assert count == 0


class TestEmployeeMagicalMethods:
    """
    Тесты для проверки магических методов класса Employee.
    
    Проверяет:
    - __eq__: равенство по ID
    - __lt__: сравнение по зарплате
    - __add__: сложение зарплат
    """
    
    def test_employee_equality_by_id(self):
        """
        Тест: два сотрудника с одинаковым ID равны.
        
        Act: сравнение через __eq__
        Assert: должны быть равны
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(1, "Bob", "HR", 6000)
        
        # Act & Assert
        assert emp1 == emp2
    
    def test_employee_less_than_by_salary(self):
        """
        Тест: сравнение по зарплате через __lt__.
        
        Act: сравнение через <
        Assert: проверка корректности
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 6000)
        
        # Act & Assert
        assert emp1 < emp2
    
    def test_employee_addition_salary(self):
        """
        Тест: сложение зарплат через __add__.
        
        Act: применение оператора +
        Assert: результат должен быть суммой
        """
        # Arrange
        emp1 = Employee(1, "Alice", "IT", 5000)
        emp2 = Employee(2, "Bob", "HR", 6000)
        
        # Act
        total = emp1 + emp2
        
        # Assert
        assert total == 11000


class TestEmployeeSorting:
    """
    Тесты для проверки сортировки сотрудников.
    
    Проверяет:
    - Сортировка по ID (встроенная)
    - Сортировка по имени (через key)
    - Сортировка по зарплате (через key и операторы сравнения)
    """
    
    def test_employee_sorting_by_name(self):
        """
        Тест: сортировка сотрудников по имени.
        
        Arrange: несортированный список
        Act: сортировка по имени
        Assert: должны быть в алфавитном порядке
        """
        # Arrange
        employees = [
            Employee(3, "Charlie", "IT", 7000),
            Employee(1, "Alice", "HR", 5000),
            Employee(2, "Bob", "IT", 6000),
        ]
        
        # Act
        sorted_employees = sorted(employees, key=lambda x: x.name)
        
        # Assert
        assert sorted_employees[0].name == "Alice"
        assert sorted_employees[1].name == "Bob"
        assert sorted_employees[2].name == "Charlie"
    
    def test_employee_sorting_by_salary(self):
        """
        Тест: сортировка сотрудников по зарплате.
        
        Arrange: несортированный список
        Act: сортировка используя операторы сравнения
        Assert: должны быть в порядке возрастания зарплаты
        """
        # Arrange
        employees = [
            Employee(3, "Charlie", "IT", 7000),
            Employee(1, "Alice", "HR", 5000),
            Employee(2, "Bob", "IT", 6000),
        ]
        
        # Act
        sorted_employees = sorted(employees)
        
        # Assert
        assert sorted_employees[0].calculate_salary() == 5000
        assert sorted_employees[1].calculate_salary() == 6000
        assert sorted_employees[2].calculate_salary() == 7000
    
    def test_department_employees_statistics(self):
        """
        Тест: получение статистики по отделу.
        
        Arrange: отдел с сотрудниками
        Act: получение различных статистик
        Assert: все значения должны быть корректны
        """
        # Arrange
        dept = Department("Development")
        emp1 = Employee(1, "Alice", "DEV", 5000)
        emp2 = Employee(2, "Bob", "DEV", 6000)
        emp3 = Employee(3, "Charlie", "DEV", 4000)
        
        for emp in [emp1, emp2, emp3]:
            dept.add_employee(emp)
        
        # Act & Assert
        assert len(dept) == 3
        assert dept.calculate_total_salary() == 15000


class TestDepartmentSerialization:
    """
    Тесты для проверки сериализации отдела.
    
    Проверяет:
    - Сохранение отдела в JSON
    - Загрузку отдела из JSON
    - Полный цикл сохранения-загрузки
    """
    
    def test_department_serialization_roundtrip(self):
        """
        Тест: полный цикл сохранения и загрузки отдела.
        
        Arrange: создание отдела с сотрудниками
        Act: сохранение и загрузка
        Assert: загруженные данные должны совпадать с исходными
        """
        # Arrange
        dept = Department("Development")
        emp1 = Employee(1, "Alice", "DEV", 5000)
        emp2 = Employee(2, "Bob", "DEV", 6000)
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        # Act: сохранение в временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
            dept.save_to_file(filename)
        
        try:
            # Act: загрузка из файла
            loaded_dept = Department.load_from_file(filename)
            
            # Assert
            assert loaded_dept.name == "Development"
            assert len(loaded_dept) == 2
            assert loaded_dept.calculate_total_salary() == 11000
        finally:
            # Cleanup
            if os.path.exists(filename):
                os.remove(filename)


@pytest.mark.parametrize("emp_id,name,salary", [
    (1, "Alice", 5000),
    (2, "Bob", 6000),
    (3, "Charlie", 4000),
])
def test_department_add_parametrized(emp_id, name, salary):
    """
    Параметризованный тест: добавление различных сотрудников.
    
    pytest создаст отдельный тест для каждого набора параметров.
    """
    # Arrange
    dept = Department("Development")
    emp = Employee(emp_id, name, "DEV", salary)
    
    # Act
    dept.add_employee(emp)
    
    # Assert
    assert len(dept) == 1
    assert emp in dept


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
