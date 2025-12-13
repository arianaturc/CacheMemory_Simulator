from Model.LRUAlgorithm import LRUAlgorithm
from Model.CacheLine import CacheLine


def test_lru_replaces_least_recently_used():
    lru = LRUAlgorithm()

    lru.update_recency(0)
    lru.update_recency(1)
    lru.update_recency(2)

    candidate_lines = (0, 1, 2)
    cache_lines = [CacheLine() for _ in range(3)]

    victim = lru.select_line_to_replace(cache_lines, candidate_lines)

    assert victim == 0


def test_lru_updates_recency():
    lru = LRUAlgorithm()

    lru.update_recency(0)
    lru.update_recency(1)
    lru.update_recency(2)
    lru.update_recency(0)
    lru.update_recency(2)
    lru.update_recency(0)

    candidate_lines = (0, 1, 2)

    victim = lru.select_line_to_replace([], candidate_lines)

    assert victim == 1


def test_lru_remove_line():
    lru = LRUAlgorithm()
    lru.update_recency(0)
    lru.update_recency(1)

    lru.remove_line(0)

    assert 0 not in lru.recent_lines
