import math
from MappingStrategy import MappingStrategy


class DirectMapping(MappingStrategy):
    def __init__(self, num_lines: int, block_size: int):
        self.num_lines = num_lines
        self.block_size = block_size
        self.blockOffset_bits = int(math.log2(block_size))
        self.index_bits = int(math.log2(self.num_lines))
        self.tag_bits = 32 - self.blockOffset_bits - self.index_bits


    def get_cache_location(self, address: int):
        index = self.get_index(address)
        return (index, )

    def get_tag(self, address: int) -> int:
        return address >> (self.blockOffset_bits + self.index_bits)

    def get_index(self, address: int) -> int:
        block_num = address >> self.blockOffset_bits
        return block_num % self.num_lines

    def get_block_offset(self, address: int) -> int:
        return address & ((1 << self.blockOffset_bits) - 1)
