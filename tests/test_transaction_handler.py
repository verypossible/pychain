import pytest

from pychain.handlers import handle_add_transaction
from pychain.persistence import RedisTransactionPool


@pytest.fixture()
def transaction_pool():
    return RedisTransactionPool()


def test_empty_pool(transaction_pool):
    assert len(transaction_pool) == 0


def test_add_transaction(chain, transaction_pool):
    handle_add_transaction({'msg': 'testing'})
    assert len(transaction_pool) == 1
    assert len(chain) == 1
