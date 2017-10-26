import os

BLOCK_SIZE = int(os.environ.get('PYCHAIN_BLOCK_SIZE', 5))

DIFFICULTY_BITS = int(os.environ.get('PYCHAIN_DIFFICULTY_BITS', 2))
TARGET = 2 ** (256 - DIFFICULTY_BITS)

#MAX_TARGET = 2 ** 256

_max_nonce = 2 ** 32 # 4 billion
MAX_NONCE = int(os.environ.get('PYCHAIN_MAX_NONCE', _max_nonce))
