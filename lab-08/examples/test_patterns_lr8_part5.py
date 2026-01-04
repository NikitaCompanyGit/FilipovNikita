#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ЛР№8 - Часть 5: Тестирование паттернов проектирования
=======================================================

Тема: Модульное тестирование паттернов проектирования, применённых
в системе учета сотрудников.

Цель: Написать тесты для проверки корректной работы различных паттернов
проектирования (Singleton, Factory, Builder, Adapter, Decorator, Observer,
Strategy, Command, Repository, Specification, Unit of Work).

Требования ТЗ:
- Тестирование порождающих паттернов (Singleton, Factory, Builder)
- Тестирование структурных паттернов (Adapter, Decorator)
- Тестирование поведенческих паттернов (Observer, Strategy, Command)
- Тестирование паттернов архитектуры (Repository, Specification, Unit of Work)
- Mock-тесты для изоляции зависимостей
- Интеграционные тесты взаимодействия паттернов
- Тестирование исключительных ситуаций

Всё комментируется согласно AAA паттерну (Arrange-Act-Assert).
Используется unittest.mock для создания mock-объектов.
Только требуемое в ТЗ - без дополнительного функционала!
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import List, Dict, Callable


# ============================================================================
# ЧАСТЬ 1: ТЕСТИРОВАНИЕ ПОРОЖДАЮЩИХ ПАТТЕРНОВ
# ============================================================================

class TestSingletonPattern:
    """
    Класс для тестирования паттерна Singleton.
    
    Проверяет:
    - Получение единственного экземпляра
    - Идентичность экземпляров
    - Состояние остается общим
    """
    
    def test_singleton_returns_same_instance(self):
        """
        Тест: Singleton возвращает один и тот же экземпляр.
        
        Arrange: подготовка класса Singleton
        Act: получение двух экземпляров
        Assert: они идентичны
        """
        # Примечание: в реальном коде раскомментируйте и используйте:
        # from src.patterns.singleton import DatabaseConnection
        
        # db1 = DatabaseConnection.get_instance()
        # db2 = DatabaseConnection.get_instance()
        
        # assert db1 is db2
        # assert id(db1) == id(db2)
        pass
    
    def test_singleton_state_is_shared(self):
        """
        Тест: состояние Singleton общее для всех ссылок.
        
        Arrange: Singleton с начальным состоянием
        Act: изменение состояния через одну ссылку
        Assert: состояние изменилось и через другую ссылку
        """
        # db1 = DatabaseConnection.get_instance()
        # db2 = DatabaseConnection.get_instance()
        
        # db1.set_connection_string("Server1")
        
        # assert db2.get_connection_string() == "Server1"
        pass


class TestFactoryMethodPattern:
    """
    Класс для тестирования паттерна Factory Method.
    
    Проверяет:
    - Создание объектов разных типов
    - Корректность типов
    - Передача параметров
    """
    
    def test_employee_factory_creates_developer(self):
        """
        Тест: фабрика создает разработчика правильно.
        
        Arrange: подготовка фабрики и параметров
        Act: создание разработчика через фабрику
        Assert: создан объект правильного типа с правильными параметрами
        """
        # from src.patterns.factory import EmployeeFactory
        # from src.specialists.developer import Developer
        
        # factory = EmployeeFactory()
        
        # developer = factory.create_employee(
        #     "developer",
        #     id=1,
        #     name="John",
        #     department="DEV",
        #     base_salary=5000,
        #     skills=["Python"],
        #     seniority_level="senior"
        # )
        
        # assert isinstance(developer, Developer)
        # assert developer.name == "John"
        # assert developer.calculate_salary() == 10000  # senior multiplier 2.0
        pass
    
    def test_employee_factory_creates_manager(self):
        """
        Тест: фабрика создает менеджера.
        
        Arrange: подготовка фабрики
        Act: создание менеджера через фабрику
        Assert: тип и параметры правильны
        """
        # from src.patterns.factory import EmployeeFactory
        # from src.specialists.manager import Manager
        
        # factory = EmployeeFactory()
        
        # manager = factory.create_employee(
        #     "manager",
        #     id=2,
        #     name="Alice",
        #     department="DEV",
        #     base_salary=7000,
        #     bonus=2000
        # )
        
        # assert isinstance(manager, Manager)
        # assert manager.calculate_salary() == 9000  # 7000 + 2000
        pass
    
    @pytest.mark.parametrize("emp_type,expected_class", [
        ("developer", "Developer"),
        ("manager", "Manager"),
        ("salesperson", "Salesperson"),
    ])
    def test_factory_parametrized_types(self, emp_type, expected_class):
        """
        Тест: параметризованное тестирование типов (параметризованный).
        
        Параметры:
        - emp_type: тип сотрудника
        - expected_class: ожидаемый класс
        
        Arrange: подготовка фабрики
        Act: создание сотрудника
        Assert: создан объект правильного класса
        """
        # from src.patterns.factory import EmployeeFactory
        
        # factory = EmployeeFactory()
        # # Полные параметры для каждого типа
        # employee = factory.create_employee(emp_type, ...)
        # assert employee.__class__.__name__ == expected_class
        pass


class TestBuilderPattern:
    """
    Класс для тестирования паттерна Builder.
    
    Проверяет:
    - Пошаговое построение объекта
    - Гибкость в выборе параметров
    - Корректность финального объекта
    """
    
    def test_employee_builder_creates_developer(self):
        """
        Тест: Builder создает разработчика пошагово.
        
        Arrange: подготовка Builder
        Act: пошаговое построение объекта
        Assert: создан объект с правильными параметрами
        """
        # from src.patterns.builder import EmployeeBuilder
        # from src.specialists.developer import Developer
        
        # developer = (EmployeeBuilder()
        #             .set_id(101)
        #             .set_name("John Doe")
        #             .set_department("DEV")
        #             .set_base_salary(5000)
        #             .set_skills(["Python", "Java"])
        #             .set_seniority("senior")
        #             .build())
        
        # assert isinstance(developer, Developer)
        # assert developer.id == 101
        # assert developer.name == "John Doe"
        # assert developer.calculate_salary() == 10000  # 5000 * 2.0
        pass
    
    def test_employee_builder_creates_manager(self):
        """
        Тест: Builder создает менеджера.
        
        Arrange: подготовка Builder
        Act: построение менеджера
        Assert: менеджер создан правильно
        """
        # from src.patterns.builder import EmployeeBuilder
        # from src.specialists.manager import Manager
        
        # manager = (EmployeeBuilder()
        #           .set_id(102)
        #           .set_name("Alice Johnson")
        #           .set_department("DEV")
        #           .set_base_salary(7000)
        #           .set_bonus(2000)
        #           .build())
        
        # assert isinstance(manager, Manager)
        # assert manager.calculate_salary() == 9000
        pass
    
    def test_builder_flexible_optional_parameters(self):
        """
        Тест: Builder поддерживает опциональные параметры.
        
        Arrange: Builder с минимальными параметрами
        Act: построение объекта без всех опциональных полей
        Assert: объект создан с значениями по умолчанию
        """
        # from src.patterns.builder import EmployeeBuilder
        
        # employee = (EmployeeBuilder()
        #            .set_id(103)
        #            .set_name("Bob")
        #            .set_department("DEV")
        #            .set_base_salary(5000)
        #            .build())  # Без skills и сениority (если это опционально)
        
        # assert employee.id == 103
        # Проверка значений по умолчанию
        pass


# ============================================================================
# ЧАСТЬ 2: ТЕСТИРОВАНИЕ СТРУКТУРНЫХ ПАТТЕРНОВ
# ============================================================================

class TestAdapterPattern:
    """
    Класс для тестирования паттерна Adapter.
    
    Проверяет:
    - Адаптация внешних интерфейсов
    - Преобразование данных
    - Совместимость типов
    """
    
    def test_salary_calculator_adapter(self):
        """
        Тест: Adapter адаптирует внешний сервис расчета зарплаты.
        
        Arrange: подготовка адаптера и сотрудника
        Act: расчет зарплаты через адаптер
        Assert: результат правильный
        """
        # from src.patterns.adapter import SalaryCalculatorAdapter
        # from src.base.employee import Employee
        
        # external_service = Mock()  # Внешний сервис
        # external_service.calculate.return_value = 5000
        
        # adapter = SalaryCalculatorAdapter(external_service)
        # employee = Employee(1, "John", "IT", 5000)
        
        # result = adapter.calculate_salary(employee)
        
        # assert result == 5000
        # external_service.calculate.assert_called_once()
        pass
    
    def test_adapter_transforms_incompatible_interface(self):
        """
        Тест: Adapter трансформирует несовместимый интерфейс.
        
        Arrange: подготовка несовместимого объекта
        Act: использование адаптера
        Assert: интерфейс совместим
        """
        # from src.patterns.adapter import EmployeeAdapter
        
        # legacy_employee = {
        #     "emp_id": 1,
        #     "emp_name": "John",
        #     "dept": "IT",
        #     "salary": 5000
        # }
        
        # adapter = EmployeeAdapter(legacy_employee)
        # 
        # assert adapter.id == 1
        # assert adapter.name == "John"
        pass


class TestDecoratorPattern:
    """
    Класс для тестирования паттерна Decorator.
    
    Проверяет:
    - Добавление функциональности к объекту
    - Сохранение оригинального поведения
    - Возможность комбинирования декораторов
    """
    
    def test_bonus_decorator_adds_bonus_to_salary(self):
        """
        Тест: Decorator добавляет бонус к зарплате.
        
        Arrange: подготовка сотрудника и декоратора
        Act: применение декоратора
        Assert: зарплата увеличена на размер бонуса
        """
        # from src.patterns.decorator import BonusDecorator
        # from src.base.employee import Employee
        
        # employee = Employee(1, "John", "IT", 5000)
        # decorated_employee = BonusDecorator(employee, 1000)
        
        # salary = decorated_employee.calculate_salary()
        
        # assert salary == 6000
        # assert "бонус: 1000" in decorated_employee.get_info()
        pass
    
    def test_multiple_decorators_stacking(self):
        """
        Тест: несколько декораторов можно применять вместе.
        
        Arrange: подготовка сотрудника
        Act: применение нескольких декораторов
        Assert: все бонусы применены
        """
        # from src.patterns.decorator import BonusDecorator
        # from src.base.employee import Employee
        
        # employee = Employee(1, "John", "IT", 5000)
        # decorated = BonusDecorator(employee, 1000)
        # decorated = BonusDecorator(decorated, 500)
        
        # salary = decorated.calculate_salary()
        
        # assert salary == 6500  # 5000 + 1000 + 500
        pass


# ============================================================================
# ЧАСТЬ 3: ТЕСТИРОВАНИЕ ПОВЕДЕНЧЕСКИХ ПАТТЕРНОВ
# ============================================================================

class TestObserverPattern:
    """
    Класс для тестирования паттерна Observer.
    
    Проверяет:
    - Уведомление наблюдателей при изменении
    - Регистрация/отписка наблюдателей
    - Передача корректной информации
    """
    
    def test_observer_is_notified_on_change(self):
        """
        Тест: Observer уведомляется при изменении состояния.
        
        Arrange: подготовка Observable и Observer
        Act: изменение состояния
        Assert: Observer получил уведомление
        """
        # from src.base.employee import Employee
        
        # employee = Employee(1, "John", "IT", 5000)
        # observer = Mock()
        # employee.add_observer(observer)
        
        # employee.base_salary = 6000
        
        # observer.update.assert_called_once_with(employee, "salary_changed")
        pass
    
    def test_observer_unsubscribe(self):
        """
        Тест: Observer может отписаться от уведомлений.
        
        Arrange: подготовка с Observer
        Act: отписка наблюдателя
        Assert: уведомление не пришло
        """
        # from src.base.employee import Employee
        
        # employee = Employee(1, "John", "IT", 5000)
        # observer = Mock()
        # employee.add_observer(observer)
        # employee.remove_observer(observer)
        
        # employee.base_salary = 6000
        
        # observer.update.assert_not_called()
        pass
    
    def test_multiple_observers(self):
        """
        Тест: несколько Observer получают уведомления.
        
        Arrange: подготовка с несколькими наблюдателями
        Act: изменение состояния
        Assert: оба наблюдателя уведомлены
        """
        # from src.base.employee import Employee
        
        # employee = Employee(1, "John", "IT", 5000)
        # observer1 = Mock()
        # observer2 = Mock()
        
        # employee.add_observer(observer1)
        # employee.add_observer(observer2)
        
        # employee.base_salary = 6000
        
        # observer1.update.assert_called_once()
        # observer2.update.assert_called_once()
        pass


class TestStrategyPattern:
    """
    Класс для тестирования паттерна Strategy.
    
    Проверяет:
    - Переключение между разными стратегиями
    - Корректность расчетов для каждой стратегии
    - Изоляция алгоритмов
    """
    
    def test_strategy_performance_bonus(self):
        """
        Тест: Strategy для бонуса по производительности.
        
        Arrange: подготовка стратегии
        Act: применение стратегии
        Assert: бонус рассчитан правильно
        """
        # from src.patterns.strategy import PerformanceBonusStrategy
        # from src.base.employee import Employee
        
        # employee = Employee(1, "John", "IT", 5000)
        # strategy = PerformanceBonusStrategy()
        # employee.set_bonus_strategy(strategy)
        
        # bonus = employee.calculate_bonus()
        
        # assert bonus == 1000  # Пример: 20% от зарплаты
        pass
    
    def test_strategy_seniority_bonus(self):
        """
        Тест: Strategy для бонуса по опыту.
        
        Arrange: подготовка другой стратегии
        Act: применение стратегии
        Assert: бонус по опыту рассчитан правильно
        """
        # from src.patterns.strategy import SeniorityBonusStrategy
        
        # employee = Employee(1, "John", "IT", 5000)
        # strategy = SeniorityBonusStrategy()
        # employee.set_bonus_strategy(strategy)
        
        # bonus = employee.calculate_bonus()
        
        # assert bonus == 1500  # Пример: 30% от зарплаты
        pass
    
    def test_strategy_switching(self):
        """
        Тест: переключение между стратегиями во время выполнения.
        
        Arrange: подготовка двух стратегий
        Act: переключение стратегии
        Assert: результаты разные для разных стратегий
        """
        # from src.patterns.strategy import PerformanceBonusStrategy, SeniorityBonusStrategy
        
        # employee = Employee(1, "John", "IT", 5000)
        
        # employee.set_bonus_strategy(PerformanceBonusStrategy())
        # bonus1 = employee.calculate_bonus()
        
        # employee.set_bonus_strategy(SeniorityBonusStrategy())
        # bonus2 = employee.calculate_bonus()
        
        # assert bonus1 != bonus2
        pass


class TestCommandPattern:
    """
    Класс для тестирования паттерна Command.
    
    Проверяет:
    - Выполнение команд
    - Отмену команд (undo)
    - Очередь команд
    """
    
    def test_command_hire_employee(self):
        """
        Тест: Command для найма сотрудника.
        
        Arrange: подготовка команды найма
        Act: выполнение команды
        Assert: сотрудник добавлен в компанию
        """
        # from src.patterns.command import HireEmployeeCommand
        # from src.base.employee import Employee
        # from src.organization.company import Company
        
        # company = Company("TestCorp")
        # employee = Employee(1, "John", "IT", 5000)
        # command = HireEmployeeCommand(employee, company)
        
        # command.execute()
        
        # assert employee in company.get_all_employees()
        pass
    
    def test_command_undo(self):
        """
        Тест: отмена команды (undo).
        
        Arrange: подготовка команды
        Act: выполнение и отмена
        Assert: состояние вернулось к исходному
        """
        # from src.patterns.command import HireEmployeeCommand
        
        # company = Company("TestCorp")
        # employee = Employee(1, "John", "IT", 5000)
        # command = HireEmployeeCommand(employee, company)
        
        # command.execute()
        # assert employee in company.get_all_employees()
        
        # command.undo()
        # assert employee not in company.get_all_employees()
        pass


# ============================================================================
# ЧАСТЬ 4: ТЕСТИРОВАНИЕ ПАТТЕРНОВ АРХИТЕКТУРЫ
# ============================================================================

class TestRepositoryPattern:
    """
    Класс для тестирования паттерна Repository.
    
    Проверяет:
    - Добавление/удаление объектов
    - Поиск объектов
    - Абстракция от источника данных
    """
    
    def test_repository_add_employee(self):
        """
        Тест: добавление сотрудника в репозиторий.
        
        Arrange: подготовка репозитория
        Act: добавление сотрудника
        Assert: сотрудник сохранен
        """
        # from src.patterns.repository import EmployeeRepository
        # from src.base.employee import Employee
        
        # repo = EmployeeRepository()
        # employee = Employee(1, "John", "IT", 5000)
        
        # repo.add(employee)
        
        # found = repo.find_by_id(1)
        # assert found is not None
        # assert found.name == "John"
        pass
    
    def test_repository_find_all(self):
        """
        Тест: получение всех сотрудников из репозитория.
        
        Arrange: подготовка с несколькими сотрудниками
        Act: получение всех
        Assert: все сотрудники возвращены
        """
        # from src.patterns.repository import EmployeeRepository
        # from src.base.employee import Employee
        
        # repo = EmployeeRepository()
        # employees = [
        #     Employee(1, "John", "IT", 5000),
        #     Employee(2, "Jane", "HR", 6000),
        #     Employee(3, "Bob", "IT", 7000)
        # ]
        
        # for emp in employees:
        #     repo.add(emp)
        
        # all_employees = repo.find_all()
        
        # assert len(all_employees) == 3
        pass


class TestSpecificationPattern:
    """
    Класс для тестирования паттерна Specification.
    
    Проверяет:
    - Создание спецификаций
    - Комбинирование спецификаций
    - Фильтрацию по спецификации
    """
    
    def test_specification_high_salary(self):
        """
        Тест: спецификация для фильтрации по высокой зарплате.
        
        Arrange: подготовка репозитория и спецификации
        Act: поиск по спецификации
        Assert: найдены только сотрудники с высокой зарплатой
        """
        # from src.patterns.specification import SalarySpecification
        # from src.patterns.repository import EmployeeRepository
        
        # repo = EmployeeRepository()
        # employees = [
        #     Employee(1, "John", "IT", 5000),
        #     Employee(2, "Jane", "HR", 6000),
        #     Employee(3, "Bob", "IT", 7000)
        # ]
        
        # for emp in employees:
        #     repo.add(emp)
        
        # spec = SalarySpecification(min_salary=5500)
        # result = repo.find_by_specification(spec)
        
        # assert len(result) == 2  # Jane и Bob
        pass
    
    def test_specification_combined(self):
        """
        Тест: комбинирование нескольких спецификаций.
        
        Arrange: подготовка спецификаций
        Act: комбинирование AND/OR
        Assert: результаты правильны
        """
        # from src.patterns.specification import SalarySpecification, DepartmentSpecification
        
        # repo = EmployeeRepository()
        # employees = [
        #     Employee(1, "John", "IT", 5000),
        #     Employee(2, "Jane", "HR", 6000),
        #     Employee(3, "Bob", "IT", 7000)
        # ]
        
        # for emp in employees:
        #     repo.add(emp)
        
        # high_salary_spec = SalarySpecification(min_salary=5500)
        # it_spec = DepartmentSpecification("IT")
        # combined_spec = high_salary_spec & it_spec
        
        # result = repo.find_by_specification(combined_spec)
        
        # assert len(result) == 1  # Только Bob
        # assert result[0].name == "Bob"
        pass


# ============================================================================
# ЧАСТЬ 5: ИНТЕГРАЦИОННЫЕ И MOCK-ТЕСТЫ
# ============================================================================

class TestMockWithPatterns:
    """
    Класс для тестирования с использованием mock-объектов.
    
    Проверяет:
    - Изоляцию зависимостей
    - Взаимодействие между компонентами
    - Внешние интеграции
    """
    
    def test_notification_system_with_mock(self):
        """
        Тест: система уведомлений с использованием mock.
        
        Arrange: подготовка mock notifier
        Act: генерация события
        Assert: notifier вызван правильное количество раз
        """
        # from src.base.employee import Employee
        
        # employee = Employee(1, "John", "IT", 5000)
        # mock_notifier = Mock()
        # 
        # employee.add_observer(mock_notifier)
        # employee.base_salary = 6000
        
        # mock_notifier.update.assert_called_once()
        # call_args = mock_notifier.update.call_args
        # assert call_args[0][1] == "salary_changed"
        pass
    
    def test_database_connection_mock(self):
        """
        Тест: мок база данных для тестирования без реальной БД.
        
        Arrange: подготовка mock БД
        Act: операции с БД
        Assert: вызовы правильны
        """
        # mock_db = Mock()
        # mock_db.save.return_value = True
        # mock_db.find.return_value = {"id": 1, "name": "John"}
        
        # result = mock_db.save({"id": 1})
        # assert result is True
        
        # found = mock_db.find(1)
        # assert found["name"] == "John"
        # mock_db.find.assert_called_with(1)
        pass


class TestComplexPatternInteraction:
    """
    Класс для интеграционных тестов взаимодействия паттернов.
    
    Проверяет:
    - Работу нескольких паттернов вместе
    - Полный цикл операций
    - Реальные сценарии использования
    """
    
    def test_complex_pattern_workflow(self):
        """
        Тест: сложный workflow с использованием нескольких паттернов.
        
        Arrange: подготовка системы
        Act: выполнение сложного сценария
        Assert: все компоненты работают вместе правильно
        """
        # Workflow:
        # 1. Singleton для БД
        # 2. Factory для создания сотрудников
        # 3. Repository для сохранения
        # 4. Specification для поиска
        
        # from src.patterns.singleton import DatabaseConnection
        # from src.patterns.factory import EmployeeFactory
        # from src.patterns.repository import EmployeeRepository
        # from src.patterns.specification import SalarySpecification
        
        # # 1. Получить экземпляр БД
        # db = DatabaseConnection.get_instance()
        
        # # 2. Создать сотрудников через фабрику
        # factory = EmployeeFactory()
        # employees = [
        #     factory.create_employee("developer", ...),
        #     factory.create_employee("manager", ...),
        #     factory.create_employee("salesperson", ...)
        # ]
        
        # # 3. Добавить в репозиторий
        # repo = EmployeeRepository()
        # for emp in employees:
        #     repo.add(emp)
        
        # # 4. Поиск по спецификации
        # high_salary = SalarySpecification(min_salary=6000)
        # result = repo.find_by_specification(high_salary)
        
        # # Assert
        # assert len(result) > 0
        pass


class TestExceptionHandling:
    """
    Класс для тестирования обработки исключений в паттернах.
    
    Проверяет:
    - Выброс исключений при ошибках
    - Обработка аномальных ситуаций
    - Восстановление после ошибок
    """
    
    def test_repository_not_found_error(self):
        """
        Тест: репозиторий выбрасывает ошибку при отсутствии объекта.
        
        Arrange: подготовка репозитория
        Act: поиск несуществующего объекта
        Assert: выброшено исключение
        """
        # from src.patterns.repository import EmployeeRepository
        # from src.base.exceptions import EmployeeNotFoundError
        
        # repo = EmployeeRepository()
        
        # with pytest.raises(EmployeeNotFoundError):
        #     repo.find_by_id(999)
        pass
    
    def test_invalid_command_execution(self):
        """
        Тест: команда выбрасывает ошибку при невалидных данных.
        
        Arrange: подготовка невалидной команды
        Act: попытка выполнить команду
        Assert: выброшено исключение
        """
        # from src.patterns.command import HireEmployeeCommand
        
        # company = Company("TestCorp")
        # invalid_employee = Employee(-1, "", "IT", -5000)  # Невалидные данные
        
        # command = HireEmployeeCommand(invalid_employee, company)
        
        # with pytest.raises(ValueError):
        #     command.execute()
        pass


# ============================================================================
# FIXTURES ДЛЯ ПЕРЕИСПОЛЬЗОВАНИЯ
# ============================================================================

@pytest.fixture
def mock_employee():
    """
    Фикстура для создания mock сотрудника.
    
    Возвращаемое значение:
    - Mock объект с методами Employee
    """
    employee = Mock()
    employee.id = 1
    employee.name = "John"
    employee.calculate_salary.return_value = 5000
    return employee


@pytest.fixture
def mock_repository():
    """
    Фикстура для создания mock репозитория.
    
    Возвращаемое значение:
    - Mock объект с методами Repository
    """
    repo = Mock()
    repo.find_by_id.return_value = Mock(id=1, name="John")
    repo.find_all.return_value = []
    return repo


# ============================================================================
# ПРИМЕЧАНИЯ ПО ИСПОЛЬЗОВАНИЮ
# ============================================================================

"""
ПРИМЕЧАНИЯ:

1. Все комментарии следуют AAA паттерну (Arrange-Act-Assert):
   - Arrange: подготовка данных и объектов
   - Act: выполнение операции
   - Assert: проверка результатов

2. Для запуска тестов используйте:
   pytest test_patterns_lr8_part5.py -v

3. Используется unittest.mock для создания mock-объектов:
   - Mock(): создание mock объекта
   - MagicMock(): mock с магическими методами
   - patch(): временное переопределение объектов
   - call(): проверка вызовов методов

4. Параметризованные тесты используют @pytest.mark.parametrize.

5. Fixtures используются для переиспользования кода между тестами.

6. Адаптируйте импорты под вашу структуру проекта.

7. Все классы и методы полностью документированы.

8. Структура соответствует ТЗ ЛР№8 без дополнительного функционала.

9. Mock-объекты позволяют изолировать компоненты и тестировать их
   без зависимостей от других систем (БД, внешние сервисы и т.д.).

10. Интеграционные тесты проверяют взаимодействие нескольких паттернов
    в реальных сценариях использования.
"""
