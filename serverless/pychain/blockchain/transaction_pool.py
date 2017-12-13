from . import Chain
from .transaction import Transaction

from ..constants import BLOCK_SIZE
from ..persistence import RedisTransactionPool, RedisPendingTransactions
from ..p2p import broadcast



def add_transaction(transaction, block_size=None, is_broadcasting=False):
    if not isinstance(transaction, Transaction):
        transaction = Transaction(transaction)

    pool = RedisTransactionPool()
    pool.append(transaction)
    pool_len = len(pool)

    # only broadcast this message if it's not itself a source of a broadcast message, otherwise
    # we'll DOS ourselves.
    if not is_broadcasting:
        broadcast(transaction)

    block_size = block_size if block_size is not None else BLOCK_SIZE

    # Each endpoint, dbs 1, 2 and 3 all start the mining process. Once complete, they will attempt
    # to verify the block and add it.  The node who does this entire process first should win, even
    # though all will eventually complete the process.
    if len(pool) >= block_size:
        transactions = pool.get_transactions()
        block = Chain.create_candidate_block(transactions)
        pool.record_pending_transactions(transactions)

    return pool_len
