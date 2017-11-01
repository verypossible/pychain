import pytest

from pychain.blockchain.block import BlockError
from pychain.blockchain.transaction import Transaction
from pychain.blockchain.genesis import (
        GENESIS_POW_HASH,
        get_genesis_block,
)



@pytest.fixture()
def mock_timestamp(mocker):
    mock_get_timestamp = mocker.patch('pychain.blockchain.chain.get_timestamp')
    mock_get_timestamp.return_value = 1508958803
    return mock_get_timestamp


@pytest.fixture()
def transactions():
    return [Transaction(d) for d in ('one', 'two', 'three')]


def test_chain_inits_with_genesis(chain):
    assert len(chain) == 1
    assert len(chain.get_last_block()) == 1
    for block in chain:
        assert len(block) == 1


from pprint import pprint as pp

def test_get_last_block_genesis(chain):
    block = chain.get_last_block()
    genesis = get_genesis_block()
    assert block.to_primitive() == genesis.to_primitive()

def test_create_candidate_header(chain, transactions, mock_timestamp):
    header = chain._create_candidate_header(transactions)
    assert header.prev_hash == GENESIS_POW_HASH
    assert header.merkle_root == 'b24cb0989bce2e423d6cce6341cc0377b847df72388f73202c1f9e218433cc7c'


def test_add_new_block(chain, block):
    assert chain.add_new_block(block)
    assert len(chain) == 2


def test_add_invalid_block_tamper_with_header_hash(chain, block, mocker):
    mock_header_hasher = mocker.MagicMock(return_value='deadbeefy')
    block.header.generate_hash = mock_header_hasher

    with pytest.raises(BlockError) as e:
        chain.add_new_block(block)

    assert 'Invalid POW hash' in str(e)
    assert len(chain) == 1


def test_add_invalid_block_tamper_with_header_nonce(chain, block, mocker):
    block.header.nonce = 1973

    with pytest.raises(BlockError) as e:
        chain.add_new_block(block)

    assert 'Invalid POW hash' in str(e)
    assert len(chain) == 1


def test_add_invalid_block_tamper_with_header_target(chain, block, mocker):
    block._Block__pow_hash = 'deadbeef'
    mock_header_hasher = mocker.MagicMock(return_value='deadbeef')
    block.header = mocker.MagicMock(target=0, generate_hash=mock_header_hasher)

    with pytest.raises(BlockError) as e:
        chain.add_new_block(block)

    assert 'POW target greater than expected target' in str(e)


#
# def test_create_candidate_block_tamper_with_header_merkle(chain, transactions, mocker):
#     mock_create_header = mocker.patch.object(chain, '_create_candidate_header')
#     mock_header = mocker.MagicMock(
#             target=0xdeadbeef + 1,
#             generate_hash=mocker.MagicMock(return_value='deadbeef'),
#             merkle_root='deadbeefy',
#     )
#     mock_create_header.return_value = (True, mock_header, 'deadbeef')
#
#     with pytest.raises(BlockError) as e:
#         chain.create_candidate_block(transactions)
#
#     assert 'Invalid merkle_root hash' in str(e)
