from abc import ABC, abstractmethod
from CacheLine import CacheLine


class ReplacementAlgorithm(ABC):
    @abstractmethod
    def select_line_to_replace(self, cacheLines: list[CacheLine], candidate_indices: tuple) -> int:
        pass

    @abstractmethod
    def update_on_access(self, cacheLine: CacheLine) -> None:
        pass