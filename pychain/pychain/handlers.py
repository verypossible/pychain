import json

from .blockchain import Chain
from .blockchain.block import (
        Block,
        BlockError,
)
from .blockchain.block_header import BlockHeader
from .blockchain.constants import TARGET
from .blockchain.miner import mine
from .blockchain.transaction import Transaction
from .blockchain.transaction_pool import add_transaction
from .helpers import get_timestamp

from pprint import pprint as pp


def _get_new_block_header(last_block, transactions):
    # This is not really a merkle root.  Instead, simply hash all of the hashes for each
    # transaction
    fake_merkle_root = Transaction.generate_hash_for_transactions(transactions)
    return BlockHeader(
            prev_hash=last_block['pow_hash'],
            merkle_root=fake_merkle_root,
            timestamp=get_timestamp(),
            target=TARGET,
    )


def handle_index(reset=False):
    if reset:
        Chain._reset()
    return {
        'num_blocks': len(Chain),
        'latest_block': Chain.get_last_block().to_primitive()
    }


def handle_mining(last_block, transactions):
    print('Start mining')
    print(transactions)
    transactions = [Transaction(t) for t in transactions]
    header = _get_new_block_header(last_block, transactions)

    nonce, pow_hash = mine(header)
    print('Mining complete: nonce: %s, pow_hash: %s' % (nonce, pow_hash))

    header.nonce = nonce

    return (header, pow_hash, transactions)


def handle_add_transaction(transaction, block_size=None):
    return add_transaction(transaction, block_size=block_size)


def handle_add_new_block(*, header, pow_hash, transactions, **kwargs):
    header = BlockHeader(**header)
    transactions = [Transaction(t) for t in transactions]
    last_block = Chain.get_last_block()
    block = Block(
            index=last_block.index + 1,
            header=header,
            transactions=transactions,
            pow_hash=pow_hash,
    )
    success = Chain.add_new_block(block)
    index = handle_index()
    index['success'] = success
    return index
