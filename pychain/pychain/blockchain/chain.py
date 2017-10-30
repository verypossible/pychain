import json
import requests

from .block import Block
from .block_header import BlockHeader
from .constants import TARGET
from .genesis import get_genesis_block
from .transaction import Transaction

from ..hashing import generate_hash
from ..helpers import get_timestamp


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

    def __len__(self):
        return len(self.__blockchain)

    def __iter__(self):
        return iter(self.__blockchain)

    def _init_genesis_block(self):
        if not self.__blockchain:
            genesis_block = get_genesis_block()
            genesis_block.check_block_header()
            genesis_block.check_block()
            self.__blockchain.append(genesis_block)

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
        header = self._get_new_block_header(last_block, transactions)
        self._send_to_miners(transactions, header, last_block)

    def _send_to_miners(self, transactions, header, last_block):
        response = requests.post(
                'http://miner:5001/mine',
                json={
                    'transactions': [t.to_primitive() for t in transactions],
                    'header': header.to_primitive(),
                },
                headers={'Content-Type': 'application/json'},
        )
        payload = response.json()
        if not payload.get('success', False):
            print('error mining')
            return

        json_response = response.json()
        # this is the new header, with the nonce from the mining
        mined_header = BlockHeader(**json_response['header'])

        # linking looks good
        assert mined_header.prev_hash == last_block.hash

        #assert header == json_response['header']

        from  pprint import pprint as pp
        import sys
        sys.stdout = sys.stderr
        pp(json_response)

        # Validate that the nonce returned from the miner creates a valid block
        assert mined_header.generate_hash(nonce=mined_header.nonce) == json_response['valid_hash']
        print('Mining completed successfully!')


    def add_block(self, block):
        self.__blockchain.append(block)

    def create_candidate_block(self, transactions):
        print("Creating candidate block!")
        last_block = self.get_last_block()
        # note, this does the mining
        self._create_candidate_header(transactions, last_block)

    def add_new_block(self, block):
        success, header, valid_hash = self._create_candidate_header(transactions, last_block)
        print(success, header, valid_hash)
        if not success:
            return None

        block = Block(
                    index=last_block.index + 1,
                    header=header,
                    transactions=transactions,
                    pow_hash=valid_hash,
        )
        block.check_block_header()
        block.check_block()

        is_valid = self.is_valid_new_block(last_block, block)
        print('Found a new block, is it valid???', is_valid)
        if is_valid:
            self.add_block(block)

        return block

    def get_last_block(self):
        return self.__blockchain[-1]

    def is_valid_new_block(self, prev_block, new_block):
        # If the blockhain is empty, the first entry is defined to be valid
        if not self.__blockchain:
            return True

        if prev_block.index + 1 != new_block.index:
            print('Unexpected block index!')
            return False

        if prev_block.hash != new_block.header.prev_hash:
            print('Mismatch block hashes!')
            return False

        # if prev_block.hash != hash(prev_block):
        #     return False

        return True


# Dumb initialization
if Chain is None:
    Chain = _Chain()
