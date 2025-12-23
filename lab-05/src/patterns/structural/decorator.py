# Decorator (Декоратор)
# ====================
# Динамически добавляет объекту новые обязанности.
# Декораторы предоставляют гибкую альтернативу подклассированию
# для расширения функциональности.

from abc import ABC, abstractmethod
from typing import Optional, List

class EmployeeComponent(ABC):
    """
    Абстрактный компонент для паттерна Decorator.
    Определяет интерфейс для базовых объектов и декораторов.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Получить имя сотрудника."""
        pass
    
    @abstractmethod
    def get_base_salary(self) -> float:
        """Получить базовую зарплату."""
        pass
    
    @abstractmethod
    def get_total_salary(self) -> float:
        """Получить полную зарплату с учетом всех добавлений."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Получить описание сотрудника и его параметров."""
        pass


class ConcreteEmployee(EmployeeComponent):
    """
    Конкретный компонент - базовый сотрудник без дополнительных параметров.
    """
    
    def __init__(self, name: str, base_salary: float):
        """
        Инициализация сотрудника.
        
        Args:
            name: Имя сотрудника
            base_salary: Базовая зарплата
        """
        self._name = name
        self._base_salary = base_salary
        print(f"[Employee] Создан сотрудник: {name}, зарплата: {base_salary}")
    
    def get_name(self) -> str:
        return self._name
    
    def get_base_salary(self) -> float:
        return self._base_salary
    
    def get_total_salary(self) -> float:
        """Полная зарплата - это базовая зарплата."""
        return self._base_salary
    
    def get_description(self) -> str:
        return f"Сотрудник: {self._name}, Базовая зарплата: {self._base_salary}"


class EmployeeDecorator(EmployeeComponent):
    """
    Абстрактный декоратор для добавления функциональности к сотруднику.
    """
    
    def __init__(self, employee: EmployeeComponent):
        """
        Инициализация декоратора.
        
        Args:
            employee: Компонент (другой сотрудник или декоратор), который оборачиваем
        """
        self._employee = employee
    
    def get_name(self) -> str:
        """Возвращает имя вложенного сотрудника."""
        return self._employee.get_name()
    
    def get_base_salary(self) -> float:
        """Возвращает базовую зарплату вложенного сотрудника."""
        return self._employee.get_base_salary()
    
    def get_total_salary(self) -> float:
        """Расширяется в подклассах с добавлением компонентов к зарплате."""
        return self._employee.get_total_salary()
    
    def get_description(self) -> str:
        """Расширяется в подклассах с добавлением описания."""
        return self._employee.get_description()


class BonusDecorator(EmployeeDecorator):
    """
    Декоратор для добавления бонуса к зарплате сотрудника.
    Представляет конкретное добавление функциональности.
    """
    
    def __init__(self, employee: EmployeeComponent, bonus_amount: float):
        """
        Инициализация декоратора с бонусом.
        
        Args:
            employee: Сотрудник для добавления бонуса
            bonus_amount: Размер бонуса
        """
        super().__init__(employee)
        self._bonus_amount = bonus_amount
        print(f"[BonusDecorator] Добавлен бонус {bonus_amount} к сотруднику {employee.get_name()}")
    
    def get_total_salary(self) -> float:
        """Полная зарплата = базовая + бонус."""
        return self._employee.get_total_salary() + self._bonus_amount
    
    def get_description(self) -> str:
        """Описание с добавлением информации о бонусе."""
        return f"{self._employee.get_description()} + Бонус: {self._bonus_amount}"


class PerformanceBonusDecorator(EmployeeDecorator):
    """
    Декоратор для добавления бонуса за производительность.
    Бонус рассчитывается как процент от базовой зарплаты.
    """
    
    def __init__(self, employee: EmployeeComponent, performance_rating: float):
        """
        Инициализация декоратора с рейтингом производительности.
        
        Args:
            employee: Сотрудник
            performance_rating: Рейтинг производительности (0.5 - 2.0)
                               1.0 = норма, > 1.0 = выше нормы
        """
        super().__init__(employee)
        if not (0.5 <= performance_rating <= 2.0):
            raise ValueError(f"Рейтинг должен быть 0.5-2.0: {performance_rating}")
        self._performance_rating = performance_rating
        print(f"[PerformanceBonusDecorator] Добавлен рейтинг {performance_rating} "
              f"для {employee.get_name()}")
    
    def get_total_salary(self) -> float:
        """Полная зарплата = базовая * рейтинг производительности."""
        base = self._employee.get_base_salary()
        performance_bonus = base * (self._performance_rating - 1.0)  # Бонус сверх нормы
        return self._employee.get_total_salary() + performance_bonus
    
    def get_description(self) -> str:
        """Описание с информацией о производительности."""
        return (f"{self._employee.get_description()} + "
                f"Рейтинг производительности: {self._performance_rating}")


class TrainingDecorator(EmployeeDecorator):
    """
    Декоратор для добавления информации о прохождении обучения.
    Сотрудник получает разовую надбавку за повышение квалификации.
    """
    
    def __init__(self, employee: EmployeeComponent, training_type: str, 
                 training_bonus: float = 500):
        """
        Инициализация декоратора с информацией об обучении.
        
        Args:
            employee: Сотрудник
            training_type: Тип обучения (например, 'Python Advanced', 'Leadership')
            training_bonus: Разовая надбавка за обучение
        """
        super().__init__(employee)
        self._training_type = training_type
        self._training_bonus = training_bonus
        print(f"[TrainingDecorator] Добавлено обучение '{training_type}' "
              f"(бонус {training_bonus}) для {employee.get_name()}")
    
    def get_total_salary(self) -> float:
        """Полная зарплата = базовая + бонус за обучение."""
        return self._employee.get_total_salary() + self._training_bonus
    
    def get_description(self) -> str:
        """Описание с информацией об обучении."""
        return (f"{self._employee.get_description()} + "
                f"Обучение: {self._training_type} ({self._training_bonus})")


class ProjExperienceDecorator(EmployeeDecorator):
    """
    Декоратор для добавления надбавки за опыт работы над проектами.
    За каждый завершённый проект сотрудник получает небольшой процент.
    """
    
    def __init__(self, employee: EmployeeComponent, 
                 completed_projects: int, per_project_bonus: float = 100):
        """
        Инициализация декоратора с проектным опытом.
        
        Args:
            employee: Сотрудник
            completed_projects: Количество завершённых проектов
            per_project_bonus: Бонус за каждый проект
        """
        super().__init__(employee)
        self._completed_projects = completed_projects
        self._per_project_bonus = per_project_bonus
        print(f"[ProjExperienceDecorator] Добавлен опыт "
              f"({completed_projects} проектов) для {employee.get_name()}")
    
    def get_total_salary(self) -> float:
        """Полная зарплата = базовая + бонус за проекты."""
        project_bonus = self._completed_projects * self._per_project_bonus
        return self._employee.get_total_salary() + project_bonus
    
    def get_description(self) -> str:
        """Описание с информацией о проектах."""
        project_bonus = self._completed_projects * self._per_project_bonus
        return (f"{self._employee.get_description()} + "
                f"Опыт проектов: {self._completed_projects} "
                f"(бонус {project_bonus})")


class VacationBenefitDecorator(EmployeeDecorator):
    """
    Декоратор для добавления выплаты за неиспользованный отпуск.
    """
    
    def __init__(self, employee: EmployeeComponent, 
                 unused_vacation_days: int, daily_rate: float = 50):
        """
        Инициализация декоратора с информацией об отпуске.
        
        Args:
            employee: Сотрудник
            unused_vacation_days: Количество неиспользованных дней отпуска
            daily_rate: Стоимость одного дня отпуска
        """
        super().__init__(employee)
        self._unused_vacation_days = unused_vacation_days
        self._daily_rate = daily_rate
        print(f"[VacationBenefitDecorator] Добавлена выплата за отпуск "
              f"({unused_vacation_days} дней) для {employee.get_name()}")
    
    def get_total_salary(self) -> float:
        """Полная зарплата = базовая + выплата за отпуск."""
        vacation_payment = self._unused_vacation_days * self._daily_rate
        return self._employee.get_total_salary() + vacation_payment
    
    def get_description(self) -> str:
        """Описание с информацией об отпуске."""
        vacation_payment = self._unused_vacation_days * self._daily_rate
        return (f"{self._employee.get_description()} + "
                f"Выплата за отпуск: {self._unused_vacation_days} дней ({vacation_payment})")


# ===== ИСПОЛЬЗОВАНИЕ ДЕКОРАТОРОВ =====
class DecoratorDemonstration:
    """
    Демонстрация работы паттерна Decorator.
    """
    
    @staticmethod
    def demonstrate_single_decorator():
        """Пример с одним декоратором."""
        print("\n=== Пример 1: Один декоратор ===\n")
        
        # Создаём базового сотрудника
        employee = ConcreteEmployee("John Doe", 5000)
        print(f"Зарплата: {employee.get_total_salary()}\n")
        
        # Добавляем бонус
        employee_with_bonus = BonusDecorator(employee, 1000)
        print(f"Зарплата с бонусом: {employee_with_bonus.get_total_salary()}\n")
    
    @staticmethod
    def demonstrate_multiple_decorators():
        """Пример с несколькими декораторами (stacking)."""
        print("\n=== Пример 2: Несколько декораторов (stacking) ===\n")
        
        # Создаём базового сотрудника
        employee = ConcreteEmployee("Alice Smith", 6000)
        print(f"Начальная зарплата: {employee.get_total_salary()}")
        
        # Добавляем декораторы последовательно (декоратор обёртывает предыдущий)
        employee = PerformanceBonusDecorator(employee, 1.2)  # +20% за производительность
        print(f"После бонуса производительности: {employee.get_total_salary()}")
        
        employee = TrainingDecorator(employee, "Advanced Python", 500)
        print(f"После обучения: {employee.get_total_salary()}")
        
        employee = ProjExperienceDecorator(employee, 3, 200)  # 3 проекта по 200 каждый
        print(f"После учёта проектного опыта: {employee.get_total_salary()}")
        
        employee = VacationBenefitDecorator(employee, 5, 100)  # 5 дней отпуска по 100
        print(f"После выплаты за отпуск: {employee.get_total_salary()}\n")
        
        # Полное описание
        print(f"Описание:\n{employee.get_description()}\n")
