from Model.CacheLine import CacheLine
from Model.ReplacementAlgorithm import ReplacementAlgorithm
import random

class RandomAlgorithm(ReplacementAlgorithm):
    def __init__(self):
        self.random = random

    def select_line_to_replace(self, cache_lines: list[CacheLine], candidate_lines: tuple) -> int:
        return self.random.choice(candidate_lines)

    def update_on_access(self, cacheLine: CacheLine) -> None:
        pass
