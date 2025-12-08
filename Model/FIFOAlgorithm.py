from collections import deque

from Model.CacheLine import CacheLine
from Model.ReplacementAlgorithm import ReplacementAlgorithm

class FIFOAlgorithm(ReplacementAlgorithm):
    def __init__(self):
        self.queue = deque()

    def select_line_to_replace(self, cache_lines: list[CacheLine], candidate_lines: tuple) -> int:
        for line_idx in self.queue:
            if line_idx in candidate_lines:
                return line_idx

        return candidate_lines[0]

    def update_on_access(self, line_idx: int) -> None:
        pass

    def update_on_insertion(self, line_idx: int) -> None:
        if line_idx not in self.queue:
            self.queue.append(line_idx)

    def remove_from_queue(self, line_idx: int) -> None:
        if line_idx in self.queue:
            self.queue.pop()




