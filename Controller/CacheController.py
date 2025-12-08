from Model.CacheMemory import CacheMemory
from Model.DirectMapping import *
from Model.FIFOAlgorithm import FIFOAlgorithm
from Model.FullyAssociative import FullyAssociative
from Model.LRUAlgorithm import LRUAlgorithm
from Model.MainMemory import MainMemory
from Model.MappingStrategy import MappingStrategy
from Model.RandomAlgorithm import RandomAlgorithm
from Model.ReplacementAlgorithm import ReplacementAlgorithm
from Model.SetAssociative import SetAssociative
from Model.Statistics import Statistics
from Model.WriteBack import WriteBack
from Model.WritePolicy import WritePolicy
from Model.WriteThrough import WriteThrough


class CacheController:
    def __init__(self, cache_size: int, block_size: int, mapping_type: str, replacement_policy: str, write_policy_type: str, main_memory: MainMemory, associativity: int = 1):

        self.num_lines = cache_size // block_size
        self.block_size = block_size
        self.main_memory = main_memory

        # --- Mapping Strategy ---
        if mapping_type == "Direct":
            self.mapping_strategy = DirectMapping(self.num_lines, block_size)

        elif mapping_type == "SetAssoc":
            self.mapping_strategy = SetAssociative(
                self.num_lines // associativity,
                block_size,
                2
            )

        elif mapping_type == "FullyAssoc":
            self.mapping_strategy = FullyAssociative(self.num_lines, block_size)

        else:
            raise ValueError("Invalid mapping strategy")

        # --- Replacement Algorithm ---
        if replacement_policy == "LRU":
            self.replacement_algorithm = LRUAlgorithm()

        elif replacement_policy == "FIFO":
            self.replacement_algorithm = FIFOAlgorithm()

        elif replacement_policy == "Random":
            self.replacement_algorithm = RandomAlgorithm()

        else:
            raise ValueError("Invalid replacement policy")

        # --- Write Policy ---
        if write_policy_type == "WriteBack":
            self.write_policy = WriteBack(self.main_memory)

        elif write_policy_type == "WriteThrough":
            self.write_policy = WriteThrough(self.main_memory)

        else:
            raise ValueError("Invalid write policy")

        self.cache_memory = CacheMemory(self.num_lines)
        self.line_addresses = {}
        self.statistics = Statistics()



    def read(self, address: int):
        tag = self.mapping_strategy.get_tag(address)
        block_offset = self.mapping_strategy.get_block_offset(address)
        candidate_lines = self.mapping_strategy.get_cache_location(address)

        if isinstance(self.mapping_strategy, DirectMapping):
            index = self.mapping_strategy.get_index(address)
            print(f"  Address breakdown: Tag=0x{tag:X}, Index={index}, Block Offset={block_offset}")
        elif isinstance(self.mapping_strategy, SetAssociative):
                set_num = self.mapping_strategy.get_set_number(address)
                print(f"  Address breakdown: Tag=0x{tag:X}, Set={set_num}, Block Offset={block_offset}")
        elif isinstance(self.mapping_strategy, FullyAssociative):
            print(f"  Address breakdown: Tag=0x{tag:X}, Block Offset={block_offset}")

        #handle cache hit
        for index in candidate_lines:
            line = self.cache_memory.get_line(index)
            if line.valid and line.tag == tag:
                self.statistics.count_hits()

                if isinstance(self.replacement_algorithm, LRUAlgorithm):
                    self.replacement_algorithm.update_recency(index)

                print(f"  → CACHE HIT at line {index}")
                return line.data

        #handle cache miss
        self.statistics.count_misses()
        print(f"  → CACHE MISS")
        return self.handle_miss(address, tag, candidate_lines, is_write=False)

    def write(self, address: int, data):
        tag = self.mapping_strategy.get_tag(address)
        candidate_lines = self.mapping_strategy.get_cache_location(address)

        for index in candidate_lines:
            line = self.cache_memory.get_line(index)
            if line.valid and line.tag == tag:
                self.statistics.count_hits()
                self.write_policy.handle_write_hit(line, address, data)

                if isinstance(self.replacement_algorithm, LRUAlgorithm):
                    self.replacement_algorithm.update_recency(index)

                return

            self.statistics.count_misses()
            allocate = self.write_policy.handle_write_miss(address, data)
            if allocate:
                self.handle_miss(address, tag, candidate_lines, is_write=True, write_data=data)


    def handle_miss(self, address: int, tag: int, candidate_lines, is_write: bool, write_data = None):
        #check for empty lines
        line_index = None
        for index in candidate_lines:
            line = self.cache_memory.get_line(index)
            if not line.valid:
                line_index = index
                break

        if line_index is None:
            if isinstance(self.mapping_strategy, DirectMapping):
                line_index = candidate_lines[0]
            else:
                line_index = self.replacement_algorithm.select_line_to_replace(self.cache_memory.lines, candidate_lines)

        line = self.cache_memory.get_line(line_index)

        if line.valid and line.dirtyBit:
            if isinstance(self.write_policy, WriteBack):
                changed_address =  self.line_addresses.get(line_index, 0)
                self.write_policy.write_if_dirty(line, changed_address)

        if line.valid:
            if isinstance(self.replacement_algorithm, FIFOAlgorithm):
                self.replacement_algorithm.remove_from_queue(line_index)
            elif isinstance(self.replacement_algorithm, LRUAlgorithm):
                self.replacement_algorithm.remove_line(line_index)

        data = self.main_memory.read(address)

        line.valid = True
        line.tag = tag
        line.data = write_data if is_write else data
        line.dirtyBit = is_write

        self.line_addresses[line_index] = address

        if isinstance(self.replacement_algorithm, FIFOAlgorithm):
            self.replacement_algorithm.update_on_insertion(line_index)
        elif isinstance(self.replacement_algorithm, LRUAlgorithm):
            self.replacement_algorithm.update_recency(line_index)
        return None

    def get_statistics(self) -> Statistics:
        return self.statistics.display_statistics()

    def display_cache_state(self):
        print(f"\nCache State:")
        print("-" * 60)
        for i, line in enumerate(self.cache_memory.lines):
            if line.valid:
                print(f"Line {i:3d}: Valid=1, Tag=0x{line.tag:04X}, "
                      f"Dirty={int(line.dirtyBit)}, Data={line.data}")
        print("-" * 60)



