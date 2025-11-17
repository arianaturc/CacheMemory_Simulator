from abc import ABC, abstractmethod

class MappingStrategy(ABC):

    @abstractmethod
    def get_tag(self, address: int) -> int:
        pass

    @abstractmethod
    def get_cache_location(self, address: int) -> tuple:
        pass

    @abstractmethod
    def get_block_offset(self, address: int) -> int:
        pass
