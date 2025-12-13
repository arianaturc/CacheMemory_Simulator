from Model.DirectMapping import DirectMapping


def test_direct_cache_location():
    dm = DirectMapping(num_lines=4, block_size=64)

    assert dm.get_cache_location(0) == (0,)
    assert dm.get_cache_location(64) == (1,)
    assert dm.get_cache_location(256) == (0,)

def test_direct_mapping_tag():
    dm = DirectMapping(num_lines=4, block_size=64)

    assert dm.get_tag(0) == 0
    assert dm.get_tag(64) == 0
    assert dm.get_tag(256) == 1


def test_direct_mapping_block_offset():
    dm = DirectMapping(num_lines=4, block_size=64)

    assert dm.get_block_offset(0) == 0
    assert dm.get_block_offset(32) == 32
    assert dm.get_block_offset(64) == 0
