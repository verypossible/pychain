import pytest

from pychain.blockchain.block import (
        Block,
        BlockError,
)


@pytest.fixture()
def block():
    return Block(index=1, prev_hash='abc', timestamp=123456789)


_test_entries = (
        ((), 0),
        (('a',), 1),
        (('a', 'b', 'c'), 3),
        (range(5), 5),
)

@pytest.mark.parametrize('entries, expected_len', _test_entries)
def test_len_entries(entries, expected_len, block):
    for data in entries:
        block.add_entry(data)
    assert len(block) == expected_len


def test_cannot_add_to_closed_block(block):
    for i in range(5):
        block.add_entry(i)

    with pytest.raises(BlockError) as e:
        block.add_entry('abc')

