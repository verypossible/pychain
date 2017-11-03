import pytest

from pychain.handlers import handle_add_transaction
from pychain.persistence import (
        RedisTransactionPool,
        RedisPendingTransactions,
)


@pytest.fixture()
def transaction_pool():
    return RedisTransactionPool()


@pytest.fixture()
def pending_transactions():
    return RedisPendingTransactions()


def test_empty_pool(transaction_pool):
    assert len(transaction_pool) == 0


def test_add_transaction(chain, transaction_pool):
    handle_add_transaction({'msg': 'testing'})
    assert len(transaction_pool) == 1
    assert len(chain) == 1


def test_add_transaction_and_create_block(chain, transaction_pool, pending_transactions, mocker):
    mock_create_candidate = mocker.patch('pychain.blockchain.chain.Chain.create_candidate_block')
    for i in range(5):
        handle_add_transaction('Test %s' % (i, ))
    assert len(transaction_pool) == 0
    assert len(chain) == 1
    assert len(pending_transactions) == 5
    mock_create_candidate.assert_called_once()
