import json

from .blockchain import Chain
from .blockchain.block import (
        Block,
        BlockError,
)
from .blockchain.block_header import BlockHeader
from .blockchain.miner import mine
from .blockchain.transaction import Transaction
from .blockchain.transaction_pool import add_transaction
from .constants import TARGET
from .helpers import get_timestamp
from .globals import get_db_number

from pprint import pprint as pp


def _get_new_block_header(last_block, transactions):
    # This is not really a merkle root.  Instead, simply hash all of the hashes for each
    # transaction
    fake_merkle_root = Transaction.generate_hash_for_transactions(transactions)
    return BlockHeader(
            prev_hash=last_block.hash,
            merkle_root=fake_merkle_root,
            timestamp=get_timestamp(),
            target=TARGET,
    )


def handle_index(reset=False):
    if reset:
        Chain._reset()
    return {
        'num_blocks': len(Chain),
        'latest_block': Chain.get_last_block().to_primitive(),
        'db_number': get_db_number(),
    }


def handle_mining(transactions):
    print('Start mining on db: %s' % get_db_number())
    print(transactions)
    transactions = [Transaction(t) for t in transactions]
    last_block = Chain.get_last_block()
    header = _get_new_block_header(last_block, transactions)

    nonce, pow_hash = mine(header)
    print('Mining complete: nonce: %s, pow_hash: %s' % (nonce, pow_hash))

    header.nonce = nonce

    return (header, pow_hash, transactions)


def handle_add_transaction(transaction, block_size=None, is_broadcasting=False):
    pool_len = add_transaction(
            transaction,
            block_size=block_size,
            is_broadcasting=is_broadcasting,
    )
    return {
        'success': True,
        'msg': 'Transaction added to transaction pool, now of length: %s' % pool_len,
        'db_number': get_db_number(),
    }


def handle_add_new_block(*, header, pow_hash, transactions, **kwargs):
    print('Adding new block on db: %s' % get_db_number())
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
