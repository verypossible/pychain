import pytest

from pychain.blockchain.block import (
        Block,
        BlockError,
)
from pychain.blockchain.block_header import BlockHeader
from pychain.blockchain.transaction import Transaction


@pytest.fixture()
def block():
    h = BlockHeader(
            prev_hash='0000f8b59e9c39b9bdb63793b6a085b465d2ae9a4e3c54759f46f17948eeff7f',
            merkle_root='2bce0bad29c5575d6e66afc4eb0dff545f8d751f4680d9ef6557345e60fcc141',
            timestamp=1508907362)
    return Block(
            index=1,
            header=h,
            transactions=[Transaction('foobar')],
            pow_hash='c73da18d9150d95f38402361a1be7213362170fd1031fc3b74ca245846bdc27e')


def test_block_len(block):
    assert len(block) == 1


def test_check_block_header(block):
    block.check_block_header()
    assert True

def test_check_block(block):
    block.check_block()
    assert True


# _test_entries = (
#         ((), 0),
#         (('a',), 1),
#         (('a', 'b', 'c'), 3),
#         (range(Block.BLOCK_SIZE), Block.BLOCK_SIZE),
# )
#
# @pytest.mark.parametrize('transactions, expected_len', _test_entries)
# def test_len_transactions(transactions, expected_len, block):
#     for data in transactions:
#         block.add_transaction(data)
#     assert len(block) == expected_len
#
#
# def test_cannot_add_to_closed_block(block):
#     for i in range(Block.BLOCK_SIZE):
#         block.add_transaction(i)
#
#     with pytest.raises(BlockError) as e:
#         block.add_transaction('abc')
#
#
# def test_hash_generated(block):
#     block.add_transaction('abc')
#     block.add_transaction({'name': 'bz', 'age': 44})
#     assert not block.hash
#     # hack for testing
#     block.timestamp = 1508802926422
#     block.close()
#     expected = 'e5e00af476d732b89a35c7e3f8f77e6b1fb43d6f0288096aab77b09ea9e6f0eb'
#     assert block.hash == expected
#
#
# #def test_validatek
