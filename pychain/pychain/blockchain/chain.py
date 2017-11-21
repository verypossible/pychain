import boto3
import json
import requests

from .block_header import BlockHeader
from .genesis import get_genesis_block
from .transaction import Transaction

from ..constants import (
        MINING_ARN,
        TARGET,
)
from ..globals import get_host, get_db_number
from ..hashing import generate_hash
from ..helpers import get_timestamp
from ..persistence import RedisChain
from ..publish import publish_mining_required

from  pprint import pprint as pp


# Dumb singleton
#
# NOTE!  Initialization of this singleton is done at the bottom of this file
#
Chain = None


class _Chain:

    def __init__(self):
        self.__blockchain = []
        self.__forks = []
        self.__orphans = []
        self.__db = RedisChain()

    def __len__(self):
        return len(self.__db)

    def __iter__(self):
        return iter(self.__blockchain)

    def _init_genesis_block(self):
        print('Looking up genesis len', self.__db.db_num)

        if len(self) < 1:
            genesis_block = get_genesis_block()
            genesis_block.check_block_header()
            genesis_block.check_block()
            self.add_block(genesis_block)

    def _reset(self):
        print('Clearing chain')
        print(self.__db.clear())
        print('Chain cleared')
        self._init_genesis_block()

    def add_block(self, block):
        self.__db.append(block)

    def _get_new_block_header(self, block, transactions):
        # This is not really a merkle root.  Instead, simply hash all of the hashes for each
        # transaction
        fake_merkle_root = Transaction.generate_hash_for_transactions(transactions)
        return BlockHeader(
                prev_hash=block.hash,
                merkle_root=fake_merkle_root,
                timestamp=get_timestamp(),
                target=TARGET,
        )

    def _create_candidate_header(self, transactions, last_block=None):
        last_block = last_block or self.get_last_block()
        return self._get_new_block_header(last_block, transactions)

    def get_last_block(self):
        return self.__db.get_item_at(-1)

    def add_new_block(self, block):
        if not self.validate_block(block):
            return None

        print('Adding new valid block to chain')
        self.add_block(block)
        return True

    def create_candidate_block(self, transactions):
        print("Creating candidate block!")
        db_num = get_db_number()
        print('Publishing. DB number: %s' % (db_num, ))
        payload = {
            'transactions': [t._raw_data for t in transactions],
            'callback_url': 'https://%s/verifyblock/%s' % (get_host(), db_num),
            'db_number': db_num,
        }
        publish_mining_required(payload)

    def validate_block(self, block):
        # Validate this block is consistent
        block.check_block_header()
        block.check_block()

        # valiate the chain
        prev_block = self.get_last_block()

        # either one of these signifies breaking of the chain, so need to handle that.
        if prev_block.index + 1 != block.index:
            print('Unexpected block index!')
            return False
        if prev_block.hash != block.header.prev_hash:
            print('Mismatch block hashes!')
            print('Prev block hash: %s' % prev_block.hash)
            print('New block prev hash: %s' % block.header.prev_hash)
            return False

        # if prev_block.hash != hash(prev_block):
        #     return False

        return True


# Dumb initialization
if Chain is None:
    Chain = _Chain()
