from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def write(self, message: str):
        raise NotImplementedError
