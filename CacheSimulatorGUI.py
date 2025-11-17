from CacheController import CacheController
from Statistics import Statistics



class CacheSimulatorGUI:


    def __init__(self, controller: CacheController, statistics: Statistics):
        self.controller = controller
        self.statistics = statistics

    def run(self):
        print("Cache Simulator GUI")
        print("=" * 60)
        print(f"Cache Configuration:")
        print(f"  Lines: {self.controller.num_lines}")
        print(f"  Block Size: {self.controller.block_size} bytes")
        print(f"  Mapping: {type(self.controller.mapping_strategy).__name__}")
        print(f"  Replacement: {type(self.controller.replacement_algorithm).__name__}")
        print(f"  Write Policy: {type(self.controller.write_policy).__name__}")
        print("=" * 60)


