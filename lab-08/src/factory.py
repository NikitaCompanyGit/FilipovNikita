from base.abstract_employee import AbstractEmployee
from specialists.ordinary_employee import OrdinaryEmployee
from specialists.manager import Manager
from specialists.developer import Developer
from specialists.salesperson import Salesperson

class EmployeeFactory:
    """
    Реализация паттерна проектирования "Фабричный метод" (Factory Method).
    
    Этот класс инкапсулирует сложную логику создания объектов сотрудников.
    Клиентский код (например, класс Company при загрузке из JSON) не должен знать,
    какой конкретно класс инстанцировать — он передает только тип сотрудника и параметры.
    """

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Универсальный метод создания сотрудника.

        :param emp_type: Строковый идентификатор типа ('manager', 'developer'...).
        :param kwargs: Словарь именованных аргументов. Должен содержать:
                       - Общие поля: id, name, department, base_salary
                       - Специфичные поля: bonus, seniority, tech_stack и др.
        :return: Экземпляр наследника AbstractEmployee.
        :raises ValueError: Если передан неизвестный тип или отсутствуют обязательные данные.
        """
        emp_type = emp_type.lower().strip()
        
        # -----------------------------------------------------------------
        # 1. Валидация общих данных
        # -----------------------------------------------------------------
        # Перед созданием любого сотрудника мы обязаны убедиться, 
        # что базовые атрибуты присутствуют в аргументах.
        required_base_fields = ['id', 'name', 'department', 'base_salary']
        for field in required_base_fields:
            if field not in kwargs:
                raise ValueError(
                    f"Ошибка Фабрики: Отсутствует обязательное поле '{field}' "
                    f"для создания сотрудника типа '{emp_type}'."
                )

        # Формируем словарь базовых аргументов для распаковки в конструктор
        base_args = {
            'emp_id': kwargs['id'], 
            'name': kwargs['name'], 
            'department': kwargs['department'], 
            'base_salary': kwargs['base_salary']
        }

        # -----------------------------------------------------------------
        # 2. Инстанцирование конкретных классов
        # -----------------------------------------------------------------
        
        if emp_type == 'employee':
            # Обычный сотрудник не требует дополнительных полей
            return OrdinaryEmployee(**base_args)
        
        elif emp_type == 'manager':
            # Для менеджера ищем 'bonus', если нет — ставим 0.0 по умолчанию
            return Manager(
                **base_args, 
                bonus=kwargs.get('bonus', 0.0)
            )
        
        elif emp_type == 'developer':
            # Разработчик требует уровень и стек технологий.
            # Обратите внимание: при загрузке из JSON ключи словаря kwargs 
            # совпадают с именами аргументов конструктора Developer.
            return Developer(
                **base_args, 
                seniority_level=kwargs.get('seniority', 'junior'),
                tech_stack=kwargs.get('tech_stack', [])
            )
        
        elif emp_type == 'salesperson':
            # Продавец требует комиссию и объем продаж.
            return Salesperson(
                **base_args, 
                commission_rate=kwargs.get('commission', 0.0),
                sales_volume=kwargs.get('sales_volume', 0.0)
            )
        
        else:
            # Если тип не найден в реестре — выбрасываем исключение
            raise ValueError(f"Фабрика не знает, как создать сотрудника типа: '{emp_type}'")
