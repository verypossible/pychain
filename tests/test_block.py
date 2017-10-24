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
    # hack for testing
    block.timestamp = 1508802926422
    block.nonce = 461
    block.close()
    print()
    print(block.nonce)
    expected = '00155abf1f2df1e62682a4f2170c7d33dfcb1f0864d97db6dc4feddd6dcea580'
    assert block.hash == expected


#def test_validatek
