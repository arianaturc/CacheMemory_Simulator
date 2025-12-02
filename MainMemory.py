class MainMemory:
    def __init__(self, size):
        self.size = size
        self.memory = {}

    def read(self, address: int):
        return self.memory.get(address, None)

    def write(self, address: int, data):
        self.memory[address] = data

    def display_memory_state(self):
        print("*" * 25)
        print("Memory State:")
        print("*" * 25)
        for address in self.memory:
            print(f"{address}: {self.memory[address]}")