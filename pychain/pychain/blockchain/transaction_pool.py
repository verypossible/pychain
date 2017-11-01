from . import Chain
from .constants import BLOCK_SIZE
from .transaction import Transaction

from ..persistence import RedisTransactionPool



def add_transaction(transaction):
    if not isinstance(transaction, Transaction):
        transaction = Transaction(transaction)

    r = RedisTransactionPool()
    r.append(transaction)

    if len(r) >= BLOCK_SIZE:
        transactions = r.get_transactions()
        block = Chain.create_candidate_block(transactions)
        r.record_pending_transactions(transactions)
        r.clear()
