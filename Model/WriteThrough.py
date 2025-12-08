from Model.CacheLine import CacheLine
from Model.WritePolicy import WritePolicy

class WriteThrough(WritePolicy):
    def __init__(self, main_memory):
        self.main_memory = main_memory
        self.write_buffer = []

    def handle_write_hit(self, cache_line: CacheLine, address: int, data):
        cache_line.data = data
        self.main_memory.write(address, data)

    def handle_write_miss(self, address: int, data):
        self.main_memory.write(address, data)
        return True
