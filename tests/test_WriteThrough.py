from Model.WriteThrough import WriteThrough
from Model.CacheLine import CacheLine
from tests.MainMemoryTest import MainMemoryTest


def test_write_through_hit_updates_cache_and_memory():
    memory = MainMemoryTest()
    wt = WriteThrough(memory)

    line = CacheLine()
    line.valid = True
    line.dirtyBit = False

    wt.handle_write_hit(line, address=64, data="X")

    assert line.data == "X"
    assert 64 in memory.status
    assert memory.status[64] == "X"
    assert line.dirtyBit is False


def test_write_through_miss():
    memory = MainMemoryTest()
    wt = WriteThrough(memory)

    allocate = wt.handle_write_miss(address=128, data="Y")

    assert allocate is True
    assert memory.status[128] == "Y"


