"""
МОДУЛЬ КОМПАРАТОРОВ (HELPER FUNCTIONS)

Этот модуль содержит функции-ключи (key functions), которые используются
встроенной функцией Python `sorted()` или методом `.sort()` списков.
Они определяют критерии сравнения объектов AbstractEmployee.
"""

def sort_by_name(employee):
    """
    Критерий сортировки: Имя сотрудника (алфавитный порядок).
    Пример использования: sorted(employees, key=sort_by_name)
    """
    return employee.name

def sort_by_salary(employee):
    """
    Критерий сортировки: Итоговая зарплата (возрастание).
    Использует полиморфный метод calculate_salary(), что позволяет
    корректно сравнивать доходы разных типов сотрудников (менеджеров, продавцов и т.д.).
    """
    return employee.calculate_salary()

def sort_by_dept_then_name(employee):
    """
    Сложный критерий сортировки:
    1. Сначала по Отделу (группировка).
    2. Затем по Имени внутри отдела (алфавитный порядок).
    
    Возвращает кортеж, так как Python сравнивает кортежи поэлементно.
    """
    return (employee.department, employee.name)
