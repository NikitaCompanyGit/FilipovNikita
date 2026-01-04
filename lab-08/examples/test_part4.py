import os
from organization.company import Company
from organization.department import Department
from organization.project import Project
from specialists.manager import Manager
from specialists.developer import Developer
from specialists.salesperson import Salesperson
from base.exceptions import DependencyError, InvalidStatusError

class TestPart4:
    """
    ТЕСТОВЫЙ НАБОР ЧАСТИ 4: КОМПОЗИЦИЯ, СИСТЕМА И ИНТЕГРАЦИЯ
    
    Цель: Проверить работу системы в сборе (System Testing).
    Основные аспекты проверки:
    1. Жизненный цикл сложных объектов (Company, Project).
    2. Управление связями (ссылки на сотрудников в проектах).
    3. Полная сериализация/десериализация с восстановлением связей.
    4. Защита целостности данных (валидация зависимостей).
    """

    @staticmethod
    def run():
        print("=== ЗАПУСК ТЕСТОВ ЧАСТИ 4 (КОМПОЗИЦИЯ И СИСТЕМА) ===")
        TestPart4.test_full_lifecycle()
        TestPart4.test_validations_and_dependencies()
        print("=== ТЕСТЫ ЧАСТИ 4 ЗАВЕРШЕНЫ ===\n")

    @staticmethod
    def test_full_lifecycle():
        """
        Сквозной тест (End-to-End):
        Создание -> Наполнение данными -> Сохранение в файл -> Загрузка -> Проверка.
        """
        print("   [4.1] Жизненный цикл компании (Full Cycle)...")
        
        # 1. Создание структуры
        comp = Company("MegaSoft")
        dept_dev = Department("Development")
        dept_sales = Department("Sales")
        comp.add_department(dept_dev)
        comp.add_department(dept_sales)

        # 2. Найм сотрудников
        dev = Developer(1, "John", "Development", 100, "senior", ["Python"])
        manager = Manager(2, "Alice", "Development", 150, 50)
        sales = Salesperson(3, "Bob", "Sales", 80, 0.1)
        
        dept_dev.add_employee(dev)
        dept_dev.add_employee(manager)
        dept_sales.add_employee(sales)

        # 3. Создание проекта и назначение команды (Композиция + Агрегация)
        proj = Project(101, "SuperApp", "The best app", "2025-12-31", "active")
        comp.add_project(proj)
        
        # Назначаем сотрудников в проект (создаем связь)
        proj.add_team_member(dev)
        proj.add_team_member(manager)

        # 4. Сериализация и Экспорт
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, "docs", "json", "company_full.json")
        csv_emp_path = os.path.join(base_dir, "docs", "csv", "employees.csv")
        csv_proj_path = os.path.join(base_dir, "docs", "csv", "projects.csv")

        comp.save_to_json(json_path)
        comp.export_employees_csv(csv_emp_path) # Проверка UTF-8-SIG кодировки
        comp.export_projects_csv(csv_proj_path)

        # 5. Десериализация и верификация связей
        new_comp = Company.load_from_json(json_path)
        
        assert len(new_comp.get_departments()) == 2
        assert len(new_comp.get_projects()) == 1
        
        # Проверяем, что команда проекта восстановилась
        loaded_proj = new_comp.get_projects()[0]
        assert loaded_proj.get_team_size() == 2, "ОШИБКА: Команда проекта потеряна при загрузке!"
        
        # Проверяем типы восстановленных объектов
        team_member = loaded_proj.get_team()[0]
        assert isinstance(team_member, (Developer, Manager))
        
        print("      -> Структура компании и связи между объектами успешно восстановлены.")

    @staticmethod
    def test_validations_and_dependencies():
        """Проверяет защиту данных от случайного удаления (Integrity Checks)."""
        print("   [4.2] Тест валидации зависимостей (Negative Tests)...")
        comp = Company("TestComp")
        dept = Department("IT")
        comp.add_department(dept)
        
        dev = Developer(10, "Dave", "IT", 100, "junior")
        dept.add_employee(dev)
        
        proj = Project(99, "Legacy", "Old stuff", "2020-01-01", "planning")
        comp.add_project(proj)
        proj.add_team_member(dev)

        # Сценарий 1: Запрет удаления непустого отдела
        try:
            comp.remove_department("IT")
            print("      -> ОШИБКА: Система позволила удалить отдел с сотрудниками.")
        except DependencyError:
            print("      -> OK: Сработала защита удаления непустого отдела.")

        # Сценарий 2: Запрет увольнения сотрудника, занятого в проекте
        try:
            comp.remove_employee_globally(10)
            print("      -> ОШИБКА: Система позволила удалить сотрудника, занятого в проекте.")
        except DependencyError:
            print("      -> OK: Сработала защита удаления занятого сотрудника.")

        # Сценарий 3: Валидация статуса проекта
        try:
            proj.status = "destroyed" # Недопустимый статус
        except InvalidStatusError:
            print("      -> OK: Валидация статуса проекта корректна.")
            
        print("      -> Все проверки целостности данных пройдены.")
