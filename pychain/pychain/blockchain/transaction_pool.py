from . import Chain
from .constants import BLOCK_SIZE
from .transaction import Transaction


__transactions = []


def add_transaction(transaction):
    global __transactions
    if not isinstance(transaction, Transaction):
        transaction = Transaction(transaction)

    __transactions.append(transaction)

    if len(__transactions) >= BLOCK_SIZE:
        block = Chain.create_candidate_block(__transactions)
        __transactions = []
