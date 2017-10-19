from .transaction import Transaction
from .block import Block
from .chain import Chain


def __init_blockchain():
    Chain.add_transaction('Genesis')

if len(Chain) == 0:
    __init_blockchain()
