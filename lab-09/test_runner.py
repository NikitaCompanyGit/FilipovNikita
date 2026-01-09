#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
                    COMPREHENSIVE TEST RUNNER
           Универсальный инструмент для запуска всех тестов проекта
                     v1.0 | 25.12.2025 | Production-Ready
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
import json

# Цветные выводы
class Colors:
    """ANSI цвета для терминала"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def disable():
        """Отключить цвета (для CI/CD)"""
        Colors.HEADER = ''
        Colors.OKBLUE = ''
        Colors.OKCYAN = ''
        Colors.OKGREEN = ''
        Colors.WARNING = ''
        Colors.FAIL = ''
        Colors.ENDC = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''


class TestRunner:
    """Главный test runner для всего проекта"""

    # Константы
    TEST_DIRS = [
        'examples'
    ]

    TEST_FILES = [
        'test_*.py'
    ]

    def __init__(self, project_root: Optional[str] = None, no_color: bool = False):
        """
        Инициализация runner'а

        Args:
            project_root: Корневая директория проекта (auto-detect по умолчанию)
            no_color: Отключить цветной вывод
        """
        if no_color:
            Colors.disable()

        self.project_root = Path(project_root or os.getcwd()).resolve()
        self.test_dir = self._find_test_dir()
        self.start_time = None
        self.results = {}

    def _find_test_dir(self) -> Path:
        """Найти директорию с тестами"""
        for test_dir in self.TEST_DIRS:
            path = self.project_root / test_dir
            if path.exists() and path.is_dir():
                return path

        # Если ничего не найдено, создать в корне
        return self.project_root / 'tests'

    def print_header(self):
        """Напечатать красивый заголовок"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "COMPREHENSIVE TEST RUNNER".center(78) + "║")
        print("║" + "Универсальный инструмент для тестирования проекта".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Colors.ENDC}\n")

    def print_section(self, title: str):
        """Напечатать заголовок секции"""
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}{'═' * 80}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKCYAN}▶ {title}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKCYAN}{'═' * 80}{Colors.ENDC}\n")

    def print_success(self, message: str):
        """Напечатать успешное сообщение"""
        print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

    def print_error(self, message: str):
        """Напечатать ошибку"""
        print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

    def print_warning(self, message: str):
        """Напечатать предупреждение"""
        print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")

    def print_info(self, message: str):
        """Напечатать информацию"""
        print(f"{Colors.OKBLUE}ℹ️  {message}{Colors.ENDC}")

    def find_tests(self) -> List[Path]:
        """Найти все тестовые файлы"""
        tests = []

        if not self.test_dir.exists():
            return tests

        for pattern in self.TEST_FILES:
            tests.extend(self.test_dir.glob(pattern))

        return sorted(set(tests))

    def run_all_tests(self, verbose: int = 1, coverage: bool = False,
                     parallel: bool = False, markers: Optional[str] = None) -> int:
        """
        Запустить все тесты

        Args:
            verbose: Уровень verbosity (0=quiet, 1=normal, 2=verbose, 3=very verbose)
            coverage: Включить анализ покрытия кода
            parallel: Использовать параллельное выполнение
            markers: Запустить тесты с конкретным маркером

        Returns:
            Код выхода pytest
        """
        self.print_header()
        self.print_section("ЗАПУСК ВСЕХ ТЕСТОВ")

        self.start_time = time.time()

        # Проверить что тесты существуют
        tests = self.find_tests()
        if not tests:
            self.print_error(f"Тесты не найдены в {self.test_dir}")
            return 1

        self.print_info(f"Найдено {len(tests)} тестовых файлов")
        for test in tests:
            self.print_info(f"  • {test.name}")

        # Построить команду pytest
        cmd = ['pytest']

        # Добавить путь к тестам
        cmd.append(str(self.test_dir))

        # Verbosity
        if verbose == 1:
            cmd.append('-v')
        elif verbose >= 2:
            cmd.append(f'-{"v" * verbose}')
        elif verbose == 0:
            cmd.append('-q')

        # Маркеры
        if markers:
            cmd.extend(['-m', markers])

        # Coverage
        if coverage:
            cmd.extend(['--cov=.', '--cov-report=html', '--cov-report=term'])

        # Параллельное выполнение
        if parallel:
            cmd.extend(['-n', 'auto'])

        # Дополнительные опции
        cmd.extend([
            '--tb=short',
            '--strict-markers',
            '-ra',  # Show summary of all test outcomes
        ])

        # Запустить тесты
        self.print_info(f"Команда: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, cwd=self.project_root)

        # Показать результаты
        elapsed = time.time() - self.start_time
        self._print_results(result.returncode, elapsed)

        return result.returncode

    def run_part(self, part: int, verbose: int = 1) -> int:
        """
        Запустить тесты конкретной части

        Args:
            part: Номер части (1-5)
            verbose: Уровень verbosity

        Returns:
            Код выхода pytest
        """
        if part < 1 or part > 5:
            self.print_error(f"Неверный номер части: {part}. Допустимо: 1-5")
            return 1

        self.print_header()
        self.print_section(f"ЗАПУСК ТЕСТОВ PART {part}")

        part_names = {
            1: "Инкапсуляция (Encapsulation)",
            2: "Наследование (Inheritance)",
            3: "Полиморфизм (Polymorphism)",
            4: "Композиция (Composition)",
            5: "Паттерны (Design Patterns)",
        }

        self.print_info(f"Тестирование: {part_names[part]}")

        self.start_time = time.time()

        cmd = [
            'pytest',
            str(self.test_dir / f'test_part{part}_*.py'),
            '-v' if verbose >= 1 else '-q',
            '--tb=short',
            '-ra',
        ]

        self.print_info(f"Команда: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, cwd=self.project_root)

        elapsed = time.time() - self.start_time
        self._print_results(result.returncode, elapsed)

        return result.returncode

    def run_unit_tests(self, verbose: int = 1) -> int:
        """Запустить только unit-тесты"""
        self.print_header()
        self.print_section("ЗАПУСК UNIT-ТЕСТОВ")

        self.start_time = time.time()

        cmd = [
            'pytest',
            str(self.test_dir),
            '-m', 'unit',
            '-v' if verbose >= 1 else '-q',
            '--tb=short',
            '-ra',
        ]

        self.print_info(f"Команда: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, cwd=self.project_root)

        elapsed = time.time() - self.start_time
        self._print_results(result.returncode, elapsed)

        return result.returncode

    def run_integration_tests(self, verbose: int = 1) -> int:
        """Запустить только интеграционные тесты"""
        self.print_header()
        self.print_section("ЗАПУСК ИНТЕГРАЦИОННЫХ ТЕСТОВ")

        self.start_time = time.time()

        cmd = [
            'pytest',
            str(self.test_dir),
            '-m', 'integration',
            '-v' if verbose >= 1 else '-q',
            '--tb=short',
            '-ra',
        ]

        self.print_info(f"Команда: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, cwd=self.project_root)

        elapsed = time.time() - self.start_time
        self._print_results(result.returncode, elapsed)

        return result.returncode

    def run_coverage(self, verbose: int = 1) -> int:
        """Запустить тесты с анализом покрытия кода"""
        self.print_header()
        self.print_section("АНАЛИЗ ПОКРЫТИЯ КОДА")

        self.start_time = time.time()

        cmd = [
            'pytest',
            str(self.test_dir),
            '--cov=.',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--cov-report=json',
            '-v' if verbose >= 1 else '-q',
            '--tb=short',
            '-ra',
        ]

        self.print_info(f"Команда: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, cwd=self.project_root)

        elapsed = time.time() - self.start_time

        if result.returncode == 0:
            self.print_success(f"Анализ покрытия завершен за {elapsed:.2f} сек")
            self.print_info("HTML отчет: htmlcov/index.html")
            self.print_info("JSON отчет: .coverage.json")
        else:
            self.print_error(f"Ошибка анализа покрытия")

        self._print_results(result.returncode, elapsed)

        return result.returncode

    def run_specific_test(self, test_path: str, verbose: int = 1) -> int:
        """
        Запустить конкретный тест

        Args:
            test_path: Путь к тесту (например: test_part1_*.py::TestClass::test_method)
            verbose: Уровень verbosity

        Returns:
            Код выхода pytest
        """
        self.print_header()
        self.print_section("ЗАПУСК КОНКРЕТНОГО ТЕСТА")

        self.print_info(f"Тест: {test_path}")

        self.start_time = time.time()

        cmd = [
            'pytest',
            test_path,
            '-vv' if verbose >= 2 else '-v',
            '--tb=long',
            '-s',  # Show output
            '-ra',
        ]

        self.print_info(f"Команда: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, cwd=self.project_root)

        elapsed = time.time() - self.start_time
        self._print_results(result.returncode, elapsed)

        return result.returncode

    def run_with_durations(self, verbose: int = 1, n_slowest: int = 10) -> int:
        """
        Запустить тесты с профилированием времени выполнения

        Args:
            verbose: Уровень verbosity
            n_slowest: Количество самых долгих тестов для показа

        Returns:
            Код выхода pytest
        """
        self.print_header()
        self.print_section("ЗАПУСК ТЕСТОВ С ПРОФИЛИРОВАНИЕМ")

        self.print_info(f"Будут показаны {n_slowest} самых долгих тестов")

        self.start_time = time.time()

        cmd = [
            'pytest',
            str(self.test_dir),
            f'--durations={n_slowest}',
            '-v' if verbose >= 1 else '-q',
            '--tb=short',
            '-ra',
        ]

        self.print_info(f"Команда: {' '.join(cmd)}\n")

        result = subprocess.run(cmd, cwd=self.project_root)

        elapsed = time.time() - self.start_time
        self._print_results(result.returncode, elapsed)

        return result.returncode

    def _print_results(self, return_code: int, elapsed: float):
        """Напечатать итоговые результаты"""
        print()
        print(f"{Colors.BOLD}{Colors.OKCYAN}{'═' * 80}{Colors.ENDC}")

        if return_code == 0:
            self.print_success(f"Все тесты пройдены за {elapsed:.2f} секунд!")
        else:
            self.print_error(f"Некоторые тесты провалены за {elapsed:.2f} секунд!")

        print(f"{Colors.BOLD}{Colors.OKCYAN}{'═' * 80}{Colors.ENDC}\n")

    def show_help(self):
        """Показать справку"""
        print(f"""
{Colors.BOLD}{Colors.HEADER}╔════════════════════════════════════════════════════════════════════════════╗
║                        COMPREHENSIVE TEST RUNNER                          ║
║                    Справка и примеры использования                        ║
╚════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.BOLD}ИСПОЛЬЗОВАНИЕ:{Colors.ENDC}
    python test_runner_comprehensive.py [КОМАНДА] [ОПЦИИ]

{Colors.BOLD}КОМАНДЫ:{Colors.ENDC}
    all                 Запустить все тесты (по умолчанию)
    part N              Запустить тесты части N (1-5)
    unit                Запустить только unit-тесты
    integration         Запустить только интеграционные тесты
    coverage            Запустить тесты с анализом покрытия
    test PATH           Запустить конкретный тест
    durations           Запустить тесты с профилированием времени
    help                Показать эту справку

{Colors.BOLD}ОПЦИИ:{Colors.ENDC}
    -v, --verbose       Увеличить verbosity (используйте несколько раз: -vvv)
    -q, --quiet         Тихий режим (no output)
    --parallel          Использовать параллельное выполнение
    --no-color          Отключить цветной вывод (для CI/CD)
    --root PATH         Указать корневую директорию проекта

{Colors.BOLD}ПРИМЕРЫ:{Colors.ENDC}

    # Запустить все тесты
    python test_runner_comprehensive.py all -v

    # Запустить тесты части 1 (Encapsulation)
    python test_runner_comprehensive.py part 1 -v

    # Запустить с анализом покрытия
    python test_runner_comprehensive.py coverage

    # Запустить конкретный тест
    python test_runner_comprehensive.py test tests/test_part1_*.py::TestClass::test_method

    # Запустить с профилированием (10 самых долгих тестов)
    python test_runner_comprehensive.py durations -v

    # Параллельное выполнение
    python test_runner_comprehensive.py all --parallel -v

    # Очень подробный вывод
    python test_runner_comprehensive.py all -vvv

{Colors.BOLD}ЧАСТИ ПРОЕКТА:{Colors.ENDC}
    Part 1  → Инкапсуляция (Encapsulation)
    Part 2  → Наследование (Inheritance)
    Part 3  → Полиморфизм (Polymorphism)
    Part 4  → Композиция (Composition)
    Part 5  → Паттерны проектирования (Design Patterns)

{Colors.BOLD}ТРЕБОВАНИЯ:{Colors.ENDC}
    pytest >= 7.0
    pytest-cov >= 3.0 (опционально, для coverage)
    pytest-xdist >= 2.0 (опционально, для параллельного выполнения)

    Установка:
    pip install pytest pytest-cov pytest-xdist

{Colors.BOLD}ДОПОЛНИТЕЛЬНО:{Colors.ENDC}
    • Тесты ищутся в папке 'tests/' автоматически
    • HTML отчет покрытия сохраняется в 'htmlcov/'
    • Результаты логируются с временем выполнения
    • Поддерживается CI/CD интеграция
""")


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description='Comprehensive Test Runner для проекта',
        add_help=False
    )

    parser.add_argument('command', nargs='?', default='all',
                       help='Команда для выполнения (all, part, unit, integration, coverage, test, durations, help)')
    parser.add_argument('argument', nargs='?', default=None,
                       help='Аргумент для команды (например, номер части или путь к тесту)')
    parser.add_argument('-v', '--verbose', action='count', default=1,
                       help='Увеличить verbosity (используйте несколько раз: -vvv)')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Тихий режим')
    parser.add_argument('--parallel', action='store_true',
                       help='Использовать параллельное выполнение')
    parser.add_argument('--no-color', action='store_true',
                       help='Отключить цветной вывод')
    parser.add_argument('--root', type=str, default=None,
                       help='Корневая директория проекта')

    args = parser.parse_args()

    # Инициализировать runner
    runner = TestRunner(project_root=args.root, no_color=args.no_color)

    # Определить уровень verbosity
    verbosity = 0 if args.quiet else args.verbose

    # Выполнить команду
    try:
        if args.command == 'help' or args.command == '-h' or args.command == '--help':
            runner.show_help()
            return 0

        elif args.command == 'all':
            return runner.run_all_tests(
                verbose=verbosity,
                coverage=False,
                parallel=args.parallel
            )

        elif args.command == 'part':
            if not args.argument or not args.argument.isdigit():
                runner.print_error("Укажите номер части: part 1")
                return 1
            return runner.run_part(int(args.argument), verbose=verbosity)

        elif args.command == 'unit':
            return runner.run_unit_tests(verbose=verbosity)

        elif args.command == 'integration':
            return runner.run_integration_tests(verbose=verbosity)

        elif args.command == 'coverage':
            return runner.run_coverage(verbose=verbosity)

        elif args.command == 'test':
            if not args.argument:
                runner.print_error("Укажите путь к тесту: test path/to/test.py::TestClass::test_method")
                return 1
            return runner.run_specific_test(args.argument, verbose=verbosity)

        elif args.command == 'durations':
            return runner.run_with_durations(verbose=verbosity, n_slowest=10)

        else:
            runner.print_error(f"Неизвестная команда: {args.command}")
            print("\nИспользуйте 'help' для справки:")
            print("  python test_runner_comprehensive.py help\n")
            return 1

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Выполнение прервано пользователем{Colors.ENDC}\n")
        return 130
    except Exception as e:
        runner.print_error(f"Ошибка: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
