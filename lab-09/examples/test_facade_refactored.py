"""
Тесты для Facade Pattern (рефакторенная версия).

Покрывает:
  ✓ OperationResult и OperationStatus
  ✓ ErrorHandler
  ✓ Subsystem взаимодействие
  ✓ CompanyFacade операции
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from facade_refactored import (
    OperationStatus, OperationResult, ErrorHandler,
    CompanySubsystemA, CompanySubsystemB, CompanySubsystemC,
    CompanySubsystemD, SubsystemManager, CompanyFacade
)


class TestOperationResult:
    """Тесты для OperationResult."""
    
    def test_success_result(self):
        """Тест успешного результата."""
        result = OperationResult(OperationStatus.SUCCESS, "Operation successful")
        assert result.is_success is True
        assert result.status == OperationStatus.SUCCESS
    
    def test_failure_result(self):
        """Тест неудачного результата."""
        result = OperationResult(OperationStatus.FAILURE, "Operation failed")
        assert result.is_success is False
        assert result.status == OperationStatus.FAILURE
    
    def test_result_with_data(self):
        """Тест результата с данными."""
        data = {"employees": ["John", "Jane"]}
        result = OperationResult(OperationStatus.SUCCESS, "Got employees", data=data)
        assert result.data == data
    
    def test_result_string_representation(self):
        """Тест строкового представления результата."""
        result = OperationResult(OperationStatus.SUCCESS, "Test message")
        assert "[SUCCESS] Test message" in str(result)


class TestErrorHandler:
    """Тесты для ErrorHandler."""
    
    def test_add_error(self):
        """Тест добавления ошибки."""
        handler = ErrorHandler()
        handler.add_error("Test error")
        
        assert handler.has_errors() is True
        assert "Test error" in handler.get_error_message()
    
    def test_multiple_errors(self):
        """Тест множества ошибок."""
        handler = ErrorHandler()
        handler.add_error("Error 1")
        handler.add_error("Error 2")
        
        errors = handler.get_errors()
        assert len(errors) == 2
        assert "Error 1" in errors
        assert "Error 2" in errors
    
    def test_clear_errors(self):
        """Тест очистки ошибок."""
        handler = ErrorHandler()
        handler.add_error("Test error")
        handler.clear()
        
        assert handler.has_errors() is False
        assert len(handler.get_errors()) == 0


class TestCompanySubsystems:
    """Тесты для подсистем."""
    
    def test_subsystem_a_departments(self):
        """Тест подсистемы управления отделами."""
        subsys = CompanySubsystemA()
        
        depts = subsys.list_all_departments()
        assert "DEV" in depts
        assert "SALES" in depts
        
        assert subsys.department_exists("DEV") is True
        assert subsys.department_exists("NONEXISTENT") is False
    
    def test_subsystem_b_employees(self):
        """Тест подсистемы управления сотрудниками."""
        subsys = CompanySubsystemB()
        
        employees = subsys.list_employees_by_department("DEV")
        assert len(employees) > 0
        
        subsys.hire_employee("NewEmployee", "DEV")
        employees = subsys.list_employees_by_department("DEV")
        assert "NewEmployee" in employees
    
    def test_subsystem_c_salary(self):
        """Тест подсистемы расчета зарплат."""
        subsys = CompanySubsystemC()
        
        salary = subsys.calculate_monthly_salary("John")
        assert salary > 0
        
        subsys.set_salary("Jane", 10000)
        salary = subsys.calculate_monthly_salary("Jane")
        assert salary == 10000
    
    def test_subsystem_d_projects(self):
        """Тест подсистемы управления проектами."""
        subsys = CompanySubsystemD()
        
        projects = subsys.list_active_projects()
        assert len(projects) > 0
        
        status = subsys.get_project_status("Project Alpha")
        assert status == "active"


class TestSubsystemManager:
    """Тесты для менеджера подсистем."""
    
    def test_subsystem_manager_initialization(self):
        """Тест инициализации менеджера."""
        manager = SubsystemManager()
        
        assert manager.subsystem_a is not None
        assert manager.subsystem_b is not None
        assert manager.subsystem_c is not None
        assert manager.subsystem_d is not None
        assert manager.error_handler is not None


class TestCompanyFacade:
    """Тесты для фасада компании."""
    
    def test_hire_new_employee_success(self):
        """Тест найма нового сотрудника."""
        facade = CompanyFacade()
        
        result = facade.hire_new_employee("NewEmployee", "DEV")
        assert result.is_success is True
        assert "успешно нанят" in result.message
    
    def test_hire_new_employee_invalid_department(self):
        """Тест найма с неправильным отделом."""
        facade = CompanyFacade()
        
        result = facade.hire_new_employee("Employee", "INVALID_DEPT")
        assert result.is_success is False
        assert "не существует" in result.message
    
    def test_fire_employee(self):
        """Тест увольнения сотрудника."""
        facade = CompanyFacade()
        
        # Сначала нанимаем
        facade.hire_new_employee("ToFire", "DEV")
        
        # Затем увольняем
        result = facade.fire_employee("ToFire")
        assert result.is_success is True
        assert "успешно уволен" in result.message
    
    def test_transfer_employee(self):
        """Тест перевода сотрудника."""
        facade = CompanyFacade()
        
        facade.hire_new_employee("ToTransfer", "DEV")
        result = facade.transfer_employee("ToTransfer", "SALES")
        
        assert result.is_success is True
        assert "SALES" in result.message
    
    def test_transfer_employee_invalid_department(self):
        """Тест перевода в несуществующий отдел."""
        facade = CompanyFacade()
        
        result = facade.transfer_employee("John", "INVALID")
        assert result.is_success is False
    
    def test_process_monthly_payroll(self):
        """Тест обработки месячной зарплаты."""
        facade = CompanyFacade()
        
        result = facade.process_monthly_payroll()
        assert result.is_success is True
        assert result.data is not None
        
        payroll = result.data
        assert isinstance(payroll, dict)
        assert len(payroll) > 0
    
    def test_get_department_employees(self):
        """Тест получения сотрудников отдела."""
        facade = CompanyFacade()
        
        result = facade.get_department_employees("DEV")
        assert result.is_success is True
        assert isinstance(result.data, list)
        assert len(result.data) > 0
    
    def test_get_company_summary(self):
        """Тест получения сводки по компании."""
        facade = CompanyFacade()
        
        result = facade.get_company_summary()
        assert result.is_success is True
        
        summary = result.data
        assert 'departments' in summary
        assert 'employees' in summary
        assert 'active_projects' in summary
    
    def test_facade_complex_scenario(self):
        """Тест сложного сценария."""
        facade = CompanyFacade()
        
        # Нанимаем сотрудника
        hire_result = facade.hire_new_employee("TestEmployee", "DEV")
        assert hire_result.is_success is True
        
        # Получаем информацию
        dept_result = facade.get_department_employees("DEV")
        assert "TestEmployee" in dept_result.data
        
        # Обрабатываем зарплату
        payroll_result = facade.process_monthly_payroll()
        assert payroll_result.is_success is True
        assert "TestEmployee" in payroll_result.data
        
        # Переводим сотрудника
        transfer_result = facade.transfer_employee("TestEmployee", "SALES")
        assert transfer_result.is_success is True
        
        # Проверяем новый отдел
        sales_result = facade.get_department_employees("SALES")
        assert "TestEmployee" in sales_result.data
        
        # Увольняем сотрудника
        fire_result = facade.fire_employee("TestEmployee")
        assert fire_result.is_success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
