from abc import ABC, abstractmethod

from CacheLine import CacheLine


class WritePolicy(ABC):
    @abstractmethod
    def handle_write_hit(self, cache_line: CacheLine, address, data):
        pass

    @abstractmethod
    def handle_write_miss(self, address: int, data) -> bool:
        pass