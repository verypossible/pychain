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
        (range(Block.BLOCK_SIZE), Block.BLOCK_SIZE),
)

@pytest.mark.parametrize('transactions, expected_len', _test_entries)
def test_len_transactions(transactions, expected_len, block):
    for data in transactions:
        block.add_transaction(data)
    assert len(block) == expected_len


def test_cannot_add_to_closed_block(block):
    for i in range(Block.BLOCK_SIZE):
        block.add_transaction(i)

    with pytest.raises(BlockError) as e:
        block.add_transaction('abc')


def test_hash_generated(block):
    block.add_transaction('abc')
    block.add_transaction({'name': 'bz', 'age': 44})
    assert not block.hash
    block.close()
    expected = 'f5fed7aed4098648431dd1e3f988c501ef626542d12bcd5aefd66d71e39231b9'
    assert block.hash == expected


#def test_validatek
