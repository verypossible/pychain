import pytest

from pychain.blockchain.chain import _Chain


@pytest.fixture()
def chain():
    chain = _Chain()
    chain.add_transaction('Genesis')
    return chain


def test_chain_inits_with_genesis(chain):
    assert len(chain) == 2
    assert len(chain.get_current_block()) == 0


def test_add_transaction_no_rolloever(chain):
    for i in range(1, 6):
        chain.add_transaction('a' * i)

    assert len(chain) == 2
    assert len(chain.get_current_block()) == 5


def test_add_transaction_rolloever(chain):
    for i in range(1, 7):
        chain.add_transaction('a' * i)

    assert len(chain) == 3
    assert len(chain.get_current_block()) == 1
