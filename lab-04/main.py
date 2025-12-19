import sys
import os

# Добавляем папки src и examples в путь поиска Python
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, os.path.join(project_root, 'examples'))

# Импорт тестов из папки examples
try:
    from test_part1 import TestPart1
    from test_part2 import TestPart2
    from test_part3 import TestPart3
    from test_part4 import TestPart4
except ImportError as e:
    print("КРИТИЧЕСКАЯ ОШИБКА ИМПОРТА!")
    print("Убедитесь, что:")
    print("  1. Папка 'examples' существует")
    print("  2. Все тестовые файлы на месте")
    print("  3. Файл examples/__init__.py существует")
    print(f"Детали: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("==========================================")
    print("   СИСТЕМА УЧЕТА СОТРУДНИКОВ: TEST RUNNER")
    print("==========================================\n")

    # Запуск всех тестов
    TestPart1.run()
    TestPart2.run()
    TestPart3.run()
    TestPart4.run()

    print("==========================================")
    print("   Все тестовые сценарии успешно выполнены.")
    print("==========================================")
