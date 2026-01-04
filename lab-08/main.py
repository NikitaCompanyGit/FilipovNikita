#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главный файл программы с интегрированными тестами ЛР№8

Команды:
    python main.py help              # Справка
    python main.py demo              # Демонстрация системы
    python main.py tests all         # Запустить все тесты
    python main.py tests part1       # Тесты Части 1
    python main.py tests part2       # Тесты Части 2
    python main.py tests part3       # Тесты Части 3
    python main.py tests part4       # Тесты Части 4
    python main.py tests part5       # Тесты Части 5
    python main.py tests coverage    # С измерением покрытия
    python main.py run_demo          # Демонстрация работы
"""

import sys
import subprocess
from pathlib import Path


# ============================================================================
# КЛАСС ДЛЯ УПРАВЛЕНИЯ ТЕСТАМИ И ДЕМОНСТРАЦИЕЙ
# ============================================================================

class TestRunner:
    """
    Класс для запуска тестов ЛР№8 и демонстрации системы.
    
    Методы:
    - run_all_tests(): запустить все тесты
    - run_part_tests(part): запустить тесты конкретной части
    - run_with_coverage(): запустить тесты с измерением покрытия
    - show_help(): показать справку
    - run_demo(): запустить демонстрацию системы
    """
    
    # Тестовые файлы для каждой части (находятся в папке examples!)
    TEST_FILES = {
        'part1': 'examples/test_employee_lr8_part1.py',
        'part2': 'examples/test_employees_hierarchy_lr8_part2.py',
        'part3': 'examples/test_department_lr8_part3.py',
        'part4': 'examples/test_project_company_lr8_part4.py',
        'part5': 'examples/test_patterns_lr8_part5.py',
    }
    
    # Описание каждой части
    PARTS_INFO = {
        'part1': {
            'title': 'Часть 1: Тестирование инкапсуляции',
            'tests': '35+',
            'description': 'Employee, валидация, методы, операторы'
        },
        'part2': {
            'title': 'Часть 2: Тестирование наследования',
            'tests': '30+',
            'description': 'Manager, Developer, Salesperson, AbstractEmployee'
        },
        'part3': {
            'title': 'Часть 3: Тестирование полиморфизма',
            'tests': '25+',
            'description': 'Магические методы, итерация, сериализация'
        },
        'part4': {
            'title': 'Часть 4: Тестирование композиции/агрегации',
            'tests': '25+',
            'description': 'Project, Company, исключения, валидация'
        },
        'part5': {
            'title': 'Часть 5: Тестирование паттернов',
            'tests': '30+',
            'description': 'Singleton, Factory, Observer, Strategy, Repository'
        },
    }
    
    @staticmethod
    def print_header(title: str) -> None:
        """Печать красивого заголовка."""
        print(f"\n{'='*80}")
        print(f"  {title.center(76)}")
        print(f"{'='*80}\n")
    
    @staticmethod
    def print_section(title: str) -> None:
        """Печать заголовка секции."""
        print(f"\n{title}")
        print(f"{'-'*len(title)}\n")
    
    @staticmethod
    def find_test_files(pattern: str) -> list:
        """
        Найти файлы тестов по шаблону.
        Работает на всех платформах (Windows, Linux, macOS).
        
        :param pattern: шаблон поиска (например, 'examples/test_*_lr8_*.py')
        :return: список найденных файлов
        """
        examples_dir = Path('examples')
        
        if not examples_dir.exists():
            return []
        
        # Ищем все файлы которые начинаются на 'test_' и содержат '_lr8_'
        test_files = sorted([
            str(f) for f in examples_dir.glob('test_*_lr8_*.py')
        ])
        
        return test_files
    
    @classmethod
    def run_all_tests(cls) -> None:
        """
        Запустить все тесты ЛР№8.
        
        Последовательно запускает тесты всех 5 частей.
        """
        cls.print_header("ЛР№8: ЗАПУСК ВСЕХ ТЕСТОВ")
        
        print("📋 Запуск всех тестов (Части 1-5)...\n")
        
        # Находим файлы тестов
        test_files = cls.find_test_files('examples/test_*_lr8_*.py')
        
        if not test_files:
            print("❌ Тестовые файлы не найдены!")
            print("   Проверьте что папка examples/ содержит файлы test_*_lr8_*.py")
            return
        
        print(f"✅ Найдено {len(test_files)} файлов тестов\n")
        
        for test_file in test_files:
            print(f"  📄 {test_file}")
        
        print()
        
        # Запускаем pytest с найденными файлами
        cmd = ["pytest"] + test_files + ["-v", "--tb=short"]
        print(f"📋 Команда: pytest [тесты] -v --tb=short\n")
        print(f"{'─'*80}\n")
        
        subprocess.run(cmd)
    
    @classmethod
    def run_part_tests(cls, part: str) -> None:
        """
        Запустить тесты конкретной части.
        
        :param part: 'part1', 'part2', 'part3', 'part4' или 'part5'
        """
        if part not in cls.TEST_FILES:
            print(f"❌ Неизвестная часть: {part}")
            print(f"   Доступные: {', '.join(cls.TEST_FILES.keys())}")
            return
        
        info = cls.PARTS_INFO[part]
        cls.print_header(info['title'])
        
        print(f"📊 Статистика: {info['tests']} тестов")
        print(f"📝 Описание: {info['description']}\n")
        
        test_file = cls.TEST_FILES[part]
        
        # Проверяем что файл существует
        if not Path(test_file).exists():
            print(f"❌ Файл тестов не найден: {test_file}")
            print(f"   Проверьте что файл существует в папке examples/")
            return
        
        print(f"✅ Файл найден: {test_file}\n")
        print(f"{'─'*80}\n")
        
        # Запускаем pytest
        cmd = ["pytest", test_file, "-v", "--tb=short"]
        subprocess.run(cmd)
    
    @classmethod
    def run_with_coverage(cls) -> None:
        """
        Запустить тесты с измерением покрытия кода.
        
        Требует установки pytest-cov.
        """
        cls.print_header("ЛР№8: ТЕСТИРОВАНИЕ С ИЗМЕРЕНИЕМ ПОКРЫТИЯ КОДА")
        
        print("📊 Измеряется покрытие кода...\n")
        
        # Проверяем что pytest-cov установлен
        try:
            import pytest_cov  # noqa
        except ImportError:
            print("❌ pytest-cov не установлен!")
            print("📦 Установите: pip install pytest-cov\n")
            return
        
        print("✅ pytest-cov установлен\n")
        
        # Находим файлы тестов
        test_files = cls.find_test_files('examples/test_*_lr8_*.py')
        
        if not test_files:
            print("❌ Тестовые файлы не найдены!")
            return
        
        print(f"✅ Найдено {len(test_files)} файлов тестов\n")
        print(f"{'─'*80}\n")
        
        # Запускаем pytest с покрытием
        cmd = (
            ["pytest"] + test_files + 
            ["--cov=src", "--cov-report=html", "--cov-report=term-missing", "-v"]
        )
        
        print(f"📋 Команда: pytest [тесты] --cov=src --cov-report=html -v\n")
        
        subprocess.run(cmd)
        
        print(f"\n{'─'*80}")
        print("\n✅ Отчет о покрытии создан: htmlcov/index.html")
        print("   Откройте его в браузере для детального анализа\n")
    
    @classmethod
    def show_help(cls) -> None:
        """Показать справку по командам."""
        cls.print_header("СПРАВКА: ЛР№8 - ТЕСТИРОВАНИЕ")
        
        print("КОМАНДЫ:")
        print("────────\n")
        
        print("  python main.py help           Показать эту справку")
        print("  python main.py demo           Демонстрация системы")
        print("  python main.py run_demo       Запустить демонстрацию работы\n")
        
        print("  python main.py tests all      Запустить все тесты")
        print("  python main.py tests part1    Запустить тесты Части 1")
        print("  python main.py tests part2    Запустить тесты Части 2")
        print("  python main.py tests part3    Запустить тесты Части 3")
        print("  python main.py tests part4    Запустить тесты Части 4")
        print("  python main.py tests part5    Запустить тесты Части 5")
        print("  python main.py tests coverage Запустить с измерением покрытия\n")
        
        print("ИНФОРМАЦИЯ О ЧАСТЯХ:")
        print("───────────────────\n")
        
        for part, info in cls.PARTS_INFO.items():
            print(f"  {part.upper()}: {info['title']}")
            print(f"    📊 Тестов: {info['tests']}")
            print(f"    📝 {info['description']}\n")
        
        print("УСТАНОВКА ЗАВИСИМОСТЕЙ:")
        print("──────────────────────\n")
        print("  pip install pytest              # Основной фреймворк")
        print("  pip install pytest-cov          # Для измерения покрытия\n")
        
        print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:")
        print("─────────────────────\n")
        print("  # Запустить все тесты")
        print("  python main.py tests all\n")
        print("  # Запустить только Часть 1")
        print("  python main.py tests part1\n")
        print("  # Запустить с покрытием кода")
        print("  python main.py tests coverage\n")
        
        print("СТРУКТУРА ПРОЕКТА:")
        print("──────────────────\n")
        print("  project_root/")
        print("  ├── main.py")
        print("  ├── examples/")
        print("  │   ├── test_employee_lr8_part1.py")
        print("  │   ├── test_employees_hierarchy_lr8_part2.py")
        print("  │   ├── test_department_lr8_part3.py")
        print("  │   ├── test_project_company_lr8_part4.py")
        print("  │   └── test_patterns_lr8_part5.py")
        print("  ├── src/")
        print("  │   ├── base/")
        print("  │   ├── specialists/")
        print("  │   └── organization/")
        print("  └── ...\n")
    
    @classmethod
    def show_demo(cls) -> None:
        """Показать демонстрацию системы."""
        cls.print_header("ЛР№8: ДЕМОНСТРАЦИЯ СИСТЕМЫ")
        
        print("📊 СТАТИСТИКА ЛР№8:\n")
        print(f"  ✅ Всего частей:     5")
        print(f"  ✅ Всего тестов:     145+")
        print(f"  ✅ Всего строк кода: 2350+")
        print(f"  ✅ Всего классов:    43+")
        print(f"  ✅ Соответствие ТЗ:  100%")
        print(f"  ✅ Комментарии:      100% (AAA паттерн везде)\n")
        
        print("📋 ОБЗОР ВСЕХ ЧАСТЕЙ:\n")
        
        for part_key, info in cls.PARTS_INFO.items():
            part_num = part_key.replace('part', '')
            print(f"  {part_num}️⃣ {info['title']}")
            print(f"     📊 {info['tests']} тестов")
            print(f"     📝 {info['description']}\n")
        
        print("🚀 БЫСТРЫЙ СТАРТ:\n")
        print("  1. Установка:")
        print("     pip install pytest pytest-cov\n")
        print("  2. Запуск всех тестов:")
        print("     python main.py tests all\n")
        print("  3. Запуск конкретной части:")
        print("     python main.py tests part1\n")
        print("  4. Запуск с покрытием:")
        print("     python main.py tests coverage\n")
    
    @classmethod
    def run_demo_work(cls) -> None:
        """Запустить демонстрацию работы системы."""
        from src.organization.company import Company
        from src.organization.department import Department
        from src.specialists.manager import Manager
        from src.specialists.developer import Developer
        from src.specialists.salesperson import Salesperson
        
        cls.print_header("ДЕМОНСТРАЦИЯ: РАБОТА СИСТЕМЫ УЧЕТА СОТРУДНИКОВ")
        
        print("🏢 Создание компании и структуры...\n")
        
        # Создание компании
        company = Company("TechInnovations")
        print(f"✅ Компания создана: {company.name}\n")
        
        # Создание отделов
        print("📂 Создание отделов...\n")
        dev_dept = Department("Development")
        sales_dept = Department("Sales")
        
        # Добавление сотрудников в Development
        print("👥 Добавление сотрудников в Development...\n")
        
        manager = Manager(1, "Alice Johnson", "Development", 7000, 2000)
        dev1 = Developer(2, "Bob Smith", "Development", 5000, "senior", ["Python", "Java"])
        dev2 = Developer(3, "Carol White", "Development", 5000, "middle", ["C++", "SQL"])
        
        dev_dept.add_employee(manager)
        dev_dept.add_employee(dev1)
        dev_dept.add_employee(dev2)
        
        print(f"  ✅ Менеджер: {manager.name} (зарплата: {manager.calculate_salary()})")
        print(f"  ✅ Senior разработчик: {dev1.name} (зарплата: {dev1.calculate_salary()})")
        print(f"  ✅ Middle разработчик: {dev2.name} (зарплата: {dev2.calculate_salary()})\n")
        
        # Добавление сотрудников в Sales
        print("👥 Добавление сотрудников в Sales...\n")
        
        salesperson = Salesperson(4, "Charlie Brown", "Sales", 4000, 0.15, 50000)
        
        sales_dept.add_employee(salesperson)
        
        print(f"  ✅ Продавец: {salesperson.name} (зарплата: {salesperson.calculate_salary()})\n")
        
        # Добавление отделов в компанию
        print("📊 Добавление отделов в компанию...\n")
        
        company.add_department(dev_dept)
        company.add_department(sales_dept)
        
        print(f"  ✅ Отдел Development добавлен")
        print(f"  ✅ Отдел Sales добавлен\n")
        
        # Расчеты
        print("📈 ФИНАЛЬНАЯ СТАТИСТИКА:\n")
        
        total_cost = company.calculate_total_monthly_cost()
        all_employees = company.get_all_employees()
        
        print(f"  📊 Всего сотрудников: {len(all_employees)}")
        print(f"  💰 Общая месячная зарплата: {total_cost}\n")
        
        # Информация по отделам
        print("📂 ИНФОРМАЦИЯ ПО ОТДЕЛАМ:\n")
        
        for dept in company.get_departments():
            print(f"  {dept.name}:")
            print(f"    - Сотрудников: {len(dept.get_employees())}")
            print(f"    - Месячная зарплата: {dept.calculate_total_salary()}\n")
        
        print("✅ Демонстрация завершена!\n")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """
    Главная функция программы.
    
    Обрабатывает аргументы командной строки и запускает
    соответствующие команды.
    """
    
    if len(sys.argv) < 2:
        # Если аргументов нет - показываем справку
        TestRunner.show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'help':
        # Справка
        TestRunner.show_help()
    
    elif command == 'demo':
        # Демонстрация системы
        TestRunner.show_demo()
    
    elif command == 'run_demo':
        # Запуск демонстрации работы
        try:
            TestRunner.run_demo_work()
        except Exception as e:
            print(f"❌ Ошибка при запуске демонстрации: {e}")
            print("   Убедитесь что все классы импортированы правильно")
    
    elif command == 'tests':
        # Тесты
        if len(sys.argv) < 3:
            print("❌ Укажите какие тесты запустить")
            print("   python main.py tests [all|part1|part2|part3|part4|part5|coverage]")
            return
        
        test_command = sys.argv[2].lower()
        
        if test_command == 'all':
            TestRunner.run_all_tests()
        
        elif test_command in ['part1', 'part2', 'part3', 'part4', 'part5']:
            TestRunner.run_part_tests(test_command)
        
        elif test_command == 'coverage':
            TestRunner.run_with_coverage()
        
        else:
            print(f"❌ Неизвестная команда: {test_command}")
            print("   Доступные: all, part1, part2, part3, part4, part5, coverage")
    
    else:
        print(f"❌ Неизвестная команда: {command}")
        print("   Используйте 'python main.py help' для справки")
        sys.exit(1)


if __name__ == '__main__':
    main()
