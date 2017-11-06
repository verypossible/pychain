from . import Chain
from .constants import BLOCK_SIZE
from .transaction import Transaction

from ..persistence import RedisTransactionPool, RedisPendingTransactions



def add_transaction(transaction, block_size=None, db_number=1):
    if not isinstance(transaction, Transaction):
        transaction = Transaction(transaction)

    pool = RedisTransactionPool()
    pool.append(transaction)
    pool_len = len(pool)

    block_size = block_size if block_size is not None else BLOCK_SIZE
    if len(pool) >= block_size:
        transactions = pool.get_transactions()
        block = Chain.create_candidate_block(transactions)
        pool.record_pending_transactions(transactions)

    return pool_len
