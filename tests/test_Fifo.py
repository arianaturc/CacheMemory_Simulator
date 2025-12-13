from Model.FIFOAlgorithm import FIFOAlgorithm
from Model.CacheLine import CacheLine


def test_fifo_eviction_order():
    fifo = FIFOAlgorithm()

    fifo.update_on_insertion(0)
    fifo.update_on_insertion(1)
    fifo.update_on_insertion(2)
    fifo.update_on_insertion(3)

    candidate_lines = (0, 1, 2, 3)
    cache_lines = [CacheLine() for _ in range(4)]

    victim = fifo.select_line_to_replace(cache_lines, candidate_lines)

    assert victim == 0


def test_fifo_remove_specific_line():
    fifo = FIFOAlgorithm()
    fifo.update_on_insertion(0)
    fifo.update_on_insertion(1)
    fifo.update_on_insertion(2)

    fifo.remove_from_queue(1)

    assert list(fifo.queue) == [0, 2]


def test_fifo_reinsert_after_eviction():
    fifo = FIFOAlgorithm()
    fifo.update_on_insertion(0)
    fifo.update_on_insertion(1)

    fifo.remove_from_queue(0)
    fifo.update_on_insertion(0)

    assert list(fifo.queue) == [1, 0]


def test_fifo_remove_after_eviction():
    fifo = FIFOAlgorithm()

    fifo.update_on_insertion(0)
    fifo.update_on_insertion(1)
    fifo.update_on_insertion(2)
    fifo.update_on_insertion(3)

    fifo.remove_from_queue(0)
    fifo.update_on_insertion(5)
    candidate_lines = (2, 3, 5)
    cache_lines = [CacheLine() for _ in range(4)]

    victim = fifo.select_line_to_replace(cache_lines, candidate_lines)

    assert victim == 2



