"""
test_runner_comprehensive.py - Главный тестовый runner

Этот файл содержит:
- Запуск всех категорий тестов
- Сборку отчетов о покрытии кода
- Форматированный вывод результатов
- Интеграцию с pytest

ИСПОЛЬЗОВАНИЕ:
    python test_runner_comprehensive.py        # Все тесты
    python test_runner_comprehensive.py part1  # Только Part 1
    pytest tests/ -v                           # Через pytest напрямую
    pytest tests/ --cov=src --cov-report=html  # С покрытием кода
"""

import subprocess
import sys
import glob
from pathlib import Path
from typing import List


class TestRunner:
    """Запускает тесты и генерирует отчеты"""

    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.tests_dir = self.project_root / "tests"
        self.src_dir = self.project_root / "src"
        # Используем текущий интерпретатор для запуска pytest
        self.pytest_cmd = [sys.executable, "-m", "pytest"]

    def print_header(self, text: str):
        """Красивый заголовок"""
        print("\n" + "═" * 70)
        print(f"  {text}")
        print("═" * 70 + "\n")

    def _find_test_files(self, pattern: str) -> List[str]:
        """Находит файлы тестов по паттерну"""
        # pathlib glob возвращает генератор путей
        files = list(self.tests_dir.glob(pattern))
        return [str(f) for f in files]

    def run_all_tests(self, verbose: bool = True, coverage: bool = False):
        """Запустить все тесты"""
        self.print_header("ЗАПУСК ПОЛНОГО НАБОРА ТЕСТОВ")

        cmd = self.pytest_cmd + [str(self.tests_dir), "-v" if verbose else "-q"]

        if coverage:
            cmd.extend([f"--cov={self.src_dir}", "--cov-report=html"])

        result = subprocess.run(cmd, cwd=self.project_root)
        return result.returncode == 0

    def run_part_tests(self, part: int, verbose: bool = True):
        """Запустить тесты определённой части"""
        self.print_header(f"ЗАПУСК ТЕСТОВ PART {part}")

        # Исправлено: ищем реальные файлы вместо передачи wildcard в subprocess
        pattern = f"test_part{part}_*.py"
        test_files = self._find_test_files(pattern)

        if not test_files:
            print(f"❌ Файлы для части {part} не найдены по шаблону {pattern}")
            return False

        cmd = self.pytest_cmd + test_files + ["-v" if verbose else "-q", f"-m=part{part}"]

        result = subprocess.run(cmd, cwd=self.project_root)
        return result.returncode == 0

    def run_integration_tests(self, verbose: bool = True):
        """Запустить интеграционные тесты"""
        self.print_header("ЗАПУСК ИНТЕГРАЦИОННЫХ ТЕСТОВ")

        # Ищем файл интеграционных тестов (может быть несколько или с суффиксами)
        test_files = self._find_test_files("test_integration*.py")

        if not test_files:
            # Fallback: пробуем искать просто по имени, если глоб не сработал
            default_file = self.tests_dir / "test_integration.py"
            if default_file.exists():
                test_files = [str(default_file)]
            else:
                print("❌ Файлы интеграционных тестов не найдены")
                return False

        cmd = self.pytest_cmd + test_files + ["-v" if verbose else "-q", "-m=integration"]

        result = subprocess.run(cmd, cwd=self.project_root)
        return result.returncode == 0

    def generate_coverage_report(self):
        """Сгенерировать отчет о покрытии кода"""
        self.print_header("ГЕНЕРАЦИЯ ОТЧЕТА О ПОКРЫТИИ КОДА")

        cmd = self.pytest_cmd + [
            str(self.tests_dir),
            f"--cov={self.src_dir}",
            "--cov-report=html",
            "--cov-report=term-missing",
            "-q"
        ]

        subprocess.run(cmd, cwd=self.project_root)

        html_report = self.project_root / "htmlcov" / "index.html"
        if html_report.exists():
            print(f"✅ Отчет сгенерирован: {html_report}")
        else:
            print("❌ Ошибка при генерации отчета")

    def show_statistics(self):
        """Показать статистику тестов"""
        self.print_header("СТАТИСТИКА ТЕСТИРОВАНИЯ")

        stats = {
            "Part 1 (Инкапсуляция)": self._count_tests_in_file("test_part1"),
            "Part 2 (Наследование)": self._count_tests_in_file("test_part2"),
            "Part 3 (Полиморфизм)": self._count_tests_in_file("test_part3"),
            "Part 4 (Композиция)": self._count_tests_in_file("test_part4"),
            "Part 5 (Паттерны)": self._count_tests_in_file("test_part5"),
            "Интеграционные": self._count_tests_in_file("test_integration"),
            "Граничные случаи": self._count_tests_in_file("test_edge_cases"),
        }

        total_tests = sum(stats.values())

        for name, count in stats.items():
            print(f"  {name:.<40} {count:>3} тестов")

        print(f"  {'ИТОГО':.<40} {total_tests:>3} тестов ✅")

    def _count_tests_in_file(self, pattern: str) -> int:
        """Подсчитать тесты в файле"""
        test_files = list(self.tests_dir.glob(f"{pattern}*.py"))

        count = 0
        for test_file in test_files:
            try:
                # Добавлена кодировка utf-8 для надежности
                with open(test_file, encoding='utf-8') as f:
                    count += f.read().count("def test_")
            except Exception as e:
                print(f"⚠️ Ошибка чтения {test_file.name}: {e}")

        return count


def main():
    """Главная функция"""
    runner = TestRunner()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "all":
            runner.show_statistics()
            success = runner.run_all_tests(coverage=True)

        elif command == "part":
            if len(sys.argv) > 2:
                try:
                    part = int(sys.argv[2])
                    success = runner.run_part_tests(part)
                except ValueError:
                    print("❌ Номер части должен быть числом")
                    return 1
            else:
                print("❌ Укажите номер части: python test_runner_comprehensive.py part 1")
                return 1

        elif command == "integration":
            success = runner.run_integration_tests()

        elif command == "coverage":
            runner.generate_coverage_report()
            success = True

        elif command == "stats":
            runner.show_statistics()
            success = True

        elif command == "help":
            print_help()
            success = True

        else:
            print(f"❌ Неизвестная команда: {command}")
            print_help()
            return 1

    else:
        # По умолчанию: все тесты с покрытием
        runner.show_statistics()
        success = runner.run_all_tests(coverage=True)
        if success:
            runner.generate_coverage_report()

    return 0 if success else 1


def print_help():
    """Справка по командам"""
    print("""
╔════════════════════════════════════════════════════════════╗
║           COMPREHENSIVE TEST RUNNER - СПРАВКА              ║
╚════════════════════════════════════════════════════════════╝

КОМАНДЫ:

  python test_runner_comprehensive.py all
      Запустить все тесты с покрытием кода

  python test_runner_comprehensive.py part 1
      Запустить тесты Part 1 (Инкапсуляция)

  python test_runner_comprehensive.py part 2
      Запустить тесты Part 2 (Наследование)

  python test_runner_comprehensive.py integration
      Запустить интеграционные тесты

  python test_runner_comprehensive.py coverage
      Сгенерировать отчет о покрытии кода (HTML)

  python test_runner_comprehensive.py stats
      Показать статистику тестов

  python test_runner_comprehensive.py help
      Показать эту справку

АЛЬТЕРНАТИВНЫЕ КОМАНДЫ (pytest):

  pytest tests/ -v
      Запустить все тесты с verbose выводом

  pytest tests/ --cov=src --cov-report=html
      Все тесты с подробным отчетом о покрытии

  pytest tests/test_part1_encapsulation.py -v
      Запустить конкретный тестовый файл

  pytest tests/ -m part1
      Запустить тесты с маркером 'part1'

  pytest tests/ -k "test_employee"
      Запустить тесты с 'test_employee' в названии

  pytest tests/ --durations=10
      Показать 10 самых долгих тестов

  pytest tests/ -n auto
      Параллельный запуск тестов (требует pytest-xdist)

НАСТРОЙКА ВЫВОДА:

  pytest tests/ -s
      Показать вывод print() из тестов

  pytest tests/ --tb=short
      Короткий формат traceback при ошибках

  pytest tests/ --tb=long
      Полный формат traceback

""")


if __name__ == "__main__":
    exit(main())
