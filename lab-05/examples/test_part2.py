from factory import EmployeeFactory
from specialists.developer import Developer
from specialists.salesperson import Salesperson
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestPart2:
    """
    ТЕСТОВЫЙ НАБОР ЧАСТИ 2: НАСЛЕДОВАНИЕ, ФАБРИКА, ПОЛИМОРФИЗМ
    
    Цель: Проверить иерархию классов и паттерн Factory Method.
    Основные аспекты проверки:
    1. Уникальная бизнес-логика расчета зарплат для разных ролей (Developer, Salesperson).
    2. Корректность создания объектов через фабрику.
    3. Полиморфное поведение методов (get_info).
    """

    @staticmethod
    def run():
        print("=== ЗАПУСК ТЕСТОВ ЧАСТИ 2 (НАСЛЕДОВАНИЕ И ФАБРИКА) ===")
        TestPart2.test_specialist_logic()
        TestPart2.test_factory_polymorphism()
        print("=== ТЕСТЫ ЧАСТИ 2 ЗАВЕРШЕНЫ ===\n")

    @staticmethod
    def test_specialist_logic():
        """Проверяет специфичную логику для конкретных классов-наследников."""
        print("   [2.1] Тест бизнес-логики специалистов...")
        try:
            # Developer: Проверка коэффициентов Seniority
            dev = Developer(1, "Dev", "IT", 1000, "junior")
            assert dev.calculate_salary() == 1000.0
            
            dev.seniority_level = "senior" # Коэффициент x2.0
            assert dev.calculate_salary() == 2000.0
            
            # Salesperson: Проверка комиссии
            sales = Salesperson(2, "Sale", "Sales", 1000, 0.1)
            sales.update_sales(5000) # Комиссия 10% от 5000 = 500
            assert sales.calculate_salary() == 1500.0
            
            print("      -> Логика начисления зарплат работает корректно.")
        except AssertionError:
            print("      -> ОШИБКА: Расчет зарплаты неверен.")
        except Exception as e:
            print(f"      -> ОШИБКА: {e}")

    @staticmethod
    def test_factory_polymorphism():
        """Проверяет создание разнородных объектов через единый интерфейс фабрики."""
        print("   [2.2] Тест фабрики и полиморфизма...")
        employees = []
        try:
            # Создаем менеджера и разработчика через фабрику
            employees.append(EmployeeFactory.create_employee('manager', 
                id=10, name="Big Boss", department="Mgmt", base_salary=100, bonus=50))
            employees.append(EmployeeFactory.create_employee('developer',
                id=11, name="Code Master", department="IT", base_salary=100, seniority="middle"))
            
            print("      -> Фабрика успешно инстанцировала объекты.")
            
            # Проверка полиморфизма: вызываем один метод get_info() для разных классов
            print("      -> Проверка вывода get_info() для разных типов...")
            for emp in employees:
                info = emp.get_info()
                # Простая эвристическая проверка формата строки
                if "Тип:" not in info or "Итоговая выплата:" not in info:
                    print("         -> ОШИБКА: get_info вернул некорректный формат строки.")
                    return
            print("      -> Полиморфизм работает корректно.")
            
        except ValueError as e:
            print(f"      -> ОШИБКА ФАБРИКИ: {e}")
