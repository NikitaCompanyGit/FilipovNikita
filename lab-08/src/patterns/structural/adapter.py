# Adapter (Адаптер)
# =================
# Преобразует интерфейс класса в другой интерфейс, ожидаемый клиентами.
# Позволяет работать вместе классам с несовместимыми интерфейсами.

from abc import ABC, abstractmethod
from typing import List, Dict, Any

# ===== ВНЕШНЯЯ СИСТЕМА (которую мы адаптируем) =====
class ExternalSalaryCalculationService:
    """
    Внешняя система расчета зарплат (несовместимый интерфейс).
    Это может быть сервис от другой компании или библиотека.
    """
    
    def calculate_monthly_payment(self, employee_data: Dict[str, Any]) -> float:
        """
        Метод расчета зарплаты (непривычный интерфейс для нашей системы).
        
        Args:
            employee_data: Словарь с данными сотрудника
                          {'base': зарплата, 'multiplier': коэффициент}
            
        Returns:
            Размер месячного платежа
        """
        base_salary = employee_data.get('base', 0)
        multiplier = employee_data.get('multiplier', 1.0)
        
        # Внешний сервис применяет свою логику
        commission = base_salary * multiplier * 0.05  # 5% комиссия сервиса
        result = (base_salary * multiplier) - commission
        
        print(f"[ExternalService] Расчет: base={base_salary}, "
              f"multiplier={multiplier}, result={result}")
        
        return result


class LegacySalaryCalculator:
    """
    Устаревшая система расчета зарплат (ещё один несовместимый интерфейс).
    """
    
    def get_total_compensation(self, employee_id: int, emp_type: str, 
                             salary_amount: float) -> float:
        """
        Расчет общей компенсации через устаревший интерфейс.
        
        Args:
            employee_id: ID сотрудника
            emp_type: Тип сотрудника ('MGR', 'DEV', 'SALES')
            salary_amount: Размер зарплаты
            
        Returns:
            Общая компенсация
        """
        type_bonuses = {
            'MGR': 0.2,      # Менеджеры получают 20% бонус
            'DEV': 0.15,     # Разработчики получают 15% бонус
            'SALES': 0.25,   # Продавцы получают 25% бонус
        }
        
        bonus_rate = type_bonuses.get(emp_type, 0.0)
        total = salary_amount * (1 + bonus_rate)
        
        print(f"[LegacyCalculator] ID={employee_id}, type={emp_type}, "
              f"total_with_bonus={total}")
        
        return total


# ===== НАША СИСТЕМА (интерфейс, ожидаемый нашей системой) =====
class SalaryCalculator(ABC):
    """
    Интерфейс для расчета зарплаты в нашей системе.
    Все калькуляторы должны реализовать этот интерфейс.
    """
    
    @abstractmethod
    def calculate_salary(self, employee: Dict[str, Any]) -> float:
        """
        Расчет зарплаты сотрудника.
        
        Args:
            employee: Словарь с данными сотрудника
                     {'id', 'name', 'department', 'base_salary', 'type', ...}
            
        Returns:
            Размер зарплаты
        """
        pass


# ===== АДАПТЕРЫ =====
class ExternalServiceAdapter(SalaryCalculator):
    """
    Адаптер для преобразования ExternalSalaryCalculationService
    к интерфейсу SalaryCalculator.
    """
    
    def __init__(self, external_service: ExternalSalaryCalculationService):
        """
        Инициализация адаптера с внешним сервисом.
        
        Args:
            external_service: Объект ExternalSalaryCalculationService
        """
        self.external_service = external_service
        print("[Adapter] ExternalServiceAdapter инициализирован")
    
    def calculate_salary(self, employee: Dict[str, Any]) -> float:
        """
        Расчет зарплаты через адаптер.
        Преобразует данные сотрудника в формат, ожидаемый внешним сервисом.
        
        Args:
            employee: Данные сотрудника в нашем формате
            
        Returns:
            Размер зарплаты
        """
        print(f"\n[Adapter] Адаптирование данных для ExternalService...")
        
        # Преобразование данных из нашего формата в формат внешнего сервиса
        external_format = {
            'base': employee.get('base_salary', 0),
            'multiplier': self._get_multiplier_by_type(employee.get('type', 'employee'))
        }
        
        # Вызов внешнего сервиса
        result = self.external_service.calculate_monthly_payment(external_format)
        
        # Преобразование результата обратно в наш формат (если нужно)
        return result
    
    def _get_multiplier_by_type(self, emp_type: str) -> float:
        """
        Преобразование типа сотрудника в коэффициент для внешнего сервиса.
        
        Args:
            emp_type: Тип сотрудника ('manager', 'developer', 'salesperson', 'employee')
            
        Returns:
            Коэффициент для расчета
        """
        multipliers = {
            'manager': 1.3,
            'developer': 1.5,
            'salesperson': 1.2,
            'employee': 1.0,
        }
        return multipliers.get(emp_type, 1.0)


class LegacyCalculatorAdapter(SalaryCalculator):
    """
    Адаптер для преобразования LegacySalaryCalculator
    к интерфейсу SalaryCalculator.
    """
    
    def __init__(self, legacy_calculator: LegacySalaryCalculator):
        """
        Инициализация адаптера с устаревшим калькулятором.
        
        Args:
            legacy_calculator: Объект LegacySalaryCalculator
        """
        self.legacy_calculator = legacy_calculator
        print("[Adapter] LegacyCalculatorAdapter инициализирован")
    
    def calculate_salary(self, employee: Dict[str, Any]) -> float:
        """
        Расчет зарплаты через адаптер.
        Преобразует данные сотрудника в формат устаревшей системы.
        
        Args:
            employee: Данные сотрудника в нашем формате
            
        Returns:
            Размер зарплаты
        """
        print(f"\n[Adapter] Адаптирование данных для LegacyCalculator...")
        
        # Преобразование типа сотрудника
        emp_type_legacy = self._convert_type_to_legacy(employee.get('type', 'employee'))
        
        # Вызов устаревшего калькулятора
        result = self.legacy_calculator.get_total_compensation(
            employee.get('id', 0),
            emp_type_legacy,
            employee.get('base_salary', 0)
        )
        
        return result
    
    def _convert_type_to_legacy(self, emp_type: str) -> str:
        """
        Преобразование типа сотрудника в формат устаревшей системы.
        
        Args:
            emp_type: Тип сотрудника в нашем формате
            
        Returns:
            Тип сотрудника в формате устаревшей системы
        """
        type_mapping = {
            'manager': 'MGR',
            'developer': 'DEV',
            'salesperson': 'SALES',
            'employee': 'EMP',
        }
        return type_mapping.get(emp_type, 'EMP')


# ===== ИСПОЛЬЗОВАНИЕ АДАПТЕРОВ В НАШЕЙ СИСТЕМЕ =====
class CompanySalaryManager:
    """
    Менеджер зарплат в нашей системе.
    Может использовать разные калькуляторы через единый интерфейс.
    """
    
    def __init__(self, calculator: SalaryCalculator):
        """
        Инициализация менеджера с калькулятором.
        
        Args:
            calculator: Объект, реализующий интерфейс SalaryCalculator
        """
        self.calculator = calculator
    
    def calculate_employee_salary(self, employee: Dict[str, Any]) -> float:
        """
        Расчет зарплаты сотрудника.
        
        Args:
            employee: Данные сотрудника
            
        Returns:
            Размер зарплаты
        """
        return self.calculator.calculate_salary(employee)
    
    def set_calculator(self, calculator: SalaryCalculator) -> None:
        """
        Замена калькулятора (например, для использования другого сервиса).
        
        Args:
            calculator: Новый калькулятор
        """
        self.calculator = calculator
        print(f"[SalaryManager] Калькулятор заменен на {calculator.__class__.__name__}")
    
    def calculate_payroll(self, employees: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Расчет зарплаты для списка сотрудников.
        
        Args:
            employees: Список сотрудников
            
        Returns:
            Словарь: имя сотрудника -> размер зарплаты
        """
        payroll = {}
        total = 0
        
        print(f"\n[SalaryManager] Расчет зарплаты для {len(employees)} сотрудников...")
        
        for employee in employees:
            salary = self.calculate_employee_salary(employee)
            payroll[employee.get('name', 'Unknown')] = salary
            total += salary
        
        print(f"[SalaryManager] Итого к выплате: {total}")
        
        return payroll
