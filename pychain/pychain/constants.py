import os

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID', '679892560156')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')


BLOCK_SIZE = int(os.environ.get('PYCHAIN_BLOCK_SIZE', 5))

DIFFICULTY_BITS = int(os.environ.get('PYCHAIN_DIFFICULTY_BITS', 17))
TARGET = 2 ** (256 - DIFFICULTY_BITS)

_max_nonce = 2 ** 32 # 4 billion
MAX_NONCE = int(os.environ.get('PYCHAIN_MAX_NONCE', _max_nonce))
MAX_MINING_TIME = int(os.environ.get('PYCHAIN_MAX_MINING_TIME', 120))
MINING_ARN = 'arn:aws:sns:%s:%s:%sPyChainMiners' % (
        AWS_REGION,
        AWS_ACCOUNT_ID,
        os.environ.get('ENV', 'dev'),
)

PEERS = (1, 2, 3)
