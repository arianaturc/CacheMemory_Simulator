class MainMemoryTest:
    def __init__(self):
        self.status = {}

    def write(self, address, data):
        self.status[address] = data
