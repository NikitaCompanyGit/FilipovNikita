"""
Тесты для Data Access Pattern (рефакторенная версия).

Покрывает:
  ✓ Entity and Value Objects
  ✓ Repository pattern (CRUD)
  ✓ Specification pattern (фильтрация)
  ✓ Unit of Work pattern
  ✓ Пример интеграции
"""

import pytest
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent))

from src.patterns.data_access_refactored import (  # ✅ ПРАВИЛЬНО
    Employee, Department, EmployeeId, DepartmentId,
    EmployeeRepository, DepartmentRepository,
    EmployeeBySalarySpecification, EmployeeByDepartmentSpecification,
    DepartmentWithMoreThan, UnitsOfWork, CompanyDataService


class TestValueObjects:
    """Тесты для значимых объектов."""
    
    def test_employee_id_creation(self):
        """Тест создания ID сотрудника."""
        emp_id = EmployeeId(1)
        assert emp_id.value == 1
    
    def test_employee_id_equality(self):
        """Тест равенства ID сотрудников."""
        id1 = EmployeeId(1)
        id2 = EmployeeId(1)
        id3 = EmployeeId(2)
        
        assert id1.value == id2.value
        assert id1.value != id3.value
    
    def test_department_id_creation(self):
        """Тест создания ID отдела."""
        dept_id = DepartmentId(10)
        assert dept_id.value == 10


class TestEmployee:
    """Тесты для сущности Employee."""
    
    def test_employee_creation(self):
        """Тест создания сотрудника."""
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John Doe",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        assert emp.emp_id.value == 1
        assert emp.name == "John Doe"
        assert emp.base_salary == 5000
    
    def test_employee_invalid_salary(self):
        """Тест создания с отрицательной зарплатой."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Employee(
                emp_id=EmployeeId(1),
                name="John",
                department_id=DepartmentId(10),
                base_salary=-1000
            )
    
    def test_employee_empty_name(self):
        """Тест создания с пустым именем."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Employee(
                emp_id=EmployeeId(1),
                name="",
                department_id=DepartmentId(10),
                base_salary=5000
            )
    
    def test_employee_representation(self):
        """Тест представления сотрудника."""
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John Doe",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        repr_str = repr(emp)
        assert "John Doe" in repr_str
        assert "5000" in repr_str


class TestDepartment:
    """Тесты для сущности Department."""
    
    def test_department_creation(self):
        """Тест создания отдела."""
        dept = Department(
            dept_id=DepartmentId(10),
            name="Development",
            budget=100000
        )
        
        assert dept.dept_id.value == 10
        assert dept.name == "Development"
        assert dept.budget == 100000
    
    def test_department_invalid_budget(self):
        """Тест создания с отрицательным бюджетом."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Department(
                dept_id=DepartmentId(10),
                name="Development",
                budget=-100000
            )
    
    def test_department_empty_name(self):
        """Тест создания с пустым названием."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Department(
                dept_id=DepartmentId(10),
                name="",
                budget=100000
            )


class TestEmployeeRepository:
    """Тесты для репозитория сотрудников."""
    
    @pytest.fixture
    def repo(self):
        """Создаем репозиторий."""
        return EmployeeRepository()
    
    def test_add_employee(self, repo):
        """Тест добавления сотрудника."""
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        repo.add(emp)
        assert repo.count() == 1
    
    def test_get_by_id(self, repo):
        """Тест получения по ID."""
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        repo.add(emp)
        retrieved = repo.get_by_id(EmployeeId(1))
        
        assert retrieved is not None
        assert retrieved.name == "John"
    
    def test_get_nonexistent(self, repo):
        """Тест получения несуществующего сотрудника."""
        result = repo.get_by_id(EmployeeId(999))
        assert result is None
    
    def test_update_employee(self, repo):
        """Тест обновления сотрудника."""
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        repo.add(emp)
        
        emp.base_salary = 6000
        repo.update(emp)
        
        updated = repo.get_by_id(EmployeeId(1))
        assert updated.base_salary == 6000
    
    def test_remove_employee(self, repo):
        """Тест удаления сотрудника."""
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        repo.add(emp)
        assert repo.count() == 1
        
        repo.remove(emp)
        assert repo.count() == 0
    
    def test_get_all(self, repo):
        """Тест получения всех сотрудников."""
        for i in range(3):
            emp = Employee(
                emp_id=EmployeeId(i+1),
                name=f"Employee{i+1}",
                department_id=DepartmentId(10),
                base_salary=5000
            )
            repo.add(emp)
        
        all_employees = repo.get_all()
        assert len(all_employees) == 3


class TestDepartmentRepository:
    """Тесты для репозитория отделов."""
    
    @pytest.fixture
    def repo(self):
        """Создаем репозиторий."""
        return DepartmentRepository()
    
    def test_add_department(self, repo):
        """Тест добавления отдела."""
        dept = Department(
            dept_id=DepartmentId(10),
            name="Development",
            budget=100000
        )
        
        repo.add(dept)
        assert repo.count() == 1
    
    def test_get_by_id(self, repo):
        """Тест получения отдела по ID."""
        dept = Department(
            dept_id=DepartmentId(10),
            name="Development",
            budget=100000
        )
        
        repo.add(dept)
        retrieved = repo.get_by_id(DepartmentId(10))
        
        assert retrieved is not None
        assert retrieved.name == "Development"


class TestSpecifications:
    """Тесты для спецификаций."""
    
    @pytest.fixture
    def employees(self):
        """Создаем сотрудников."""
        return [
            Employee(EmployeeId(1), "Alice", DepartmentId(10), 5000),
            Employee(EmployeeId(2), "Bob", DepartmentId(10), 6000),
            Employee(EmployeeId(3), "Charlie", DepartmentId(20), 7000),
            Employee(EmployeeId(4), "David", DepartmentId(20), 4000),
        ]
    
    def test_salary_specification(self, employees):
        """Тест спецификации по зарплате."""
        spec = EmployeeBySalarySpecification(min_salary=5500, max_salary=7000)
        
        filtered = [emp for emp in employees if spec.is_satisfied_by(emp)]
        
        assert len(filtered) == 2
        assert all(5500 <= emp.base_salary <= 7000 for emp in filtered)
    
    def test_department_specification(self, employees):
        """Тест спецификации по отделу."""
        spec = EmployeeByDepartmentSpecification(DepartmentId(10))
        
        filtered = [emp for emp in employees if spec.is_satisfied_by(emp)]
        
        assert len(filtered) == 2
        assert all(emp.department_id.value == 10 for emp in filtered)
    
    def test_combined_specifications(self, employees):
        """Тест комбинирования спецификаций."""
        salary_spec = EmployeeBySalarySpecification(min_salary=5000)
        dept_spec = EmployeeByDepartmentSpecification(DepartmentId(10))
        
        filtered = [
            emp for emp in employees
            if salary_spec.is_satisfied_by(emp) and dept_spec.is_satisfied_by(emp)
        ]
        
        assert len(filtered) == 2


class TestUnitOfWork:
    """Тесты для Unit of Work паттерна."""
    
    def test_unit_of_work_commit(self):
        """Тест commit в UoW."""
        uow = UnitsOfWork()
        
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        uow.employee_repo.add(emp)
        uow.commit()
        
        # Проверяем что изменения сохранены
        assert uow.employee_repo.count() == 1
    
    def test_unit_of_work_rollback(self):
        """Тест rollback в UoW."""
        uow = UnitsOfWork()
        
        emp = Employee(
            emp_id=EmployeeId(1),
            name="John",
            department_id=DepartmentId(10),
            base_salary=5000
        )
        
        uow.employee_repo.add(emp)
        uow.rollback()
        
        # После rollback изменения должны быть отменены
        assert uow.employee_repo.count() == 0


class TestCompanyDataService:
    """Тесты для сервиса данных компании."""
    
    def test_hire_employee(self):
        """Тест найма сотрудника."""
        service = CompanyDataService()
        
        result = service.hire_employee("John Doe", DepartmentId(10), 5000)
        
        assert result.is_success is True
        assert result.employee is not None
        assert result.employee.name == "John Doe"
    
    def test_hire_employee_invalid_salary(self):
        """Тест найма с отрицательной зарплатой."""
        service = CompanyDataService()
        
        result = service.hire_employee("John", DepartmentId(10), -5000)
        
        assert result.is_success is False
        assert "Invalid employee data" in result.error
    
    def test_get_department_salary_info(self):
        """Тест получения информации о зарплатах в отделе."""
        service = CompanyDataService()
        
        service.hire_employee("John", DepartmentId(10), 5000)
        service.hire_employee("Jane", DepartmentId(10), 6000)
        service.hire_employee("Bob", DepartmentId(20), 7000)
        
        info = service.get_department_salary_info(DepartmentId(10))
        
        assert info.total_salary == 11000
        assert info.average_salary == 5500
        assert info.employee_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
