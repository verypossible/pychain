import pytest

from pychain.blockchain.block import BlockError
from pychain.blockchain.chain import _Chain
from pychain.blockchain.transaction import Transaction
from pychain.blockchain.genesis import GENESIS_POW_HASH


@pytest.fixture()
def chain():
    chain = _Chain()
    chain._init_genesis_block()
    return chain


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


def test_create_candidate_header_success(chain, transactions, mock_timestamp):
    (success, header, valid_hash) = chain._create_candidate_header(transactions)
    assert success is True
    assert header.prev_hash == GENESIS_POW_HASH
    assert valid_hash == '282f8c77d5c5e9d67c0c07c7961690b7effd4fa29c60964db2342efc9d1e5bf4'


def test_create_candidate_header_fail(chain, transactions, mocker):
    mock_mine = mocker.patch('pychain.blockchain.chain.mine')
    mock_mine.return_value = (None, None)
    (success, header, valid_hash) = chain._create_candidate_header(transactions)
    assert success is False
    assert header.prev_hash == GENESIS_POW_HASH
    assert valid_hash is None


def test_create_candidate_block_success(chain, transactions, mock_timestamp):
    candidate_block = chain.create_candidate_block(transactions)
    assert candidate_block is not None
    expected_hash = '282f8c77d5c5e9d67c0c07c7961690b7effd4fa29c60964db2342efc9d1e5bf4'
    assert candidate_block.hash == expected_hash


def test_create_candidate_block_success_different_hash(chain, transactions):
    """Test that candidate produces a different hash.

    The header timestamp isn't under our control during the test, so the hash cannot be predicted.
    The candidate block which is produced is still a valid block, but the resulting hash is
    different from the test above where we control the timestamp.

    """
    candidate_block = chain.create_candidate_block(transactions)
    assert candidate_block is not None
    expected_hash = '282f8c77d5c5e9d67c0c07c7961690b7effd4fa29c60964db2342efc9d1e5bf4'
    assert candidate_block.hash != expected_hash


def test_create_candidate_block_fail(chain, mocker):
    """Simulate failed mining"""
    mock_create_header = mocker.patch.object(chain, '_create_candidate_header')
    mock_create_header.return_value = (False, None, None)
    candidate_block = chain.create_candidate_block(None)
    assert candidate_block is None


def test_create_candidate_block_tamper_with_header_hash(chain, transactions, mocker):
    """Tamper with the header after it has been mined.

    This will fail the header hash check since the test will set the return value of
    header.generate_hash to return a value different from the valid hash during creation of the
    header.

    """
    mock_create_header = mocker.patch.object(chain, '_create_candidate_header')
    mock_header = mocker.MagicMock(generate_hash=mocker.MagicMock(return_value='deadbeefy'))
    mock_create_header.return_value = (True, mock_header, 'deadbeef')

    with pytest.raises(BlockError) as e:
        chain.create_candidate_block(transactions)

    assert 'Invalid POW hash' in str(e)


def test_create_candidate_block_tamper_with_header_target(chain, transactions, mocker):
    mock_create_header = mocker.patch.object(chain, '_create_candidate_header')
    mock_header = mocker.MagicMock(
            target=0,
            generate_hash=mocker.MagicMock(return_value='deadbeef'),
    )
    mock_create_header.return_value = (True, mock_header, 'deadbeef')

    with pytest.raises(BlockError) as e:
        chain.create_candidate_block(transactions)

    assert 'POW target greater than expected target' in str(e)


def test_create_candidate_block_tamper_with_header_merkle(chain, transactions, mocker):
    mock_create_header = mocker.patch.object(chain, '_create_candidate_header')
    mock_header = mocker.MagicMock(
            target=0xdeadbeef + 1,
            generate_hash=mocker.MagicMock(return_value='deadbeef'),
            merkle_root='deadbeefy',
    )
    mock_create_header.return_value = (True, mock_header, 'deadbeef')

    with pytest.raises(BlockError) as e:
        chain.create_candidate_block(transactions)

    assert 'Invalid merkle_root hash' in str(e)
