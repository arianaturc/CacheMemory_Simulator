class MainMemory:
    def __init__(self, size):
        self.size = size
        self.memory = {}

    def read(self, address: int):
        return self.memory.get(address, None)

    def write(self, address: int, data):
        self.memory[address] = data

    def hardcode_memory(self):
        self.memory = {
            0x1000: "Data_A",
            0x1040: "Data_B",
            0x1080: "Data_C",
            0x10C0: "Data_D",
            0x2000: "Data_E",
            0x2040: "Data_F",
            0x2080: "Data_G",
            0x20C0: "Data_H",
            0x3000: "Data_I",
            0x3040: "Data_J",
            0x3080: "Data_K",
            0x30C0: "Data_L",
            0x4000: "Data_M",
            0x4040: "Data_N",
            0x4080: "Data_O",
            0x40C0: "Data_P",
        }

    def display_memory_state(self):
        print("*" * 25)
        print("Memory State:")
        print("*" * 25)
        for address in self.memory:
            print(f"{address}: {self.memory[address]}")