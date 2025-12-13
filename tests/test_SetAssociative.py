from Model.SetAssociative import SetAssociative


def test_set_associative_location():
    sa = SetAssociative(num_sets=2, block_size=64, associative=2)

    assert sa.get_cache_location(0) == (0, 1)  # address 0 → block 0 → set 0 → lines 0,1
    assert sa.get_cache_location(64) == (2, 3)  # address 64 → block 1 → set 1 → lines 2,3
    assert sa.get_cache_location(128) == (0, 1) # address 128 → block 2 → set 0


def test_set_associative_set_number():
    sa = SetAssociative(num_sets=2, block_size=64, associative=2)

    assert sa.get_set_number(0) == 0
    assert sa.get_set_number(64) == 1
    assert sa.get_set_number(128) == 0


def test_set_associative_tag():
    sa = SetAssociative(num_sets=2, block_size=64, associative=2)

    assert sa.get_tag(0) == 0
    assert sa.get_tag(256) == 2

def test_set_associative_block_offset():
    sa = SetAssociative(num_sets=2, block_size=64, associative=2)

    assert sa.get_block_offset(10) == 10
    assert sa.get_block_offset(63) == 63

