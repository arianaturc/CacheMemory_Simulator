import math
from MappingStrategy import MappingStrategy

'''
block_num = address // block_size
set_index = block_num % num_sets
'''


class SetAssociative(MappingStrategy):
    def __init__(self, num_sets: int, block_size: int, associative: int):
        self.num_sets = num_sets
        self.block_size = block_size
        self.associative = associative # lines / set
        self.blockOffset_bits = int(math.log2(block_size))
        self.set_bits = int(math.log2(num_sets))
        self.tag_bits = 32 - self.blockOffset_bits - self.set_bits

    def get_cache_location(self, address: int) -> tuple:
        set_number = self.get_set_number(address)
        start_line = set_number * self.associative
        return tuple(range(start_line, start_line + self.associative))

    def get_tag(self, address: int) -> int:
        return address >> (self.blockOffset_bits + self.set_bits)

    def get_set_number(self, address: int) -> int:
        block_num = address >> self.blockOffset_bits
        return block_num % self.num_sets

    def get_block_offset(self, address: int) -> int:
        return address & ((1 << self.blockOffset_bits) - 1)

