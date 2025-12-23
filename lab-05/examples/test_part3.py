import os
from organization.department import Department
from factory import EmployeeFactory
from specialists.developer import Developer
import utils.comparators as comps

class TestPart3:
    """
    ТЕСТОВЫЙ НАБОР ЧАСТИ 3: МАГИЧЕСКИЕ МЕТОДЫ И КОЛЛЕКЦИИ
    
    Цель: Проверить "питоничность" классов и работу с коллекциями.
    Основные аспекты проверки:
    1. Перегрузка операторов сравнения и арифметики (__eq__, __add__).
    2. Поведение класса Department как контейнера (len, in).
    3. Базовая сериализация в JSON.
    """

    @staticmethod
    def run():
        print("=== ЗАПУСК ТЕСТОВ ЧАСТИ 3 (ПОЛИМОРФИЗМ И МАГИЯ) ===")
        TestPart3.test_magic_methods()
        TestPart3.test_department_collection()
        TestPart3.test_sorting_and_iter()
        TestPart3.test_serialization()
        print("=== ТЕСТЫ ЧАСТИ 3 ЗАВЕРШЕНЫ ===\n")

    @staticmethod
    def test_magic_methods():
        """Проверяет перегрузку операторов сравнения и сложения."""
        print("   [3.1] Тест магических методов (__eq__, __lt__, __add__)...")
        e1 = EmployeeFactory.create_employee('employee', id=1, name="A", department="D", base_salary=100)
        e2 = EmployeeFactory.create_employee('employee', id=2, name="B", department="D", base_salary=200)
        
        # __eq__: Сравнение по ID
        assert e1 != e2 
        # __lt__: Сравнение по зарплате
        assert e1 < e2
        # __add__: Сложение зарплат
        assert (e1 + e2) == 300.0
        
        print("      -> Успешно.")

    @staticmethod
    def test_department_collection():
        """Проверяет методы контейнера для отдела."""
        print("   [3.2] Тест коллекции Department...")
        dept = Department("IT Heroes")
        dev = EmployeeFactory.create_employee('developer', id=10, name="Dev", department="IT", base_salary=100, seniority="middle")
        dept.add_employee(dev)
        
        # Проверка длины и вхождения
        assert len(dept) == 1
        assert dept.calculate_total_salary() == 150.0
        assert dev in dept
        
        print("      -> Успешно.")

    @staticmethod
    def test_sorting_and_iter():
        """Проверяет итераторы и кастомную сортировку."""
        print("   [3.3] Тест сортировки и итерации...")
        
        # Итерация по объекту Developer (перебор стека технологий)
        dev = Developer(1, "Dev", "IT", 100, "junior", ["Python", "SQL"])
        skills = list(dev) 
        assert "Python" in skills
        
        # Сортировка списка сотрудников
        e1 = EmployeeFactory.create_employee('employee', id=1, name="Zara", department="A", base_salary=500)
        e2 = EmployeeFactory.create_employee('employee', id=2, name="Anna", department="B", base_salary=100)
        
        # Используем компаратор из utils.comparators
        sorted_emps = sorted([e1, e2], key=comps.sort_by_name)
        assert sorted_emps[0].name == "Anna"
        
        print("      -> Успешно.")

    @staticmethod
    def test_serialization():
        """Проверяет сохранение отдела в JSON."""
        print("   [3.4] Тест сериализации (JSON)...")
        
        # Вычисляем путь к папке docs/json относительно текущего файла
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_file = os.path.join(base_dir, "docs", "json", "test_dept.json")
        
        dept = Department("Test Dept")
        dept.add_employee(EmployeeFactory.create_employee('employee', id=1, name="TestUser", department="QA", base_salary=50000))
        dept.add_employee(EmployeeFactory.create_employee('developer', id=2, name="PyDev", department="IT", base_salary=100000, seniority="senior", tech_stack=["Python"]))
        
        # Сохранение
        dept.save_to_file(target_file)
        
        if os.path.exists(target_file):
            print(f"      -> Файл успешно создан: {target_file}")
        else:
            print("      -> ОШИБКА: Файл не найден после сохранения.")
            return

        # Загрузка и проверка валидности
        loaded_dept = Department.load_from_file(target_file)
        assert len(loaded_dept) == 2
        assert loaded_dept.name == "Test Dept"
        
        print("      -> Восстановление данных прошло успешно.")
