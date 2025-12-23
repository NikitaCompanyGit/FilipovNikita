# Singleton (Одиночка) - Управление единственным подключением к БД SQLite
# ============================================================================
# Гарантирует, что класс имеет только один экземпляр и предоставляет
# глобальную точку доступа к этому экземпляру.

import sqlite3
from typing import Optional

class DatabaseConnection:
    """
    Реализация паттерна Singleton для управления подключением к БД.
    Гарантирует единственное подключение к SQLite на протяжении жизни приложения.
    """
    
    # Класс-переменная для хранения единственного экземпляра
    _instance: Optional['DatabaseConnection'] = None
    # Флаг инициализации (для потокобезопасности)
    _initialized: bool = False
    
    def __new__(cls) -> 'DatabaseConnection':
        """
        Переопределение __new__ для создания единственного экземпляра.
        При повторном вызове возвращает существующий экземпляр.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, db_path: str = "company.db"):
        """
        Инициализация подключения (вызывается только один раз).
        
        Args:
            db_path: Путь к файлу БД SQLite
        """
        # Защита от повторной инициализации
        if not DatabaseConnection._initialized:
            self.db_path = db_path
            self.connection: Optional[sqlite3.Connection] = None
            self._connect()
            DatabaseConnection._initialized = True
    
    def _connect(self) -> None:
        """Установка подключения к БД SQLite."""
        try:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False  # Для простоты, в production используйте потокобезопасные подключения
            )
            # Включаем внешние ключи
            self.connection.execute("PRAGMA foreign_keys = ON")
            print(f"[DB] Подключение к '{self.db_path}' установлено")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Ошибка подключения: {e}")
            raise
    
    @classmethod
    def get_instance(cls, db_path: str = "company.db") -> 'DatabaseConnection':
        """
        Класс-метод для получения единственного экземпляра.
        
        Args:
            db_path: Путь к БД (используется только при первом вызове)
            
        Returns:
            Единственный экземпляр DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Получение активного подключения к БД.
        
        Returns:
            Объект подключения sqlite3.Connection
        """
        if self.connection is None:
            raise RuntimeError("Подключение к БД не установлено")
        return self.connection
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Выполнение SELECT запроса.
        
        Args:
            query: SQL запрос
            params: Параметры запроса для защиты от SQL-injection
            
        Returns:
            Список результатов (список кортежей)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB ERROR] Ошибка выполнения запроса: {e}")
            raise
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Выполнение INSERT, UPDATE, DELETE запроса.
        
        Args:
            query: SQL запрос
            params: Параметры запроса
            
        Returns:
            Количество затронутых строк
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"[DB ERROR] Ошибка выполнения обновления: {e}")
            raise
    
    def close_connection(self) -> None:
        """Закрытие подключения к БД."""
        if self.connection:
            self.connection.close()
            print("[DB] Подключение закрыто")
            DatabaseConnection._instance = None
            DatabaseConnection._initialized = False
    
    def create_tables(self) -> None:
        """Создание таблиц для системы учета сотрудников."""
        schema = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            base_salary REAL NOT NULL,
            type TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            deadline TEXT NOT NULL
        );
        """
        try:
            cursor = self.connection.cursor()
            cursor.executescript(schema)
            self.connection.commit()
            print("[DB] Таблицы созданы успешно")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Ошибка создания таблиц: {e}")
            raise
