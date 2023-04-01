from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")

class Repository(ABC):

    @abstractmethod
    def read(self) -> list[T]:
        ...

    @abstractmethod
    def read_by_id(self, line_id: T) -> T | None:
        ...

    @abstractmethod
    def write(self, data: list[T] | T):
        ...