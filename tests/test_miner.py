import pytest

from pychain.blockchain import miner



@pytest.fixture()
def header(mocker):
    return mocker.MagicMock(target=256)


def test_mine_and_find_one_iteration(header, mocker):
    mock_hasher = mocker.MagicMock(return_value='ff')
    header.generate_hash = mock_hasher
    assert miner.mine(header) == (0, 'ff')
    mock_hasher.assert_called_once_with(nonce=0)


def test_mine_and_find_three_iterations(header, mocker):
    mock_hasher = mocker.MagicMock(side_effect=('ffff', 'fff', 'ff'))
    header.generate_hash = mock_hasher
    assert miner.mine(header) == (2, 'ff')
    assert mock_hasher.call_count == 3


def test_mine_no_match_one_iteration(header, mocker):
    mocker.patch('pychain.blockchain.miner.MAX_NONCE', 1)
    mock_hasher = mocker.MagicMock(return_value='ff0000')
    header.generate_hash = mock_hasher
    assert miner.mine(header) == (None, None)
    assert mock_hasher.call_count == 1


def test_mine_no_match_three_iterations(header, mocker):
    mocker.patch('pychain.blockchain.miner.MAX_NONCE', 3)
    mock_hasher = mocker.MagicMock(side_effect=('ffff000', 'fff000', 'ff000'))
    header.generate_hash = mock_hasher
    assert miner.mine(header) == (None, None)
    assert mock_hasher.call_count == 3
