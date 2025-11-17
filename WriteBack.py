from CacheLine import CacheLine
from WritePolicy import WritePolicy

class WriteBack(WritePolicy):
    def __init__(self, main_memory):
        self.main_memory = main_memory

    def handle_write_hit(self, cache_line: CacheLine, address: int, data):
        cache_line.data = data
        cache_line.dirtyBit = True

    def write_if_dirty(self, cache_line: CacheLine, address: int) -> bool:
        if cache_line.dirtyBit:
            self.main_memory.write(address, cache_line.data)
            return True
        return False