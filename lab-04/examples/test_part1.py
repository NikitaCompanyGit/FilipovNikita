from base.employee import Employee
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestPart1:
    """
    ТЕСТОВЫЙ НАБОР ЧАСТИ 1: ИНКАПСУЛЯЦИЯ И ВАЛИДАЦИЯ
    
    Цель: Проверить корректность реализации базового класса Employee.
    Основные аспекты проверки:
    1. Приватность атрибутов (доступ только через свойства).
    2. Корректность работы геттеров и сеттеров.
    3. Механизм валидации данных (выброс исключений при некорректном вводе).
    """

    @staticmethod
    def run():
        print("=== ЗАПУСК ТЕСТОВ ЧАСТИ 1 (ИНКАПСУЛЯЦИЯ) ===")
        TestPart1.test_valid_creation()
        TestPart1.test_validation_errors()
        print("=== ТЕСТЫ ЧАСТИ 1 ЗАВЕРШЕНЫ ===\n")

    @staticmethod
    def test_valid_creation():
        """Проверяет успешное создание объекта и обновление полей валидными данными."""
        print("   [1.1] Тест создания и обновления (Happy Path)...")
        try:
            emp = Employee(1, "Тест Юзер", "QA", 50000)
            
            # Проверка чтения данных (Getter)
            assert emp.name == "Тест Юзер"
            assert emp.base_salary == 50000
            
            # Проверка изменения данных (Setter)
            emp.base_salary = 60000
            assert emp.base_salary == 60000
            
            print("      -> Успешно.")
        except AssertionError:
            print("      -> ОШИБКА: Данные объекта не соответствуют ожидаемым.")
        except ValueError as e:
            print(f"      -> ОШИБКА ВАЛИДАЦИИ: {e}")

    @staticmethod
    def test_validation_errors():
        """Проверяет реакцию системы на некорректные данные (Negative Testing)."""
        print("   [1.2] Тест обработки ошибок валидации...")
        errors_caught = 0
        expected_errors = 3

        # Сценарий 1: Отрицательный ID
        try:
            Employee(-1, "Name", "Dept", 100)
        except ValueError:
            errors_caught += 1

        # Сценарий 2: Пустое имя
        try:
            Employee(1, "", "Dept", 100)
        except ValueError:
            errors_caught += 1

        # Сценарий 3: Отрицательная зарплата
        try:
            Employee(1, "Name", "Dept", -5000)
        except ValueError:
            errors_caught += 1

        if errors_caught == expected_errors:
            print(f"      -> Успешно перехвачено {errors_caught}/{expected_errors} некорректных операций.")
        else:
            print(f"      -> ОШИБКА: Ожидалось {expected_errors} исключений, получено {errors_caught}.")
