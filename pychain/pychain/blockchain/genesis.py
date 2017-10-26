from .block import Block
from .block_header import BlockHeader
from .transaction import Transaction


GENESIS_HEADER_MERKLE_ROOT = '2f2d7ab3523283b62fe9e1ed89a64247a19a2abb8d80dd22e96a8784d0707d5e'
GENESIS_HEADER_TIMESTAMP = 1508907362
GENESIS_HEADER_TARGET = 2 ** (256 - 16)
GENESIS_HEADER_NONCE = 151809

GENESIS_POW_HASH = '0000f8b59e9c39b9bdb63793b6a085b465d2ae9a4e3c54759f46f17948eeff7f'

def get_genesis_block():
    h = BlockHeader(
            prev_hash='0',
            merkle_root=GENESIS_HEADER_MERKLE_ROOT,
            timestamp=GENESIS_HEADER_TIMESTAMP,
            target=GENESIS_HEADER_TARGET,
            nonce=GENESIS_HEADER_NONCE,
    )
    t = Transaction('Genesis')
    h = Block(index=0, header=h, transactions=[t], pow_hash=GENESIS_POW_HASH)
    h.check_block_header()
    h.check_block()
    return h
