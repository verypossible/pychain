from .block_entry import BlockEntry
from .block import Block
from .chain import Chain


def __init_blockchain():
    Chain.add_entry('Genesis')

if len(Chain) == 0:
    __init_blockchain()
