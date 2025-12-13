from Model.RandomAlgorithm import RandomAlgorithm
from Model.CacheLine import CacheLine


def test_random_returns_valid_candidate():
    rand = RandomAlgorithm()

    candidate_lines = (0, 1, 2, 3)
    cache_lines = [CacheLine() for _ in range(4)]

    victim = rand.select_line_to_replace(cache_lines, candidate_lines)

    assert victim in candidate_lines
