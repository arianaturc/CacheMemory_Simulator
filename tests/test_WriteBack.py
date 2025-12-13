from Model.WriteBack import WriteBack
from Model.CacheLine import CacheLine
from tests.MainMemoryTest import MainMemoryTest


def test_write_back_hit_sets_dirty_without_memory_write():
    memory = MainMemoryTest()
    wb = WriteBack(memory)

    line = CacheLine()
    line.valid = True
    line.dirtyBit = False

    wb.handle_write_hit(line, address=64, data="X")

    assert line.data == "X"
    assert line.dirtyBit is True
    assert memory.status == {}

def test_write_back_writes_if_dirty():
    memory = MainMemoryTest()
    wb = WriteBack(memory)

    line = CacheLine()
    line.data = "Z"
    line.dirtyBit = True

    written = wb.write_if_dirty(line, address=256)

    assert written is True
    assert memory.status[256] == "Z"


def test_write_back_not_dirty():
    memory = MainMemoryTest()
    wb = WriteBack(memory)

    line = CacheLine()
    line.data = "Z"
    line.dirtyBit = False

    written = wb.write_if_dirty(line, address=256)

    assert written is False
    assert memory.status == {}


def test_write_back_miss_allows_allocation():
    memory = MainMemoryTest()
    wb = WriteBack(memory)

    written = wb.handle_write_miss(address=512, data="A")

    assert written is True

