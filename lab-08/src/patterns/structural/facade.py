# Facade (Фасад)
# ===============
# Предоставляет унифицированный интерфейс к набору интерфейсов в подсистеме.
# Фасад определяет более высокоуровневый интерфейс, облегчающий использование подсистемы.

from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod

class CompanySubsystemA:
    """Подсистема А - Управление отделами."""
    
    def list_all_departments(self) -> List[str]:
        """Получить список всех отделов."""
        print("[Subsystem A] Запрос списка отделов из БД...")
        return ["DEV", "SALES", "HR", "FINANCE"]
    
    def add_department(self, dept_name: str) -> bool:
        """Добавить новый отдел."""
        print(f"[Subsystem A] Добавление отдела '{dept_name}'...")
        return True
    
    def remove_department(self, dept_name: str) -> bool:
        """Удалить отдел."""
        print(f"[Subsystem A] Удаление отдела '{dept_name}'...")
        return True


class CompanySubsystemB:
    """Подсистема B - Управление сотрудниками."""
    
    def list_employees_by_department(self, dept_name: str) -> List[str]:
        """Получить сотрудников отдела."""
        print(f"[Subsystem B] Запрос сотрудников отдела '{dept_name}'...")
        return ["John Doe", "Jane Smith", "Bob Johnson"]
    
    def hire_employee(self, name: str, dept_name: str) -> bool:
        """Нанять сотрудника."""
        print(f"[Subsystem B] Найм '{name}' в отдел '{dept_name}'...")
        return True
    
    def fire_employee(self, name: str) -> bool:
        """Уволить сотрудника."""
        print(f"[Subsystem B] Увольнение '{name}'...")
        return True


class CompanySubsystemC:
    """Подсистема C - Расчёт зарплат."""
    
    def calculate_monthly_salary(self, employee_name: str) -> float:
        """Расчёт месячной зарплаты."""
        print(f"[Subsystem C] Расчёт зарплаты для '{employee_name}'...")
        import random
        return random.uniform(2000, 10000)
    
    def process_payroll(self, employee_names: List[str]) -> float:
        """Обработка зарплатной ведомости."""
        print(f"[Subsystem C] Обработка зарплаты для {len(employee_names)} сотрудников...")
        total = sum(self.calculate_monthly_salary(name) for name in employee_names)
        return total
    
    def apply_bonus(self, employee_name: str, bonus_amount: float) -> bool:
        """Применить бонус."""
        print(f"[Subsystem C] Применение бонуса {bonus_amount} для '{employee_name}'...")
        return True


class CompanySubsystemD:
    """Подсистема D - Управление проектами."""
    
    def list_active_projects(self) -> List[str]:
        """Получить список активных проектов."""
        print("[Subsystem D] Запрос активных проектов...")
        return ["Project Alpha", "Project Beta", "Project Gamma"]
    
    def assign_employee_to_project(self, employee_name: str, 
                                  project_name: str) -> bool:
        """Назначить сотрудника на проект."""
        print(f"[Subsystem D] Назначение '{employee_name}' на '{project_name}'...")
        return True
    
    def get_project_status(self, project_name: str) -> str:
        """Получить статус проекта."""
        print(f"[Subsystem D] Запрос статуса '{project_name}'...")
        return "active"


# ===== ФАСАД =====
class CompanyFacade:
    """
    Фасад для работы с компанией.
    Предоставляет простой интерфейс для операций, скрывая сложность подсистем.
    """
    
    def __init__(self):
        """Инициализация фасада со всеми подсистемами."""
        self._subsystem_a = CompanySubsystemA()
        self._subsystem_b = CompanySubsystemB()
        self._subsystem_c = CompanySubsystemC()
        self._subsystem_d = CompanySubsystemD()
        print("[Facade] CompanyFacade инициализирован со всеми подсистемами\n")
    
    # ===== ВЫСОКОУРОВНЕВЫЕ ОПЕРАЦИИ =====
    
    def hire_new_employee(self, name: str, department: str) -> bool:
        """
        Нанять нового сотрудника (скрывает сложность).
        Включает:
        1. Проверку наличия отдела
        2. Регистрацию сотрудника
        3. Создание записей в системе зарплат
        
        Args:
            name: Имя нового сотрудника
            department: Отдел
            
        Returns:
            True если успешно, False иначе
        """
        print(f"\n[Facade] === НАНЯТЬ СОТРУДНИКА: {name} в {department} ===")
        
        # Операция 1: Проверяем отдел
        departments = self._subsystem_a.list_all_departments()
        if department not in departments:
            print(f"[Facade] Отдел '{department}' не существует!")
            return False
        
        # Операция 2: Нанимаем сотрудника
        if not self._subsystem_b.hire_employee(name, department):
            print(f"[Facade] Ошибка при найме сотрудника")
            return False
        
        # Операция 3: Инициализируем зарплату в системе
        print(f"[Facade] Инициализация зарплаты в системе...")
        
        print(f"[Facade] ✓ Сотрудник успешно нанят!\n")
        return True
    
    def fire_employee(self, name: str) -> bool:
        """
        Уволить сотрудника (скрывает сложность).
        Включает:
        1. Поиск сотрудника
        2. Удаление из всех проектов
        3. Расчёт финальной зарплаты
        4. Удаление из БД
        
        Args:
            name: Имя сотрудника для увольнения
            
        Returns:
            True если успешно, False иначе
        """
        print(f"\n[Facade] === УВОЛИТЬ СОТРУДНИКА: {name} ===")
        
        # Операция 1: Расчет финальной зарплаты (severance pay)
        final_salary = self._subsystem_c.calculate_monthly_salary(name)
        print(f"[Facade] Финальная выплата: {final_salary}")
        
        # Операция 2: Удаление из проектов
        projects = self._subsystem_d.list_active_projects()
        for project in projects:
            print(f"[Facade] Удаление '{name}' из проекта '{project}'...")
        
        # Операция 3: Увольнение
        if not self._subsystem_b.fire_employee(name):
            print(f"[Facade] Ошибка при увольнении")
            return False
        
        print(f"[Facade] ✓ Сотрудник успешно уволен!\n")
        return True
    
    def transfer_employee(self, name: str, new_department: str) -> bool:
        """
        Перевести сотрудника в другой отдел (скрывает сложность).
        
        Args:
            name: Имя сотрудника
            new_department: Новый отдел
            
        Returns:
            True если успешно, False иначе
        """
        print(f"\n[Facade] === ПЕРЕВЕСТИ СОТРУДНИКА: {name} -> {new_department} ===")
        
        # Проверяем отдел
        departments = self._subsystem_a.list_all_departments()
        if new_department not in departments:
            print(f"[Facade] Отдел '{new_department}' не существует!")
            return False
        
        print(f"[Facade] Обновление информации о сотруднике...")
        print(f"[Facade] Переназначение проектов...")
        
        print(f"[Facade] ✓ Сотрудник успешно переведён!\n")
        return True
    
    def process_monthly_payroll(self) -> Dict[str, float]:
        """
        Обработать месячную зарплатную ведомость (скрывает сложность).
        Включает:
        1. Получение списка всех сотрудников
        2. Расчёт зарплаты
        3. Применение бонусов
        4. Создание платёжных документов
        
        Returns:
            Словарь: сотрудник -> зарплата
        """
        print(f"\n[Facade] === ОБРАБОТКА МЕСЯЧНОЙ ЗАРПЛАТЫ ===")
        
        payroll = {}
        
        # Получаем всех сотрудников
        departments = self._subsystem_a.list_all_departments()
        all_employees = []
        
        for dept in departments:
            employees = self._subsystem_b.list_employees_by_department(dept)
            all_employees.extend(employees)
        
        print(f"[Facade] Найдено сотрудников: {len(all_employees)}")
        
        # Обрабатываем зарплату для каждого
        for emp_name in all_employees:
            salary = self._subsystem_c.calculate_monthly_salary(emp_name)
            payroll[emp_name] = salary
        
        # Генерируем отчёт
        total = sum(payroll.values())
        print(f"[Facade] Итого к выплате: {total}")
        
        print(f"[Facade] ✓ Зарплата успешно обработана!\n")
        return payroll
    
    def get_department_employees(self, department: str) -> List[str]:
        """
        Получить сотрудников отдела (простой вызов подсистемы).
        
        Args:
            department: Название отдела
            
        Returns:
            Список имён сотрудников
        """
        print(f"\n[Facade] === ПОЛУЧИТЬ СОТРУДНИКОВ ОТДЕЛА: {department} ===")
        return self._subsystem_b.list_employees_by_department(department)
    
    def get_active_projects(self) -> List[str]:
        """Получить активные проекты."""
        print(f"\n[Facade] === ПОЛУЧИТЬ АКТИВНЫЕ ПРОЕКТЫ ===")
        return self._subsystem_d.list_active_projects()
    
    def assign_to_project(self, employee_name: str, project_name: str) -> bool:
        """Назначить сотрудника на проект."""
        print(f"\n[Facade] === НАЗНАЧИТЬ НА ПРОЕКТ ===")
        return self._subsystem_d.assign_employee_to_project(employee_name, project_name)
    
    def apply_performance_bonus(self, employee_name: str, bonus_percentage: float) -> bool:
        """
        Применить бонус производительности (скрывает сложность).
        
        Args:
            employee_name: Имя сотрудника
            bonus_percentage: Процент бонуса от базовой зарплаты
            
        Returns:
            True если успешно, False иначе
        """
        print(f"\n[Facade] === ПРИМЕНИТЬ БОНУС: {employee_name} ===")
        
        # Вычисляем размер бонуса
        salary = self._subsystem_c.calculate_monthly_salary(employee_name)
        bonus_amount = salary * (bonus_percentage / 100)
        
        # Применяем бонус
        result = self._subsystem_c.apply_bonus(employee_name, bonus_amount)
        
        print(f"[Facade] Бонус {bonus_percentage}% = {bonus_amount}")
        print(f"[Facade] ✓ Бонус успешно применён!\n")
        
        return result
    
    def get_company_summary(self) -> Dict[str, Any]:
        """
        Получить сводку по компании (использует все подсистемы).
        
        Returns:
            Словарь с информацией о компании
        """
        print(f"\n[Facade] === СВОДКА ПО КОМПАНИИ ===")
        
        departments = self._subsystem_a.list_all_departments()
        projects = self._subsystem_d.list_active_projects()
        
        employee_count = 0
        for dept in departments:
            emps = self._subsystem_b.list_employees_by_department(dept)
            employee_count += len(emps)
        
        summary = {
            'departments': departments,
            'employee_count': employee_count,
            'active_projects': projects,
            'project_count': len(projects),
        }
        
        print(f"[Facade] Отделы: {len(departments)}")
        print(f"[Facade] Сотрудники: {employee_count}")
        print(f"[Facade] Активные проекты: {len(projects)}\n")
        
        return summary
