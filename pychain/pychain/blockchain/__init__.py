from .transaction import Transaction
from .block import Block
from .chain import Chain


if len(Chain) == 0:
    Chain._init_genesis_block()
