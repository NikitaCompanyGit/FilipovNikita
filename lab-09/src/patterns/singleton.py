class IDatabaseConnection(ABC)
    @abstractmethod
    def execute_query(self, query str, params tuple = ()) - List[Tuple]
        pass

    @abstractmethod
    def execute_update(self, query str, params tuple = ()) - int
        pass

    @abstractmethod
    def close_connection(self) - None
        pass

class ThreadSafeDatabaseConnection(IDatabaseConnection)
    _instance Optional['ThreadSafeDatabaseConnection'] = None
    _lock threading.Lock = threading.Lock()
    _initialized bool = False

    def __new__(cls, db_path str = company.db, logger ILogger = None)
        if cls._instance is None
            with cls._lock
                if cls._instance is None
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path str = company.db, logger ILogger = None)
        if not ThreadSafeDatabaseConnection._initialized
            with self._lock
                if not ThreadSafeDatabaseConnection._initialized
                    self.db_path = db_path
                    self._logger = logger or NullLogger()
                    self.connection = sqlite3.connect(db_path, check_same_thread=False)
                    self._logger.info(fБД подключена {db_path})
                    ThreadSafeDatabaseConnection._initialized = True

    def execute_query(self, query str, params tuple = ()) - List[Tuple]
        with self._lock
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query str, params tuple = ()) - int
        with self._lock
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount

    def close_connection(self) - None
        with self._lock
            if self.connection
                self.connection.close()
                ThreadSafeDatabaseConnection._instance = None
                ThreadSafeDatabaseConnection._initialized = False