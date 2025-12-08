from Model.CacheLine import CacheLine


class CacheMemory:
    def __init__(self, num_lines: int):
        self.num_lines = num_lines
        self.lines = [CacheLine() for _ in range(num_lines)]

    def get_line(self, index: int) -> CacheLine:
        return self.lines[index]

    def __repr__(self):
        valid_lines = sum(1 for line in self.lines if line.valid)
        return f"CacheMemory(lines={self.num_lines}, valid={valid_lines})"