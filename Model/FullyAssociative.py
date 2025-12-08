import math
from Model.MappingStrategy import MappingStrategy


class FullyAssociative(MappingStrategy):
    def __init__(self, num_lines: int, block_size: int):
        self.num_lines = num_lines
        self.block_size = block_size
        self.blockOffset_bits = int(math.log2(block_size))
        self.tag_bits = 32 - self.blockOffset_bits

    def get_cache_location(self, address: int) -> tuple:
        return tuple(range(self.num_lines))

    def get_tag(self, address: int) -> int:
        return address >> self.blockOffset_bits

    def get_block_offset(self, address: int) -> int:
        return address & ((1 << self.blockOffset_bits) - 1)