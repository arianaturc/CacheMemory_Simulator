from Model.FullyAssociative import FullyAssociative


def test_fully_associative_cache_location():
    fa = FullyAssociative(num_lines=4, block_size=64)

    assert fa.get_cache_location(0) == (0, 1, 2, 3)
    assert fa.get_cache_location(256) == (0, 1, 2, 3)

def test_fully_associative_tag():
    fa = FullyAssociative(num_lines=4, block_size=64)

    assert fa.get_tag(0) == 0
    assert fa.get_tag(64) == 1
    assert fa.get_tag(128) == 2


def test_fully_associative_block_offset():
    fa = FullyAssociative(num_lines=4, block_size=64)

    assert fa.get_block_offset(5) == 5
    assert fa.get_block_offset(64) == 0
