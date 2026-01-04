#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ЛР№8: Часть 2 - Тестирование наследования и абстрактных классов
================================================================

Модуль содержит модульные тесты для иерархии классов сотрудников, проверяющие:
- Корректность наследования от AbstractEmployee
- Реализацию абстрактных методов в подклассах
- Полиморфное поведение при расчете зарплаты
- Работу фабрики сотрудников

Для запуска:
    pytest test_employees_hierarchy.py -v
"""

import pytest
import sys
import os

# Добавляем path для импорта из src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Импортируем классы для тестирования
try:
    from base.employee import Employee
    from base.abstract_employee import AbstractEmployee
    from specialists.manager import Manager
    from specialists.developer import Developer
    from specialists.salesperson import Salesperson
    from specialists.ordinary_employee import OrdinaryEmployee
except ImportError as e:
    pytest.skip(f"Cannot import classes: {e}", allow_module_level=True)


class TestAbstractEmployeeInstantiation:
    """
    Тесты для проверки, что AbstractEmployee - это абстрактный класс.
    
    Проверяет:
    - Нельзя создать экземпляр AbstractEmployee напрямую
    - Можно создать экземпляры подклассов
    """
    
    def test_cannot_instantiate_abstract_employee(self):
        """
        Тест: попытка создать экземпляр AbstractEmployee напрямую.
        
        Assert: ожидается исключение TypeError (не удается создать абстрактный класс)
        """
        # Assert
        with pytest.raises(TypeError):
            AbstractEmployee(1, "Test", "IT", 5000)
    
    def test_can_instantiate_concrete_employee_subclasses(self):
        """
        Тест: можно создать экземпляры конкретных подклассов.
        
        Act: создание экземпляров Manager, Developer, Salesperson
        Assert: все объекты создаются успешно
        """
        # Act
        manager = Manager(1, "Alice", "Management", 5000, 1000)
        developer = Developer(2, "Bob", "DEV", 5000, "middle", ["Python"])
        salesperson = Salesperson(3, "Charlie", "Sales", 4000, 0.15, 50000)
        
        # Assert
        assert isinstance(manager, AbstractEmployee)
        assert isinstance(developer, AbstractEmployee)
        assert isinstance(salesperson, AbstractEmployee)
    
    def test_subclasses_are_employees(self):
        """
        Тест: все подклассы являются экземплярами Employee.
        
        Act: создание подклассов
        Assert: все должны быть типом Employee
        """
        # Act
        manager = Manager(1, "Alice", "Management", 5000, 1000)
        developer = Developer(2, "Bob", "DEV", 5000, "middle", ["Python"])
        
        # Assert
        assert isinstance(manager, Employee)
        assert isinstance(developer, Employee)


class TestManagerClass:
    """
    Тесты для проверки корректной работы класса Manager.
    
    Проверяет:
    - Расчет зарплаты с бонусом
    - Информацию о бонусе в методе get_info
    - Валидацию данных бонуса
    """
    
    def test_manager_salary_calculation_with_bonus(self):
        """
        Тест: расчет зарплаты менеджера с бонусом.
        
        Arrange: создание менеджера с известной зарплатой и бонусом
        Act: расчет итоговой зарплаты
        Assert: результат должен быть base_salary + bonus
        """
        # Arrange
        manager = Manager(1, "Alice", "Management", 5000, 1000)
        
        # Act
        salary = manager.calculate_salary()
        
        # Assert
        assert salary == 6000  # 5000 + 1000
    
    def test_manager_salary_different_values(self):
        """
        Тест: расчет зарплаты для разных комбинаций base_salary и bonus.
        
        Параметризованные проверки разных значений.
        """
        # Arrange & Act & Assert
        test_cases = [
            (5000, 1000, 6000),  # base_salary, bonus, expected
            (4000, 500, 4500),
            (7000, 2000, 9000),
            (6000, 0, 6000),  # бонус равен нулю
        ]
        
        for base_salary, bonus, expected in test_cases:
            manager = Manager(1, "Test", "Management", base_salary, bonus)
            assert manager.calculate_salary() == expected
    
    def test_manager_get_info_includes_bonus(self):
        """
        Тест: метод get_info содержит информацию о бонусе.
        
        Act: получение информации о менеджере
        Assert: информация должна содержать данные о бонусе и итоговой зарплате
        """
        # Arrange
        manager = Manager(1, "Alice", "Management", 5000, 1000)
        
        # Act
        info = manager.get_info()
        
        # Assert
        assert "1000" in info or "бонус" in info.lower()
        assert "6000" in info or "зарплата" in info.lower()
    
    def test_manager_invalid_bonus_raises_error(self):
        """
        Тест: попытка создать менеджера с отрицательным бонусом.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Manager(1, "Alice", "Management", 5000, -1000)
    
    def test_manager_set_bonus_valid(self):
        """
        Тест: установка нового значения бонуса.
        
        Arrange: создание менеджера
        Act: изменение бонуса через сеттер
        Assert: проверка корректного обновления
        """
        # Arrange
        manager = Manager(1, "Alice", "Management", 5000, 1000)
        
        # Act
        manager.bonus = 1500
        
        # Assert
        assert manager.bonus == 1500
        assert manager.calculate_salary() == 6500


class TestDeveloperClass:
    """
    Тесты для проверки корректной работы класса Developer.
    
    Проверяет:
    - Расчет зарплаты в зависимости от уровня квалификации
    - Управление стеком технологий (добавление, удаление)
    - Информацию о технологиях в методе get_info
    - Валидацию уровня seniority
    """
    
    @pytest.mark.parametrize("seniority,multiplier,base_salary,expected", [
        ("junior", 1.0, 5000, 5000),
        ("middle", 1.5, 5000, 7500),
        ("senior", 2.0, 5000, 10000),
    ])
    def test_developer_salary_by_seniority_level(self, seniority, multiplier, base_salary, expected):
        """
        Тест: расчет зарплаты разработчика в зависимости от уровня.
        
        Параметризованный тест для junior, middle, senior.
        """
        # Arrange
        dev = Developer(1, "Bob", "DEV", base_salary, seniority, ["Python"])
        
        # Act
        salary = dev.calculate_salary()
        
        # Assert
        assert salary == expected
    
    def test_developer_add_skill(self):
        """
        Тест: добавление навыка к разработчику.
        
        Arrange: создание разработчика с одним навыком
        Act: добавление второго навыка
        Assert: навыки должны быть в списке
        """
        # Arrange
        dev = Developer(1, "Bob", "DEV", 5000, "middle", ["Python"])
        
        # Act
        dev.add_skill("Java")
        
        # Assert
        assert "Java" in dev.skills
        assert len(dev.skills) == 2
    
    def test_developer_remove_skill(self):
        """
        Тест: удаление навыка от разработчика.
        
        Arrange: создание разработчика с навыками
        Act: удаление одного навыка
        Assert: навык должен быть удален
        """
        # Arrange
        dev = Developer(1, "Bob", "DEV", 5000, "middle", ["Python", "Java"])
        
        # Act
        dev.remove_skill("Python")
        
        # Assert
        assert "Python" not in dev.skills
        assert "Java" in dev.skills
        assert len(dev.skills) == 1
    
    def test_developer_get_info_includes_technologies(self):
        """
        Тест: метод get_info содержит информацию о технологиях.
        
        Act: получение информации
        Assert: должны быть перечислены технологии
        """
        # Arrange
        dev = Developer(1, "Bob", "DEV", 5000, "senior", ["Python", "Go"])
        
        # Act
        info = dev.get_info()
        
        # Assert
        assert "Python" in info
        assert "Go" in info
        assert "senior" in info.lower()
    
    def test_developer_get_info_includes_salary(self):
        """
        Тест: метод get_info содержит информацию о зарплате.
        
        Act: получение информации
        Assert: зарплата должна быть рассчитана с учетом уровня
        """
        # Arrange
        dev = Developer(1, "Bob", "DEV", 5000, "senior", ["Python"])
        
        # Act
        info = dev.get_info()
        
        # Assert
        assert "10000" in info  # 5000 * 2.0 для senior
    
    def test_developer_invalid_seniority_raises_error(self):
        """
        Тест: попытка создать разработчика с невалидным уровнем.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Developer(1, "Bob", "DEV", 5000, "expert", ["Python"])


class TestSalespersonClass:
    """
    Тесты для проверки корректной работы класса Salesperson.
    
    Проверяет:
    - Расчет зарплаты с комиссией
    - Обновление объема продаж
    - Информацию о комиссии в методе get_info
    - Валидацию данных комиссии
    """
    
    def test_salesperson_salary_with_commission(self):
        """
        Тест: расчет зарплаты продавца с комиссией.
        
        Arrange: создание продавца с известными параметрами
        Act: расчет итоговой зарплаты
        Assert: результат должен быть base_salary + (sales * commission_rate)
        """
        # Arrange
        # commission_rate = 0.1 (10%), sales = 50000
        # salary = 4000 + (50000 * 0.1) = 4000 + 5000 = 9000
        salesperson = Salesperson(1, "Charlie", "Sales", 4000, 0.1, 50000)
        
        # Act
        salary = salesperson.calculate_salary()
        
        # Assert
        assert salary == 9000
    
    def test_salesperson_salary_different_commission_rates(self):
        """
        Тест: расчет зарплаты для разных коэффициентов комиссии.
        
        Параметризованные проверки разных значений.
        """
        # Arrange & Act & Assert
        test_cases = [
            (4000, 0.1, 50000, 9000),   # 4000 + 50000*0.1
            (4000, 0.15, 60000, 13000), # 4000 + 60000*0.15
            (5000, 0.2, 100000, 25000), # 5000 + 100000*0.2
        ]
        
        for base_salary, commission_rate, sales, expected in test_cases:
            salesperson = Salesperson(1, "Test", "Sales", base_salary, commission_rate, sales)
            assert salesperson.calculate_salary() == expected
    
    def test_salesperson_update_sales(self):
        """
        Тест: обновление объема продаж.
        
        Arrange: создание продавца
        Act: обновление объема продаж
        Assert: зарплата должна пересчитаться
        """
        # Arrange
        salesperson = Salesperson(1, "Charlie", "Sales", 4000, 0.1, 50000)
        
        # Act
        salesperson.sales_amount = 100000
        new_salary = salesperson.calculate_salary()
        
        # Assert
        assert new_salary == 14000  # 4000 + 100000*0.1
    
    def test_salesperson_get_info_includes_commission(self):
        """
        Тест: метод get_info содержит информацию о комиссии.
        
        Act: получение информации
        Assert: должны быть данные о комиссии и объеме продаж
        """
        # Arrange
        salesperson = Salesperson(1, "Charlie", "Sales", 4000, 0.15, 50000)
        
        # Act
        info = salesperson.get_info()
        
        # Assert
        assert "0.15" in info or "15" in info  # Процент комиссии
        assert "50000" in info  # Объем продаж
    
    def test_salesperson_invalid_commission_rate_raises_error(self):
        """
        Тест: попытка создать продавца с отрицательной комиссией.
        
        Assert: ожидается исключение ValueError
        """
        # Assert
        with pytest.raises(ValueError):
            Salesperson(1, "Charlie", "Sales", 4000, -0.1, 50000)


class TestOrdinaryEmployeeClass:
    """
    Тесты для проверки корректной работы класса OrdinaryEmployee.
    
    Проверяет:
    - Расчет зарплаты (равна базовой)
    - Информацию в методе get_info
    """
    
    def test_ordinary_employee_salary_calculation(self):
        """
        Тест: расчет зарплаты обычного сотрудника.
        
        Arrange: создание обычного сотрудника
        Act: расчет зарплаты
        Assert: результат должен быть равен базовой зарплате
        """
        # Arrange
        emp = OrdinaryEmployee(1, "Dave", "Support", 4000)
        
        # Act
        salary = emp.calculate_salary()
        
        # Assert
        assert salary == 4000
    
    def test_ordinary_employee_get_info(self):
        """
        Тест: метод get_info обычного сотрудника.
        
        Act: получение информации
        Assert: должна содержать базовую информацию
        """
        # Arrange
        emp = OrdinaryEmployee(1, "Dave", "Support", 4000)
        
        # Act
        info = emp.get_info()
        
        # Assert
        assert "Dave" in info
        assert "Support" in info
        assert "4000" in info


class TestPolymorphicBehavior:
    """
    Тесты для проверки полиморфного поведения при работе с разными типами сотрудников.
    
    Проверяет:
    - Правильный расчет зарплаты для разных типов в коллекции
    - Вызов правильной реализации методов
    """
    
    def test_polymorphic_salary_calculation(self):
        """
        Тест: полиморфный расчет зарплаты для разных типов.
        
        Arrange: коллекция разных типов сотрудников
        Act: расчет зарплаты для каждого
        Assert: каждый тип должен рассчитать зарплату по своей логике
        """
        # Arrange
        employees = [
            Manager(1, "Alice", "Management", 5000, 1000),
            Developer(2, "Bob", "DEV", 5000, "senior", ["Python"]),
            Salesperson(3, "Charlie", "Sales", 4000, 0.1, 50000),
            OrdinaryEmployee(4, "Dave", "Support", 4000),
        ]
        
        # Act
        salaries = [emp.calculate_salary() for emp in employees]
        
        # Assert
        assert salaries[0] == 6000   # Manager: 5000 + 1000
        assert salaries[1] == 10000  # Developer senior: 5000 * 2.0
        assert salaries[2] == 9000   # Salesperson: 4000 + 50000*0.1
        assert salaries[3] == 4000   # OrdinaryEmployee: 4000
    
    def test_polymorphic_collection_processing(self):
        """
        Тест: обработка коллекции разных типов сотрудников.
        
        Act: итерация по коллекции
        Assert: каждый тип должен обработаться правильно
        """
        # Arrange
        employees = [
            Manager(1, "Alice", "Management", 5000, 1000),
            Developer(2, "Bob", "DEV", 5000, "middle", ["Python"]),
            Salesperson(3, "Charlie", "Sales", 4000, 0.15, 60000),
        ]
        
        total_salary = 0
        
        # Act
        for emp in employees:
            total_salary += emp.calculate_salary()
        
        # Assert
        # 6000 + 7500 + 13000 = 26500
        assert total_salary == 26500


class TestEmployeeFactoryMethod:
    """
    Тесты для проверки фабрики сотрудников (если она реализована).
    
    Проверяет:
    - Создание разных типов сотрудников
    - Передача параметров
    - Обработка ошибок
    """
    
    def test_employee_factory_creates_manager(self):
        """
        Тест: фабрика создает Manager.
        
        Act: использование фабрики для создания Manager
        Assert: объект должен быть типом Manager
        """
        # Arrange
        from factory import EmployeeFactory
        factory = EmployeeFactory()
        
        # Act
        manager = factory.create_employee("manager", 1, "Alice", "Management", 5000, bonus=1000)
        
        # Assert
        assert isinstance(manager, Manager)
        assert manager.calculate_salary() == 6000
    
    def test_employee_factory_creates_developer(self):
        """
        Тест: фабрика создает Developer.
        
        Act: использование фабрики для создания Developer
        Assert: объект должен быть типом Developer
        """
        # Arrange
        from factory import EmployeeFactory
        factory = EmployeeFactory()
        
        # Act
        dev = factory.create_employee("developer", 2, "Bob", "DEV", 5000, 
                                     seniority="senior", skills=["Python"])
        
        # Assert
        assert isinstance(dev, Developer)
        assert dev.calculate_salary() == 10000


@pytest.mark.parametrize("emp_type,params,expected_class", [
    ("manager", {"id": 1, "name": "Alice", "dept": "Mgmt", "salary": 5000, "bonus": 1000}, Manager),
    ("developer", {"id": 2, "name": "Bob", "dept": "DEV", "salary": 5000, "seniority": "middle", "skills": ["Python"]}, Developer),
    ("salesperson", {"id": 3, "name": "Charlie", "dept": "Sales", "salary": 4000, "commission": 0.1, "sales": 50000}, Salesperson),
])
def test_create_different_employee_types_parametrized(emp_type, params, expected_class):
    """
    Параметризованный тест: создание разных типов сотрудников.
    
    pytest создаст отдельный тест для каждого типа.
    """
    # Act: создание в зависимости от типа
    if emp_type == "manager":
        emp = Manager(params["id"], params["name"], params["dept"], params["salary"], params["bonus"])
    elif emp_type == "developer":
        emp = Developer(params["id"], params["name"], params["dept"], params["salary"], 
                       params["seniority"], params["skills"])
    elif emp_type == "salesperson":
        emp = Salesperson(params["id"], params["name"], params["dept"], params["salary"],
                         params["commission"], params["sales"])
    
    # Assert
    assert isinstance(emp, expected_class)
    assert emp.id == params["id"]
    assert emp.name == params["name"]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
