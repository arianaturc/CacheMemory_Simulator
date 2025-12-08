import math
from Controller.CacheController import CacheController
from View.CacheSimulatorGUI import CacheSimulatorGUI
from Model.DirectMapping import DirectMapping
from Model.FIFOAlgorithm import FIFOAlgorithm
from Model.FullyAssociative import FullyAssociative
from Model.LRUAlgorithm import LRUAlgorithm
from Model.MainMemory import MainMemory
from Model.SetAssociative import SetAssociative
from Model.WriteBack import WriteBack


if __name__ == "__main__":
    cache_size = 1024
    block_size = 64
    main_memory_size = 65536

    main_memory = MainMemory(main_memory_size)

    for i in range(0, 2000, 64):
        main_memory.write(i, f"Data_{i}")

    # DIRECT MAPPING SIMULATION
    print("=" * 28)
    print("DIRECT MAPPING SIMULATION")
    print("=" * 28)
    print(f"Cache: {cache_size} bytes, Block: {block_size} bytes")

    num_lines = cache_size // block_size
    print(f"Number of lines: {num_lines}")
    print(f"Address bits: Offset={int(math.log2(block_size))}, Index={int(math.log2(num_lines))}, Tag={32 - int(math.log2(block_size)) - int(math.log2(num_lines))}")

    mapping = DirectMapping(num_lines, block_size)
    replacement = LRUAlgorithm()
    write_policy = WriteBack(main_memory)

    controller = CacheController(cache_size, block_size, mapping, replacement, write_policy, main_memory)

    addresses = [0, 64, 70, 0, 64, 1024]

    for addr in addresses:
        print(f"\nAccessing address: {addr} (0x{addr:X})")
        data = controller.read(addr)
        print(f"  Read: {data}")


    controller.display_cache_state()
    controller.get_statistics()



    # FULLY ASSOCIATIVE SIMULATION
    print("\n\n\n" + "=" * 38)
    print("FULLY ASSOCIATIVE MAPPING SIMULATION")
    print("=" * 38)

    main_memory = MainMemory(main_memory_size)
    for i in range(0, 2000, 64):
        main_memory.write(i, f"Data_{i}")

    print(f"Cache: {cache_size} bytes, Block: {block_size} bytes")
    print(f"Number of lines: {num_lines}")
    print(f"Address bits: Offset={int(math.log2(block_size))}, Tag={32 - int(math.log2(block_size))}")

    mapping3 = FullyAssociative(num_lines, block_size)
    replacement3 = FIFOAlgorithm()
    write_policy3 = WriteBack(main_memory)

    controller3 = CacheController(cache_size, block_size, mapping3, replacement3, write_policy3, main_memory)

    addresses3 = [ 0, 64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 128, 384, 0, 64 ]

    for addr in addresses3:
        print(f"\nAccessing address: {addr} (0x{addr:X})")
        data = controller3.read(addr)
        print(f"  Read: {data}")

    controller3.write(0, "Modified_0")


    addr = 1024
    print(f"\nAccessing address: {addr} (0x{addr:X})")
    controller3.read(addr)

    print(f"\nMemory state\n")
    print(main_memory.display_memory_state())

    controller3.display_cache_state()





    # SET ASSOCIATIVE SIMULATION
    print("\n\n" + "=" * 38)
    print("SET-ASSOCIATIVE MAPPING SIMULATION")
    print("=" * 38)


    main_memory = MainMemory(main_memory_size)
    for i in range(0, 2000, 64):
        main_memory.write(i, f"Data_{i}")

    num_sets = 8
    associativity = 2
    print(f"Cache: {cache_size} bytes, Block: {block_size} bytes")
    print(f"Sets: {num_sets}, Associativity: 2 lines / set")
    print(
        f"Address bits: Offset={int(math.log2(block_size))}, "
        f"Set={int(math.log2(num_sets))}, "
        f"Tag={32 - int(math.log2(block_size)) - int(math.log2(num_sets))}"
    )

    mapping2 = SetAssociative(num_sets, block_size, associativity)
    replacement2 = FIFOAlgorithm()
    write_policy2 = WriteBack(main_memory)

    controller2 = CacheController(cache_size, block_size, mapping2, replacement2, write_policy2, main_memory)

    addresses2 = [0, 512, 1024, 64, 128, 64]

    for addr in addresses2:
        print(f"\nAccessing address: {addr} (0x{addr:X})")
        data = controller2.read(addr)
        print(f"  Read: {data}")

    controller2.display_cache_state()

    print("\n")
    controller2.get_statistics()