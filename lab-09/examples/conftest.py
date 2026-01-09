#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
                          PYTEST CONFIGURATION
                    Конфигурация для всех тестов проекта
                          conftest.py v1.0
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import sys
import time
from pathlib import Path
from typing import Generator, Any

# ═══════════════════════════════════════════════════════════════════════════════
# НАСТРОЙКА ПУТЕЙ И ИМПОРТОВ
# ═══════════════════════════════════════════════════════════════════════════════

# Добавить src/ директорию в путь для импорта модулей
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
if src_path.exists():
    sys.path.insert(0, str(src_path))

# Попробовать добавить корневую директорию
if project_root.exists():
    sys.path.insert(0, str(project_root))


# ═══════════════════════════════════════════════════════════════════════════════
# ФИКСТУРЫ
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def temp_dir(tmp_path):
    """Временная директория для тестов"""
    return tmp_path


@pytest.fixture
def sample_employee_data():
    """Примеры данных сотрудников"""
    return {
        'valid': {
            'id': 1,
            'name': 'John Doe',
            'position': 'Developer',
            'salary': 50000,
            'department': 'IT',
        },
        'invalid': {
            'name': '',
            'salary': -1000,
        }
    }


@pytest.fixture
def sample_departments():
    """Примеры данных отделов"""
    return {
        'IT': {
            'name': 'IT Department',
            'budget': 500000,
        },
        'HR': {
            'name': 'Human Resources',
            'budget': 200000,
        },
        'Sales': {
            'name': 'Sales Department',
            'budget': 300000,
        },
    }


@pytest.fixture
def sample_projects():
    """Примеры данных проектов"""
    return {
        'project1': {
            'id': 1,
            'name': 'Project Alpha',
            'budget': 100000,
            'status': 'active',
        },
        'project2': {
            'id': 2,
            'name': 'Project Beta',
            'budget': 150000,
            'status': 'planning',
        },
    }


@pytest.fixture
def mock_logger(mocker):
    """Mock logger для тестов"""
    logger = mocker.MagicMock()
    logger.info = mocker.MagicMock()
    logger.warning = mocker.MagicMock()
    logger.error = mocker.MagicMock()
    logger.debug = mocker.MagicMock()
    return logger


@pytest.fixture
def timer():
    """Таймер для профилирования"""
    class Timer:
        def __init__(self):
            self.start = None
            self.end = None
        
        def __enter__(self):
            self.start = time.time()
            return self
        
        def __exit__(self, *args):
            self.end = time.time()
        
        @property
        def elapsed(self):
            if self.end is None:
                return time.time() - self.start
            return self.end - self.start
    
    return Timer()


@pytest.fixture
def capture_output(capsys):
    """Захват вывода для проверки"""
    return capsys


# ═══════════════════════════════════════════════════════════════════════════════
# МАРКЕРЫ
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_configure(config):
    """Регистрация кастомных маркеров"""
    markers = [
        'unit: unit-тесты (быстрые)',
        'integration: интеграционные тесты',
        'slow: медленные тесты',
        'part1: тесты Инкапсуляции',
        'part2: тесты Наследования',
        'part3: тесты Полиморфизма',
        'part4: тесты Композиции',
        'part5: тесты Паттернов',
        'smoke: smoke-тесты (базовая функциональность)',
        'regression: регрессионные тесты',
    ]
    
    for marker in markers:
        config.addinivalue_line('markers', marker)


# ═══════════════════════════════════════════════════════════════════════════════
# ХУКИ PYTEST
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_collection_modifyitems(config, items):
    """Модификация собранных тестов"""
    for item in items:
        # Добавить маркеры на основе названия файла
        if 'test_part1' in str(item.fspath):
            item.add_marker(pytest.mark.part1)
        elif 'test_part2' in str(item.fspath):
            item.add_marker(pytest.mark.part2)
        elif 'test_part3' in str(item.fspath):
            item.add_marker(pytest.mark.part3)
        elif 'test_part4' in str(item.fspath):
            item.add_marker(pytest.mark.part4)
        elif 'test_part5' in str(item.fspath):
            item.add_marker(pytest.mark.part5)
        elif 'test_integration' in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для кастомного отчета о тестах"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == 'call':
        # Добавить информацию о времени
        rep.test_duration = rep.duration


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Кастомный summary после всех тестов"""
    if exitstatus == 0:
        color = '\033[92m'  # Green
    else:
        color = '\033[91m'  # Red
    
    reset = '\033[0m'
    
    terminalreporter.write_sep('=', 'ТЕСТИРОВАНИЕ ЗАВЕРШЕНО', bold=True)
    if exitstatus == 0:
        terminalreporter.write_line(
            f'{color}✅ Все тесты пройдены успешно!{reset}',
            bold=True
        )
    else:
        terminalreporter.write_line(
            f'{color}❌ Некоторые тесты провалены!{reset}',
            bold=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_sessionstart(session):
    """Выполнить перед началом сессии тестирования"""
    print('\n' + '═' * 80)
    print('▶ ЗАПУСК ТЕСТИРОВАНИЯ'.center(80))
    print('═' * 80 + '\n')


def pytest_sessionfinish(session, exitstatus):
    """Выполнить после окончания сессии тестирования"""
    print('\n' + '═' * 80)
    if exitstatus == 0:
        print('✅ ТЕСТИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО'.center(80))
    else:
        print('❌ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО С ОШИБКАМИ'.center(80))
    print('═' * 80 + '\n')


# ═══════════════════════════════════════════════════════════════════════════════
# КОНФИГУРАЦИЯ PYTEST
# ═══════════════════════════════════════════════════════════════════════════════

# pytest.ini эквивалент в коде
pytest_plugins = []

# Опции по умолчанию (могут быть переопределены из командной строки)
def pytest_addoption(parser):
    """Добавить кастомные опции для pytest"""
    parser.addoption(
        '--slow',
        action='store_true',
        default=False,
        help='Запустить медленные тесты',
    )
    parser.addoption(
        '--cov-min',
        action='store',
        default=85,
        help='Минимальный процент покрытия кода (по умолчанию 85)',
    )


def pytest_configure(config):
    """Дополнительная конфигурация"""
    if not config.option.slow:
        config.option.marker_expr = 'not slow'


# ═══════════════════════════════════════════════════════════════════════════════
# КЛАСС ДЛЯ ТЕСТИРОВАНИЯ
# ═══════════════════════════════════════════════════════════════════════════════

class BaseTestCase:
    """Базовый класс для всех тестов"""
    
    @staticmethod
    def assert_is_valid_email(email: str) -> bool:
        """Проверить валидность email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def assert_is_valid_phone(phone: str) -> bool:
        """Проверить валидность номера телефона"""
        import re
        pattern = r'^[+]?[\d\s\-\(\)]{10,}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def assert_salary_in_range(salary: float, min_salary: float = 0, max_salary: float = 1000000) -> bool:
        """Проверить что зарплата в допустимом диапазоне"""
        return min_salary <= salary <= max_salary