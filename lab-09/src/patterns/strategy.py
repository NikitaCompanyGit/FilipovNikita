class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class ILogger(ABC):
    """Интерфейс для логгера (DIP)"""

    @abstractmethod
    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass

class ConsoleLogger(ILogger):
    """Логирование в консоль"""

    def __init__(self, show_timestamp: bool = True):
        self.show_timestamp = show_timestamp

    def _format_message(self, message: str, level: LogLevel) -> str:
        timestamp = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " if self.show_timestamp else ""
        return f"{timestamp}[{level.value}] {message}"

    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        print(self._format_message(message, level))

    def debug(self, message: str) -> None:
        self.log(message, LogLevel.DEBUG)

    def info(self, message: str) -> None:
        self.log(message, LogLevel.INFO)

    def warning(self, message: str) -> None:
        self.log(message, LogLevel.WARNING)

    def error(self, message: str) -> None:
        self.log(message, LogLevel.ERROR)

class FileLogger(ILogger):
    """Логирование в файл"""

    def __init__(self, filename: str):
        self.filename = filename
        self.logs = []

    def _format_message(self, message: str, level: LogLevel) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"[{timestamp}] [{level.value}] {message}"

    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        formatted = self._format_message(message, level)
        self.logs.append(formatted)

    def debug(self, message: str) -> None:
        self.log(message, LogLevel.DEBUG)

    def info(self, message: str) -> None:
        self.log(message, LogLevel.INFO)

    def warning(self, message: str) -> None:
        self.log(message, LogLevel.WARNING)

    def error(self, message: str) -> None:
        self.log(message, LogLevel.ERROR)

class NullLogger(ILogger):
    """Пустой логгер (Null Object Pattern)"""

    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        pass

    def debug(self, message: str) -> None:
        pass

    def info(self, message: str) -> None:
        pass

    def warning(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass