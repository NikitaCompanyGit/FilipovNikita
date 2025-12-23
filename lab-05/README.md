# Лабораторная работа №5: Применение паттернов проектирования

## Описание

Данная лабораторная работа представляет собой комплексный рефакторинг системы учета сотрудников из ЛР №4 с применением 9 паттернов проектирования для повышения гибкости, расширяемости и модульности системы:

1. **Порождающие паттерны** (3) - управление созданием объектов
2. **Структурные паттерны** (3) - организация отношений между объектами
3. **Поведенческие паттерны** (3) - определение взаимодействия между объектами

## Структура проекта

```
project_root/
├── src/                          # Исходный код системы
│   ├── base/                     # Базовые классы (из ЛР4)
│   │   ├── employee.py
│   │   ├── abstract_employee.py
│   │   └── exceptions.py
│   │
│   ├── specialists/              # Типы сотрудников (из ЛР4)
│   │   ├── manager.py
│   │   ├── developer.py
│   │   ├── salesperson.py
│   │   └── ordinary_employee.py
│   │
│   ├── organization/             # Управление структурами (из ЛР4)
│   │   ├── department.py
│   │   ├── project.py
│   │   └── company.py
│   │
│   ├── factory.py                # EmployeeFactory (рефакторенная)
│   │
│   ├── patterns/                 # Реализации паттернов (новое!)
│   │   ├── __init__.py
│   │   ├── singleton.py          # Singleton - DatabaseConnection
│   │   ├── builder.py            # Builder - EmployeeBuilder
│   │   ├── strategy.py           # Strategy - BonusStrategy
│   │   ├── observer.py           # Observer - NotificationSystem
│   │   ├── command.py            # Command - HireEmployeeCommand
│   │   ├── decorator.py          # Decorator - BonusDecorator, TaxDecorator
│   │   ├── adapter.py            # Adapter - SalaryCalculatorAdapter
│   │   └── facade.py             # Facade - CompanyFacade
│   │
│   └── utils/                    # Вспомогательные модули
│       ├── comparators.py
│       └── validators.py
│
├── examples/                     # Примеры и тесты
│   ├── test_patterns_lr8_part5.py    # 30+ тестов паттернов
│   └── demo_patterns.py              # Демонстрация паттернов
│
├── main.py                       # Test Runner
├── README.md                     # Документация
└── docs/                         # Документация и отчеты
    └── patterns_guide.md         # Справочник по паттернам
```

## Реализованные паттерны

### 1️⃣ ПОРОЖДАЮЩИЕ ПАТТЕРНЫ

#### **Singleton** (`patterns/singleton.py`)
Гарантирует единственный экземпляр класса и предоставляет глобальную точку доступа.

```python
class DatabaseConnection:
    __instance = None
    __lock = threading.Lock()
    
    def __new__(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance

# Использование
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # Один и тот же объект!
```

**Используется для:** управление подключением к БД, конфигурация системы

#### **Builder** (`patterns/builder.py`)
Разделяет конструирование сложного объекта от его представления, позволяя пошаговое создание.

```python
emp = (EmployeeBuilder()
    .set_id(1)
    .set_name("Alice")
    .set_department("IT")
    .set_base_salary(5000)
    .add_param("type", "developer")
    .add_param("level", "senior")
    .add_param("skills", ["Python", "Go"])
    .build())
```

**Используется для:** создание сложных сотрудников с множеством параметров

#### **Factory Method** (рефакторенная в `factory.py`)
Определяет интерфейс для создания объекта, но оставляет подклассам решение о том, какой класс инстанцировать.

```python
emp = EmployeeFactory.create_employee(
    "developer",
    emp_id=1,
    name="Bob",
    department="IT",
    base_salary=5000,
    level="senior"
)
```

**Используется для:** централизованное создание разных типов сотрудников

---

### 2️⃣ СТРУКТУРНЫЕ ПАТТЕРНЫ

#### **Decorator** (`patterns/decorator.py`)
Динамически добавляет новую функциональность к объекту, оборачивая его в декоратор.

```python
developer = Developer(1, "Alice", "IT", 5000, "senior", ["Python"])
# Зарплата: 5000 * 2 = 10000

with_bonus = BonusDecorator(developer, 1000)
# 10000 + 1000 = 11000

with_tax = TaxDecorator(with_bonus, 0.13)
# 11000 * 0.87 = 9570

print(with_tax.calculate_salary())  # 9570
```

**Используется для:** добавление бонусов, налогов, тренингов к зарплате

#### **Adapter** (`patterns/adapter.py`)
Преобразует интерфейс класса в другой интерфейс, ожидаемый клиентами.

```python
class OldSalaryCalculator:
    def get_gross_salary(self, base, params):
        return base * 1.2

adapted = SalaryCalculatorAdapter(employee, old_calculator)
salary = adapted.calculate_salary()  # Работает с новым интерфейсом
```

**Используется для:** интеграция со старыми системами расчета зарплат

#### **Facade** (`patterns/facade.py`)
Предоставляет унифицированный интерфейс к набору интерфейсов в подсистеме.

```python
facade = CompanyFacade(company)

# Быстрый найм одной функцией
facade.hire_employee_quick("developer", "Charlie", "IT", 5000)

# Безопасное увольнение
facade.fire_employee_safe(1)

# Статистика по отделу
stats = facade.get_department_stats("IT")
```

**Используется для:** упрощение работы с компанией

---

### 3️⃣ ПОВЕДЕНЧЕСКИЕ ПАТТЕРНЫ

#### **Strategy** (`patterns/strategy.py`)
Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.

```python
class BonusStrategy(ABC):
    @abstractmethod
    def calculate_bonus(self, salary: float) -> float:
        pass

class BasicBonusStrategy(BonusStrategy):
    def calculate_bonus(self, salary):
        return salary * 0.1

class SeniorBonusStrategy(BonusStrategy):
    def calculate_bonus(self, salary):
        return salary * 0.2

# Использование
strategy = SeniorBonusStrategy()
bonus = strategy.calculate_bonus(5000)  # 1000
```

**Используется для:** разные алгоритмы расчета бонусов (базовый, старший, по производительности)

#### **Observer** (`patterns/observer.py`)
Определяет зависимость один-ко-многим между объектами таким образом, чтобы при изменении состояния одного объекта все зависящие от него объекты уведомлялись об этом.

```python
emp = Employee(1, "Alice", "IT", 5000)
observer = EmployeeNotificationObserver()

emp.attach(observer)
emp.base_salary = 6000  # notify() будет вызван
# Вывод: ✉ Зарплата Alice изменилась
```

**Используется для:** система уведомлений об изменении зарплаты, отдела

#### **Command** (`patterns/command.py`)
Инкапсулирует запрос как объект, позволяя параметризовать клиентов с различными запросами, ставить запросы в очередь, регистрировать запросы и поддерживать отмену операций.

```python
history = []

hire_cmd = HireEmployeeCommand(company, developer)
hire_cmd.execute()
history.append(hire_cmd)

# Отмена последней операции
history[-1].undo()
```

**Используется для:** истории операций, отмена действий (undo/redo)

---

## Использование

### Запуск демонстрации паттернов

```bash
python examples/demo_patterns.py
```

### Запуск тестов паттернов

```bash
python main.py tests part5        # 30+ тестов паттернов
python main.py tests coverage     # С покрытием кода
```

### Пример использования всех паттернов вместе

```python
from src.organization.company import Company
from src.patterns.builder import EmployeeBuilder
from src.patterns.facade import CompanyFacade
from src.patterns.decorator import BonusDecorator, TaxDecorator

# 1. Создание компании
company = Company("MegaCorp")

# 2. Использование Facade
facade = CompanyFacade(company)

# 3. Использование Builder
developer = (EmployeeBuilder()
    .set_id(1)
    .set_name("Alice")
    .set_department("IT")
    .set_base_salary(5000)
    .add_param("type", "developer")
    .add_param("level", "senior")
    .build())

# 4. Использование Decorator
with_bonus = BonusDecorator(developer, 2000)
final_emp = TaxDecorator(with_bonus, 0.13)

print(final_emp.calculate_salary())  # 10440

# 5. Использование Singleton
from src.patterns.singleton import DatabaseConnection
db = DatabaseConnection()
db.query("SELECT * FROM employees")
```

## Результаты тестирования

| Паттерн | Описание | Статус |
|---------|---------|--------|
| Singleton | Единственный экземпляр БД | ✅ PASSED |
| Builder | Пошаговое создание объектов | ✅ PASSED |
| Factory | Создание разных типов | ✅ PASSED |
| Decorator | Наслаивание функциональности | ✅ PASSED |
| Strategy | Разные алгоритмы | ✅ PASSED |
| Observer | Система уведомлений | ✅ PASSED |
| Command | История операций | ✅ PASSED |
| Adapter | Интеграция со старым кодом | ✅ PASSED |
| Facade | Упрощенный API | ✅ PASSED |
| **Итого** | **30+ тестов** | **✅ 100%** |

## Ключевые особенности

✅ **9 паттернов проектирования** - полный спектр порождающих, структурных и поведенческих  
✅ **Гибкая архитектура** - легко добавлять новые типы сотрудников и операции  
✅ **Расширяемость** - паттерны позволяют расширять функциональность без изменения существующего кода  
✅ **Комбинируемость** - паттерны работают хорошо вместе  
✅ **Тестируемость** - каждый паттерн покрыт тестами  

## Преимущества использования паттернов

| Паттерн | Преимущество |
|---------|-------------|
| **Singleton** | Единственный контролируемый доступ к ресурсу |
| **Builder** | Читаемый код через chaining |
| **Factory** | Централизованное создание объектов |
| **Decorator** | Динамическое добавление функциональности |
| **Strategy** | Инкапсуляция алгоритмов |
| **Observer** | Слабая связь между объектами |
| **Command** | Инкапсуляция операций |
| **Adapter** | Интеграция несовместимых интерфейсов |
| **Facade** | Упрощение сложных систем |

## Требования

- Python 3.8+
- Стандартная библиотека Python (abc, threading)
- pytest (для запуска тестов)

## Возможности развития

- Добавление новых паттернов (Template Method, Chain of Responsibility)
- Интеграция с веб-фреймворком
- REST API с использованием паттернов
- Сохранение истории операций в БД
- Расширенная система отчетности с использованием паттернов

---

**Автор:** [Филиппов Никита Сергеевич]  
**Группа:** [ПИН-б-0-24-2]  
**Дата:** 29.12.2025  
**Статус:** ✅ ВЫПОЛНЕНА
