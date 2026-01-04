#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ЛР№8: Главный файл запуска всех тестов
========================================

Этот файл позволяет запустить все тесты с красивым форматированием
и получить подробный отчет о результатах.

Использование:
    python run_all_tests.py          # Запустить все тесты
    python run_all_tests.py part1    # Запустить часть 1
    python run_all_tests.py part2    # Запустить часть 2
    python run_all_tests.py part3    # Запустить часть 3
    python run_all_tests.py coverage # Запустить с покрытием
    python run_all_tests.py help     # Справка
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(title: str) -> None:
    """
    Печать красивого заголовка.
    
    :param title: Текст заголовка
    """
    print(f"\n{'='*80}")
    print(f"  {title.center(76)}")
    print(f"{'='*80}\n")


def print_command(cmd: str) -> None:
    """
    Печать команды для выполнения.
    
    :param cmd: Команда
    """
    print(f"📋 Команда: {cmd}")
    print(f"{'─'*80}\n")


def run_command(cmd: list) -> int:
    """
    Выполнить команду и вернуть код возврата.
    
    :param cmd: Команда как список аргументов
    :return: Код возврата процесса
    """
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        return result.returncode
    except Exception as e:
        print(f"❌ Ошибка при выполнении команды: {e}")
        return 1


def run_all_tests() -> None:
    """
    Запустить все тесты.
    
    Запускает все части ЛР№8 последовательно.
    """
    print_header("ЛР№8: ЗАПУСК ВСЕХ ТЕСТОВ")
    
    # Определяем пути к тестовым файлам
    test_files = [
        "tests/test_employee_lr8_part1.py",
        "tests/test_employees_hierarchy_lr8_part2.py",
        "tests/test_department_lr8_part3.py",
    ]
    
    total_passed = 0
    total_failed = 0
    
    # Запускаем каждый файл
    for test_file in test_files:
        if Path(test_file).exists():
            print_header(f"Запуск: {test_file}")
            cmd = ["pytest", test_file, "-v", "--tb=short"]
            print_command(" ".join(cmd))
            return_code = run_command(cmd)
            
            if return_code != 0:
                total_failed += 1
            else:
                total_passed += 1
        else:
            print(f"⚠️  Файл не найден: {test_file}\n")
    
    # Итоги
    print_header("ИТОГИ ТЕСТИРОВАНИЯ")
    print(f"✅ Успешно: {total_passed} файлов")
    print(f"❌ Ошибок: {total_failed} файлов")
    print()


def run_part1() -> None:
    """
    Запустить тесты Части 1: Инкапсуляция.
    
    Тесты для класса Employee.
    """
    print_header("ЛР№8 - ЧАСТЬ 1: ТЕСТИРОВАНИЕ ИНКАПСУЛЯЦИИ")
    
    test_file = "tests/test_employee_lr8_part1.py"
    
    if not Path(test_file).exists():
        print(f"❌ Файл не найден: {test_file}")
        return
    
    cmd = ["pytest", test_file, "-v", "--tb=short"]
    print_command(" ".join(cmd))
    print("\nТесты в этой части:")
    print("  • Создание Employee с валидными данными")
    print("  • Валидация отрицательных значений")
    print("  • Тестирование сеттеров")
    print("  • Тестирование методов (calculate_salary, __str__)")
    print("  • Тестирование операций сравнения")
    print("  • Параметризованные тесты\n")
    
    run_command(cmd)


def run_part2() -> None:
    """
    Запустить тесты Части 2: Наследование.
    
    Тесты для иерархии классов сотрудников.
    """
    print_header("ЛР№8 - ЧАСТЬ 2: ТЕСТИРОВАНИЕ НАСЛЕДОВАНИЯ")
    
    test_file = "tests/test_employees_hierarchy_lr8_part2.py"
    
    if not Path(test_file).exists():
        print(f"❌ Файл не найден: {test_file}")
        return
    
    cmd = ["pytest", test_file, "-v", "--tb=short"]
    print_command(" ".join(cmd))
    print("\nТесты в этой части:")
    print("  • Проверка абстрактного класса AbstractEmployee")
    print("  • Тестирование класса Manager")
    print("  • Тестирование класса Developer")
    print("  • Тестирование класса Salesperson")
    print("  • Тестирование класса OrdinaryEmployee")
    print("  • Полиморфное поведение")
    print("  • Параметризованные тесты уровней сотрудников\n")
    
    run_command(cmd)


def run_part3() -> None:
    """
    Запустить тесты Части 3: Полиморфизм и магические методы.
    
    Тесты для Department и магических методов.
    """
    print_header("ЛР№8 - ЧАСТЬ 3: ТЕСТИРОВАНИЕ ПОЛИМОРФИЗМА")
    
    test_file = "tests/test_department_lr8_part3.py"
    
    if not Path(test_file).exists():
        print(f"❌ Файл не найден: {test_file}")
        return
    
    cmd = ["pytest", test_file, "-v", "--tb=short"]
    print_command(" ".join(cmd))
    print("\nТесты в этой части:")
    print("  • Управление сотрудниками в отделе")
    print("  • Полиморфный расчет зарплаты")
    print("  • Магические методы: __len__, __getitem__, __contains__")
    print("  • Итерация по отделу")
    print("  • Операции сравнения: __eq__, __lt__, __add__")
    print("  • Сортировка сотрудников")
    print("  • Сериализация и десериализация\n")
    
    run_command(cmd)


def run_with_coverage() -> None:
    """
    Запустить тесты с измерением покрытия кода.
    
    Требует pytest-cov.
    """
    print_header("ЛР№8: ТЕСТИРОВАНИЕ С ИЗМЕРЕНИЕМ ПОКРЫТИЯ КОДА")
    
    # Проверяем, что pytest-cov установлен
    try:
        import pytest_cov  # noqa
    except ImportError:
        print("❌ pytest-cov не установлен!")
        print("📦 Установите: pip install pytest-cov\n")
        return
    
    test_dir = "tests"
    src_dir = "src"
    
    if not Path(test_dir).exists():
        print(f"❌ Папка не найдена: {test_dir}")
        return
    
    cmd = [
        "pytest",
        test_dir,
        f"--cov={src_dir}",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v"
    ]
    
    print_command(" ".join(cmd))
    print("\nИзмеряется покрытие кода в:")
    print(f"  • Исходные файлы: {src_dir}/")
    print(f"  • Тестовые файлы: {test_dir}/")
    print("  • HTML отчет: htmlcov/index.html\n")
    
    run_command(cmd)
    
    print("\n✅ Отчет о покрытии создан: htmlcov/index.html")
    print("   Откройте его в браузере для детального анализа\n")


def print_help() -> None:
    """
    Показать справку.
    """
    print_header("СПРАВКА: ЗАПУСК ТЕСТОВ ЛР№8")
    
    help_text = """
КОМАНДЫ:
──────

  python run_all_tests.py all       Запустить все тесты (части 1-3)
  python run_all_tests.py part1     Запустить только Часть 1 (инкапсуляция)
  python run_all_tests.py part2     Запустить только Часть 2 (наследование)
  python run_all_tests.py part3     Запустить только Часть 3 (полиморфизм)
  python run_all_tests.py coverage  Запустить тесты с измерением покрытия
  python run_all_tests.py help      Показать эту справку

АЛЬТЕРНАТИВНЫЕ КОМАНДЫ (через pytest):
────────────────────────────────────

  pytest tests/ -v                           Все тесты с подробным выводом
  pytest tests/test_employee_lr8_part1.py    Только Часть 1
  pytest tests/test_department_lr8_part3.py  Только Часть 3
  pytest tests/test_*.py::TestClassName      Конкретный класс тестов
  pytest tests/ -k "test_name"               Тесты по имени
  pytest tests/ --tb=short                   Короткий вывод ошибок
  pytest tests/ --tb=long                    Полный вывод ошибок
  pytest tests/ -x                           Остановиться на первой ошибке
  pytest tests/ --maxfail=3                  Остановиться после 3 ошибок
  pytest tests/ -q                           Минимальный вывод
  pytest tests/ --co                         Показать список тестов

УСТАНОВКА ЗАВИСИМОСТЕЙ:
──────────────────────

  pip install pytest                  # Основной фреймворк
  pip install pytest-cov              # Для измерения покрытия
  pip install pytest-asyncio          # Для асинхронных тестов (опционально)
  pip install pytest-mock             # Для моков (опционально)

ФАЙЛЫ ТЕСТОВ:
─────────────

  ✅ tests/test_employee_lr8_part1.py
     - 35+ тестов для Employee
     - Инкапсуляция, валидация, методы

  ✅ tests/test_employees_hierarchy_lr8_part2.py
     - 30+ тестов для иерархии
     - Наследование, полиморфизм, фабрики

  ✅ tests/test_department_lr8_part3.py
     - 25+ тестов для Department
     - Магические методы, итерация, сортировка

ПРИМЕРЫ:
────────

  # Запустить все тесты Части 1
  python run_all_tests.py part1

  # Запустить только тесты создания Employee
  pytest tests/test_employee_lr8_part1.py::TestEmployeeCreation -v

  # Запустить с покрытием кода
  python run_all_tests.py coverage

  # Запустить один конкретный тест
  pytest tests/test_employee_lr8_part1.py::TestEmployeeCreation::test_employee_creation_valid_data -v

ИНФОРМАЦИЯ О ТЕСТАХ:
───────────────────

Часть 1: Инкапсуляция (test_employee_lr8_part1.py)
  • TestEmployeeCreation - создание объектов
  • TestEmployeeValidation - валидация данных
  • TestEmployeeSetters - проверка сеттеров
  • TestEmployeeMethods - тестирование методов
  • TestEmployeeEquality - операции сравнения
  • TestEmployeeSalaryComparison - сравнение зарплат
  • TestEmployeeSalaryAddition - сложение зарплат
  • TestEmployeeIntegration - интеграционные тесты

Часть 2: Наследование (test_employees_hierarchy_lr8_part2.py)
  • TestAbstractEmployeeInstantiation - абстрактный класс
  • TestManagerClass - менеджеры
  • TestDeveloperClass - разработчики
  • TestSalespersonClass - продавцы
  • TestOrdinaryEmployeeClass - обычные сотрудники
  • TestPolymorphicBehavior - полиморфизм
  • TestEmployeeFactoryMethod - фабрики

Часть 3: Полиморфизм (test_department_lr8_part3.py)
  • TestDepartmentEmployeeManagement - управление
  • TestDepartmentPolymorphicBehavior - полиморфизм
  • TestDepartmentMagicalMethods - магические методы
  • TestDepartmentIteration - итерация
  • TestEmployeeMagicalMethods - методы Employee
  • TestEmployeeSorting - сортировка
  • TestDepartmentSerialization - сериализация

РЕЗУЛЬТАТ:
─────────

✅ Успешный запуск = зелёный вывод с PASSED
❌ Ошибка = красный вывод с FAILED
⚠️  Пропущено = жёлтый вывод с SKIPPED

Статистика:
  • Всего тестов: 90+
  • Строк кода: 1500+
  • Классов: 22+
  • Полное комментирование
"""
    
    print(help_text)


def main() -> None:
    """
    Главная функция обработки команд.
    """
    if len(sys.argv) < 2:
        run_all_tests()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'all':
        run_all_tests()
    elif command == 'part1':
        run_part1()
    elif command == 'part2':
        run_part2()
    elif command == 'part3':
        run_part3()
    elif command == 'coverage':
        run_with_coverage()
    elif command == 'help':
        print_help()
    else:
        print(f"❌ Неизвестная команда: {command}")
        print("📖 Используйте 'python run_all_tests.py help' для справки")
        sys.exit(1)


if __name__ == '__main__':
    main()
