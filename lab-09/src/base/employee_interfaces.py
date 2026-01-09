"""Интерфейсы для сотрудников (ISP)."""
from abc import ABC, abstractmethod
from typing import Dict, Any

class ISalaryCalculable(ABC):
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

class IInfoProvidable(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass

class ISerializable(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class IComparable(ABC):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass
    
    @abstractmethod
    def __lt__(self, other: 'IComparable') -> bool:
        pass

class IArithmetic(ABC):
    @abstractmethod
    def __add__(self, other: Any) -> float:
        pass
    
    @abstractmethod
    def __radd__(self, other: Any) -> float:
        pass