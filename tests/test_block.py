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


def test_check_block_header_invalid_pow_hash(block, mocker):
    mock_hasher = mocker.patch.object(block.header, 'generate_hash')
    mock_hasher.return_value = 'abc123'

    with pytest.raises(BlockError) as e:
        block.check_block_header()

    assert 'Invalid POW hash' in str(e)


def test_check_block_header_invalid_pow_target(block, mocker):
    def _generate_hash(*args, **kwargs):
        return 'c73da18d9150d95f38402361a1be7213362170fd1031fc3b74ca245846bdc27e'

    mock_header = mocker.MagicMock(
            target=0xdeadbeef,
            nonce=block.header.nonce,
            generate_hash=_generate_hash,
    )
    block.header = mock_header

    with pytest.raises(BlockError) as e:
        block.check_block_header()

    assert 'POW target greater than expected target' in str(e)


def test_check_block(block):
    block.check_block()
    assert True


def test_check_block_empty():
    block = Block(index=1, header=None, transactions=[], pow_hash='')

    with pytest.raises(BlockError) as e:
        block.check_block()

    assert 'Empty transactions list' in str(e)


def test_check_block_invalid_merkle(mocker):
    t = Transaction('foobar')

    mock_header = mocker.MagicMock(merkle_root='abc123')
    block = Block(index=1, header=mock_header, transactions=[t], pow_hash='')

    with pytest.raises(BlockError) as e:
        block.check_block()

    assert 'Invalid merkle_root hash' in str(e)


def test_as_dict(block):
    header = {
        'merkle_root': '2bce0bad29c5575d6e66afc4eb0dff545f8d751f4680d9ef6557345e60fcc141',
        'nonce': 0,
        'prev_hash': '0000f8b59e9c39b9bdb63793b6a085b465d2ae9a4e3c54759f46f17948eeff7f',
        'target': 115792089237316195423570985008687907853269984665640564039457584007913129639936,
        'timestamp': 1508907362,
        'version': 1,
    }

    expected = {
        'header': header,
        'index': 1,
        'pow_hash': 'c73da18d9150d95f38402361a1be7213362170fd1031fc3b74ca245846bdc27e',
        'transactions': [
            ('a61deaef26c069e32bda388991cf1f07f0a6dd451bc6a7bdad3e34eecbbadb39', '"foobar"')
        ]
    }
    assert block.as_dict() == expected
