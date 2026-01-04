# Behavioral Patterns (Поведенческие паттерны)
# ============================================
# Observer (Наблюдатель), Strategy (Стратегия), Command (Команда)

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime


# ======================== OBSERVER (НАБЛЮДАТЕЛЬ) ========================

class Observer(ABC):
    """
    Абстрактный класс для наблюдателей.
    Определяет интерфейс для получения уведомлений об изменениях.
    """
    
    @abstractmethod
    def update(self, subject: 'Subject', event_data: Dict[str, Any]) -> None:
        """
        Метод обновления, вызываемый при изменении в Subject.
        
        Args:
            subject: Объект, за которым наблюдаем
            event_data: Данные о событии
        """
        pass


class Subject(ABC):
    """
    Абстрактный класс для объектов, за которыми наблюдают (Subject).
    """
    
    def __init__(self):
        """Инициализация списка наблюдателей."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """
        Подписать наблюдателя на события.
        
        Args:
            observer: Объект наблюдателя
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[Subject] Наблюдатель {observer.__class__.__name__} подписан")
    
    def detach(self, observer: Observer) -> None:
        """
        Отписать наблюдателя от событий.
        
        Args:
            observer: Объект наблюдателя
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[Subject] Наблюдатель {observer.__class__.__name__} отписан")
    
    def notify(self, event_data: Dict[str, Any]) -> None:
        """
        Уведомить всех наблюдателей об изменении.
        
        Args:
            event_data: Данные события
        """
        print(f"[Subject] Отправка уведомления {len(self._observers)} наблюдателям...")
        for observer in self._observers:
            observer.update(self, event_data)


class EmployeeSalarySubject(Subject):
    """
    Subject - объект, за которым наблюдают.
    Представляет зарплату сотрудника.
    """
    
    def __init__(self, emp_id: int, name: str, salary: float):
        """Инициализация сотрудника."""
        super().__init__()
        self.emp_id = emp_id
        self.name = name
        self._salary = salary
    
    @property
    def salary(self) -> float:
        return self._salary
    
    @salary.setter
    def salary(self, new_salary: float) -> None:
        """Установка новой зарплаты с уведомлением наблюдателей."""
        if new_salary != self._salary:
            old_salary = self._salary
            self._salary = new_salary
            
            # Уведомляем наблюдателей
            self.notify({
                'event': 'salary_changed',
                'employee_id': self.emp_id,
                'employee_name': self.name,
                'old_salary': old_salary,
                'new_salary': new_salary,
                'change': new_salary - old_salary,
                'timestamp': datetime.now().isoformat(),
            })


class EmailNotificationObserver(Observer):
    """Наблюдатель - отправляет уведомления по email."""
    
    def update(self, subject: Subject, event_data: Dict[str, Any]) -> None:
        """Отправка email при изменении зарплаты."""
        if event_data['event'] == 'salary_changed':
            print(f"\n[EmailObserver] EMAIL: Зарплата сотрудника {event_data['employee_name']} "
                  f"изменена с {event_data['old_salary']} на {event_data['new_salary']}")


class LoggingObserver(Observer):
    """Наблюдатель - логирует изменения."""
    
    def __init__(self, log_file: str = "salary_changes.log"):
        """Инициализация с файлом логов."""
        self.log_file = log_file
        self.log_entries: List[str] = []
    
    def update(self, subject: Subject, event_data: Dict[str, Any]) -> None:
        """Логирование изменения."""
        if event_data['event'] == 'salary_changed':
            log_entry = (f"{event_data['timestamp']} | "
                        f"{event_data['employee_name']}: "
                        f"{event_data['old_salary']} -> {event_data['new_salary']} "
                        f"(Δ {event_data['change']:+.2f})")
            self.log_entries.append(log_entry)
            print(f"[LoggingObserver] LOG: {log_entry}")


class AuditObserver(Observer):
    """Наблюдатель - ведёт аудит всех изменений."""
    
    def __init__(self):
        """Инициализация аудита."""
        self.audit_log: List[Dict[str, Any]] = []
    
    def update(self, subject: Subject, event_data: Dict[str, Any]) -> None:
        """Добавление записи в аудит-лог."""
        self.audit_log.append(event_data)
        print(f"[AuditObserver] AUDIT: Запись #{len(self.audit_log)} добавлена в аудит-лог")


class NotificationSystem:
    """
    Система уведомлений.
    Управляет наблюдателями и сотрудниками.
    """
    
    def __init__(self):
        """Инициализация системы."""
        self.employees: Dict[int, EmployeeSalarySubject] = {}
        self.observers: List[Observer] = []
    
    def register_observer(self, observer: Observer) -> None:
        """Регистрация глобального наблюдателя."""
        self.observers.append(observer)
        print(f"[NotificationSystem] Наблюдатель {observer.__class__.__name__} зарегистрирован")
    
    def add_employee(self, emp_id: int, name: str, salary: float) -> None:
        """Добавление сотрудника в систему."""
        employee = EmployeeSalarySubject(emp_id, name, salary)
        
        # Подписываем всех глобальных наблюдателей
        for observer in self.observers:
            employee.attach(observer)
        
        self.employees[emp_id] = employee
        print(f"[NotificationSystem] Сотрудник {name} добавлен в систему")
    
    def update_salary(self, emp_id: int, new_salary: float) -> None:
        """Обновление зарплаты сотрудника."""
        if emp_id in self.employees:
            self.employees[emp_id].salary = new_salary
        else:
            print(f"[NotificationSystem] Сотрудник {emp_id} не найден")


# ======================== STRATEGY (СТРАТЕГИЯ) ========================

class BonusStrategy(ABC):
    """
    Абстрактная стратегия расчета бонуса.
    """
    
    @abstractmethod
    def calculate_bonus(self, base_salary: float, **kwargs) -> float:
        """
        Расчет бонуса.
        
        Args:
            base_salary: Базовая зарплата
            **kwargs: Дополнительные параметры для расчета
            
        Returns:
            Размер бонуса
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Описание стратегии."""
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """Стратегия бонуса за производительность."""
    
    def calculate_bonus(self, base_salary: float, performance_rating: float = 1.0) -> float:
        """
        Бонус = базовая зарплата * (рейтинг - 1.0)
        
        Args:
            base_salary: Базовая зарплата
            performance_rating: Рейтинг производительности (0.5 - 2.0)
            
        Returns:
            Размер бонуса
        """
        # Бонус только если рейтинг > 1.0
        if performance_rating > 1.0:
            bonus = base_salary * (performance_rating - 1.0)
            print(f"[PerformanceStrategy] Бонус за производительность ({performance_rating}): {bonus}")
            return bonus
        return 0.0
    
    def get_description(self) -> str:
        return "Бонус за производительность"


class SeniorityBonusStrategy(BonusStrategy):
    """Стратегия бонуса за стаж."""
    
    def calculate_bonus(self, base_salary: float, years_of_service: int = 0) -> float:
        """
        Бонус = базовая зарплата * (лет стажа * 2%)
        
        Args:
            base_salary: Базовая зарплата
            years_of_service: Количество лет работы
            
        Returns:
            Размер бонуса
        """
        bonus_rate = min(years_of_service * 0.02, 0.20)  # Максимум 20%
        bonus = base_salary * bonus_rate
        print(f"[SeniorityStrategy] Бонус за стаж ({years_of_service} лет): {bonus}")
        return bonus
    
    def get_description(self) -> str:
        return "Бонус за стаж"


class ProjectBonusStrategy(BonusStrategy):
    """Стратегия бонуса за завершённые проекты."""
    
    def calculate_bonus(self, base_salary: float, projects_completed: int = 0) -> float:
        """
        Бонус = базовая зарплата * 5% за каждый проект
        
        Args:
            base_salary: Базовая зарплата
            projects_completed: Количество завершённых проектов
            
        Returns:
            Размер бонуса
        """
        bonus_rate = min(projects_completed * 0.05, 0.30)  # Максимум 30%
        bonus = base_salary * bonus_rate
        print(f"[ProjectStrategy] Бонус за проекты ({projects_completed} шт): {bonus}")
        return bonus
    
    def get_description(self) -> str:
        return "Бонус за проекты"


class EmployeeWithStrategy:
    """Сотрудник, использующий стратегию расчета бонуса."""
    
    def __init__(self, name: str, base_salary: float):
        """Инициализация сотрудника."""
        self.name = name
        self.base_salary = base_salary
        self._strategy: Optional[BonusStrategy] = None
    
    def set_bonus_strategy(self, strategy: BonusStrategy) -> None:
        """Установить стратегию бонуса."""
        self._strategy = strategy
        print(f"[Employee] Для {self.name} установлена стратегия: {strategy.get_description()}")
    
    def calculate_total_salary(self, **strategy_params) -> float:
        """
        Расчет полной зарплаты.
        
        Args:
            **strategy_params: Параметры для стратегии
            
        Returns:
            Полная зарплата (базовая + бонус)
        """
        if self._strategy is None:
            print(f"[Employee] Для {self.name} стратегия не установлена")
            return self.base_salary
        
        bonus = self._strategy.calculate_bonus(self.base_salary, **strategy_params)
        total = self.base_salary + bonus
        print(f"[Employee] {self.name}: базовая {self.base_salary} + "
              f"бонус {bonus} = итого {total}")
        return total


# ======================== COMMAND (КОМАНДА) ========================

class Command(ABC):
    """Абстрактная команда."""
    
    @abstractmethod
    def execute(self) -> None:
        """Выполнение команды."""
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Отмена команды (откат)."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Описание команды."""
        pass


class HireEmployeeCommand(Command):
    """Команда для найма сотрудника."""
    
    def __init__(self, employee_name: str, department: str, salary: float):
        """Инициализация команды."""
        self.employee_name = employee_name
        self.department = department
        self.salary = salary
        self._executed = False
    
    def execute(self) -> None:
        """Выполнение найма."""
        print(f"[HireCommand] Нанимаем {self.employee_name} в {self.department}")
        # Здесь была бы фактическая реализация найма
        self._executed = True
    
    def undo(self) -> None:
        """Отмена найма (увольнение)."""
        if self._executed:
            print(f"[HireCommand] Отмена: увольняем {self.employee_name}")
            self._executed = False
    
    def get_description(self) -> str:
        return f"Найм {self.employee_name}"


class UpdateSalaryCommand(Command):
    """Команда для изменения зарплаты."""
    
    def __init__(self, employee_name: str, old_salary: float, new_salary: float):
        """Инициализация команды."""
        self.employee_name = employee_name
        self.old_salary = old_salary
        self.new_salary = new_salary
    
    def execute(self) -> None:
        """Изменение зарплаты."""
        print(f"[UpdateSalaryCommand] Изменяем зарплату {self.employee_name}: "
              f"{self.old_salary} -> {self.new_salary}")
    
    def undo(self) -> None:
        """Откат изменения зарплаты."""
        print(f"[UpdateSalaryCommand] Откат: восстанавливаем зарплату {self.employee_name}: "
              f"{self.new_salary} -> {self.old_salary}")
    
    def get_description(self) -> str:
        return f"Изменение зарплаты {self.employee_name}"


class PromoteEmployeeCommand(Command):
    """Команда для повышения в должности."""
    
    def __init__(self, employee_name: str, old_position: str, new_position: str,
                 salary_increase: float):
        """Инициализация команды."""
        self.employee_name = employee_name
        self.old_position = old_position
        self.new_position = new_position
        self.salary_increase = salary_increase
    
    def execute(self) -> None:
        """Повышение в должности."""
        print(f"[PromoteCommand] Повышаем {self.employee_name}: "
              f"{self.old_position} -> {self.new_position} (+{self.salary_increase})")
    
    def undo(self) -> None:
        """Откат повышения."""
        print(f"[PromoteCommand] Откат: возвращаем {self.employee_name} на должность "
              f"{self.old_position}")
    
    def get_description(self) -> str:
        return f"Повышение {self.employee_name}"


class CommandInvoker:
    """
    Invoker - выполняет команды и может откатывать их.
    """
    
    def __init__(self):
        """Инициализация invoker."""
        self._history: List[Command] = []
        self._undo_stack: List[Command] = []
    
    def execute_command(self, command: Command) -> None:
        """
        Выполнить команду.
        
        Args:
            command: Команда для выполнения
        """
        print(f"\n[Invoker] Выполнение: {command.get_description()}")
        command.execute()
        self._history.append(command)
        self._undo_stack.clear()  # Очищаем undo при новой команде
    
    def undo(self) -> None:
        """Откатить последнюю команду."""
        if self._history:
            command = self._history.pop()
            print(f"\n[Invoker] Откат: {command.get_description()}")
            command.undo()
            self._undo_stack.append(command)
        else:
            print("[Invoker] Нет команд для отката")
    
    def redo(self) -> None:
        """Повторить последнюю отменённую команду."""
        if self._undo_stack:
            command = self._undo_stack.pop()
            print(f"\n[Invoker] Повтор: {command.get_description()}")
            command.execute()
            self._history.append(command)
        else:
            print("[Invoker] Нет команд для повтора")
    
    def get_history(self) -> List[str]:
        """Получить историю команд."""
        return [cmd.get_description() for cmd in self._history]
