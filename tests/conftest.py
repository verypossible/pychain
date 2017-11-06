import os
import sys
import pytest
import random

from pathlib import Path


CWD = Path(__file__).resolve().parent
code_dir = CWD / '../pychain'
sys.path.append(str(code_dir))

os.environ.update({
    # setting this to zero means all pow are correct
    'PYCHAIN_DIFFICULTY_BITS': '0',
    'PYCHAIN_REDIS_HOST': 'redis',
    'PYCHAIN_DEFAULT_DB_NUMBER': '5',
})

from pychain.blockchain import Chain
from pychain.blockchain.block import Block
from pychain.blockchain.block_header import BlockHeader
from pychain.blockchain.genesis import GENESIS_POW_HASH
from pychain.blockchain.transaction import Transaction
from pychain.globals import _request_local
from pychain.persistence import clear_all_dbs


def pytest_configure(config):
    """Called at the start of the entire test run"""
    clear_all_dbs()

def pytest_unconfigure(config):
    """Called at the end of a test run"""
    pass


def pytest_runtest_teardown(item, nextitem):
    """Called at the end of each test"""
    clear_all_dbs()


@pytest.fixture()
def chain():
    _request_local.host = 'testhost.local'
    # Since conftest clears out the chain before every run, re-init
    Chain._init_genesis_block()
    return Chain


@pytest.fixture()
def block():
    h = BlockHeader(
            prev_hash=GENESIS_POW_HASH,
            merkle_root='2bce0bad29c5575d6e66afc4eb0dff545f8d751f4680d9ef6557345e60fcc141',
            timestamp=1508907362)
    return Block(
            index=1,
            header=h,
            transactions=[Transaction('foobar')],
            pow_hash='c73da18d9150d95f38402361a1be7213362170fd1031fc3b74ca245846bdc27e')
