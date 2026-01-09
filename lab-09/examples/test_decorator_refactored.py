"""
Тесты для Decorator Pattern (рефакторенная версия).

Покрывает:
  ✓ Система логирования (ILogger, ConsoleLogger, FileLogger, NullLogger, CompositeLogger)
  ✓ Валидация параметров (SalaryValidator)
  ✓ Все типы декораторов
  ✓ Обработка исключений
"""

import pytest
import sys
import os
from pathlib import Path
from io import StringIO

# Добавляем родительскую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from decorator_refactored import (
    LogLevel, ILogger, ConsoleLogger, FileLogger, NullLogger, CompositeLogger,
    SalaryValidator, EmployeeComponent, ConcreteEmployee,
    BonusDecorator, PerformanceBonusDecorator, TrainingDecorator,
    ProjExperienceDecorator, VacationBenefitDecorator
)


class TestLoggerInterface:
    """Тесты для интерфейса логирования."""
    
    def test_console_logger(self, capsys):
        """Тест ConsoleLogger."""
        logger = ConsoleLogger()
        logger.info("Test message")
        
        captured = capsys.readouterr()
        assert "[INFO] Test message" in captured.out
    
    def test_file_logger(self, tmp_path):
        """Тест FileLogger."""
        log_file = tmp_path / "test.log"
        logger = FileLogger(str(log_file))
        
        logger.info("Test message")
        logger.error("Error message")
        
        content = log_file.read_text()
        assert "[INFO] Test message" in content
        assert "[ERROR] Error message" in content
    
    def test_null_logger(self, capsys):
        """Тест NullLogger (ничего не выводит)."""
        logger = NullLogger()
        logger.info("This should not print")
        
        captured = capsys.readouterr()
        assert captured.out == ""
    
    def test_composite_logger(self, capsys, tmp_path):
        """Тест CompositeLogger."""
        log_file = tmp_path / "composite.log"
        
        composite = CompositeLogger()
        composite.add_logger(ConsoleLogger())
        composite.add_logger(FileLogger(str(log_file)))
        
        composite.info("Test message")
        
        # Проверяем консоль
        captured = capsys.readouterr()
        assert "[INFO] Test message" in captured.out
        
        # Проверяем файл
        content = log_file.read_text()
        assert "[INFO] Test message" in content
    
    def test_all_log_levels(self, capsys):
        """Тест всех уровней логирования."""
        logger = ConsoleLogger()
        
        logger.debug("Debug")
        logger.info("Info")
        logger.warning("Warning")
        logger.error("Error")
        
        captured = capsys.readouterr()
        assert "[DEBUG] Debug" in captured.out
        assert "[INFO] Info" in captured.out
        assert "[WARNING] Warning" in captured.out
        assert "[ERROR] Error" in captured.out


class TestSalaryValidator:
    """Тесты для валидатора зарплаты."""
    
    def test_validate_bonus_positive(self):
        """Тест валидации позитивного бонуса."""
        validator = SalaryValidator()
        validator.validate_bonus(1000)  # Не должно быть исключения
    
    def test_validate_bonus_negative(self):
        """Тест валидации негативного бонуса."""
        validator = SalaryValidator()
        with pytest.raises(ValueError, match="Бонус не может быть отрицательным"):
            validator.validate_bonus(-100)
    
    def test_validate_rating_valid(self):
        """Тест валидации корректного рейтинга."""
        validator = SalaryValidator()
        validator.validate_rating(1.0)
        validator.validate_rating(0.5)
        validator.validate_rating(2.0)
    
    def test_validate_rating_invalid(self):
        """Тест валидации некорректного рейтинга."""
        validator = SalaryValidator()
        with pytest.raises(ValueError, match="Рейтинг должен быть"):
            validator.validate_rating(2.5)
        
        with pytest.raises(ValueError, match="Рейтинг должен быть"):
            validator.validate_rating(0.3)
    
    def test_validate_days_positive(self):
        """Тест валидации позитивного количества дней."""
        validator = SalaryValidator()
        validator.validate_days(5)
    
    def test_validate_days_negative(self):
        """Тест валидации негативного количества дней."""
        validator = SalaryValidator()
        with pytest.raises(ValueError, match="Количество дней не может быть отрицательным"):
            validator.validate_days(-1)


class TestConcreteEmployee:
    """Тесты для базового сотрудника."""
    
    def test_create_employee(self):
        """Тест создания сотрудника."""
        logger = NullLogger()
        employee = ConcreteEmployee("John Doe", 5000, logger)
        
        assert employee.get_name() == "John Doe"
        assert employee.get_base_salary() == 5000
        assert employee.get_total_salary() == 5000
    
    def test_employee_invalid_salary(self):
        """Тест создания сотрудника с отрицательной зарплатой."""
        logger = NullLogger()
        with pytest.raises(ValueError, match="Зарплата не может быть отрицательной"):
            ConcreteEmployee("John", -1000, logger)
    
    def test_employee_description(self):
        """Тест описания сотрудника."""
        logger = NullLogger()
        employee = ConcreteEmployee("John Doe", 5000, logger)
        desc = employee.get_description()
        
        assert "John Doe" in desc
        assert "5000" in desc


class TestBonusDecorator:
    """Тесты для BonusDecorator."""
    
    def test_single_bonus(self):
        """Тест добавления одного бонуса."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        employee_with_bonus = BonusDecorator(employee, 1000, logger)
        
        assert employee_with_bonus.get_total_salary() == 6000
        assert "Бонус: 1000" in employee_with_bonus.get_description()
    
    def test_negative_bonus(self):
        """Тест добавления отрицательного бонуса."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        
        with pytest.raises(ValueError, match="Бонус не может быть отрицательным"):
            BonusDecorator(employee, -500, logger)
    
    def test_stacked_bonuses(self):
        """Тест стека бонусов."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        employee = BonusDecorator(employee, 1000, logger)
        employee = BonusDecorator(employee, 500, logger)
        
        assert employee.get_total_salary() == 6500


class TestPerformanceBonusDecorator:
    """Тесты для PerformanceBonusDecorator."""
    
    def test_performance_bonus_above_norm(self):
        """Тест бонуса за производительность выше нормы."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 1000, logger)
        employee = PerformanceBonusDecorator(employee, 1.5, logger)
        
        # Бонус = 1000 * (1.5 - 1.0) = 500
        assert employee.get_total_salary() == 1500
    
    def test_performance_bonus_below_norm(self):
        """Тест бонуса за производительность ниже нормы."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 1000, logger)
        employee = PerformanceBonusDecorator(employee, 0.8, logger)
        
        # Бонус = 1000 * (0.8 - 1.0) = -200
        assert employee.get_total_salary() == 800
    
    def test_invalid_performance_rating(self):
        """Тест некорректного рейтинга производительности."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 1000, logger)
        
        with pytest.raises(ValueError, match="Рейтинг должен быть"):
            PerformanceBonusDecorator(employee, 3.0, logger)


class TestTrainingDecorator:
    """Тесты для TrainingDecorator."""
    
    def test_training_bonus(self):
        """Тест добавления бонуса за обучение."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        employee = TrainingDecorator(employee, "Python Advanced", 500, logger)
        
        assert employee.get_total_salary() == 5500
        assert "Python Advanced" in employee.get_description()
    
    def test_invalid_training_bonus(self):
        """Тест отрицательного бонуса за обучение."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        
        with pytest.raises(ValueError, match="Бонус не может быть отрицательным"):
            TrainingDecorator(employee, "Python", -500, logger)


class TestProjExperienceDecorator:
    """Тесты для ProjExperienceDecorator."""
    
    def test_project_bonus(self):
        """Тест добавления бонуса за опыт проектов."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        employee = ProjExperienceDecorator(employee, 3, 200, logger)
        
        # Бонус = 3 * 200 = 600
        assert employee.get_total_salary() == 5600
        assert "Опыт проектов: 3" in employee.get_description()
    
    def test_no_projects(self):
        """Тест при отсутствии проектов."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        employee = ProjExperienceDecorator(employee, 0, 200, logger)
        
        assert employee.get_total_salary() == 5000


class TestVacationBenefitDecorator:
    """Тесты для VacationBenefitDecorator."""
    
    def test_vacation_benefit(self):
        """Тест добавления выплаты за отпуск."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        employee = VacationBenefitDecorator(employee, 5, 100, logger)
        
        # Выплата = 5 * 100 = 500
        assert employee.get_total_salary() == 5500
        assert "Выплата за отпуск: 5 дней (500)" in employee.get_description()
    
    def test_invalid_vacation_days(self):
        """Тест отрицательного количества дней отпуска."""
        logger = NullLogger()
        employee = ConcreteEmployee("John", 5000, logger)
        
        with pytest.raises(ValueError, match="Количество дней не может быть отрицательным"):
            VacationBenefitDecorator(employee, -5, 100, logger)


class TestDecoratorStacking:
    """Тесты для комбинирования нескольких декораторов."""
    
    def test_complex_employee(self):
        """Тест сложного сотрудника со множеством декораторов."""
        logger = NullLogger()
        
        # Создаём сотрудника
        employee = ConcreteEmployee("Alice", 6000, logger)
        
        # Добавляем декораторы
        employee = PerformanceBonusDecorator(employee, 1.2, logger)  # +20% = 1200
        employee = TrainingDecorator(employee, "Leadership", 500, logger)
        employee = ProjExperienceDecorator(employee, 3, 200, logger)  # 3 * 200 = 600
        employee = VacationBenefitDecorator(employee, 5, 100, logger)  # 5 * 100 = 500
        
        # Проверяем результат
        total = employee.get_total_salary()
        expected = 6000 + 1200 + 500 + 600 + 500
        assert total == expected
        
        # Проверяем описание
        desc = employee.get_description()
        assert "Alice" in desc
        assert "Leadership" in desc
        assert "Опыт проектов" in desc


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
