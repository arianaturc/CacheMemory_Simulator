from CacheLine import CacheLine
from ReplacementAlgorithm import ReplacementAlgorithm

class LRUAlgorithm(ReplacementAlgorithm):
    def __init__(self):
        self.recent_lines = {}
        self.access_count = 0


    def select_line_to_replace(self, cache_lines: list[CacheLine], candidate_lines: tuple) -> int:
        line_idx = candidate_lines[0]
        min_recency = self.recent_lines.get(line_idx, -1)

        for line in candidate_lines:
            recency = self.recent_lines.get(line, -1)
            if recency < min_recency:
                min_recency = recency
                line_idx = line

        return line_idx

    def update_recency(self, line_idx: int):
        self.access_count += 1
        self.recent_lines[line_idx] = self.access_count


    def update_on_access(self, line_idx: int) -> None:
        pass

    def remove_line(self, line_idx: int) -> None:
        if line_idx in self.recent_lines:
            del self.recent_lines[line_idx]





