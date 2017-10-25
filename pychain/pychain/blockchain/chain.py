from .block import Block
from .block_header import BlockHeader
from .block_header import BlockHeader
from .constants import TARGET
from .miner import mine
from .transaction import Transaction

from ..hashing import generate_hash
from ..helpers import get_timestamp


# dumb singleton
Chain = None


def get_genesis_block():
    h = BlockHeader(
            prev_hash='0',
            merkle_root='2f2d7ab3523283b62fe9e1ed89a64247a19a2abb8d80dd22e96a8784d0707d5e',
            timestamp=1508907362,
            target=2 ** (256 - 16),
            nonce=151809,
    )
    t = Transaction('Genesis')
    pow_hash = '0000f8b59e9c39b9bdb63793b6a085b465d2ae9a4e3c54759f46f17948eeff7f'
    return Block(index=0, header=h, transactions=[t], pow_hash=pow_hash)


class _Chain:

    def __init__(self):
        self.__blockchain = []
        self.__entries = []

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
        # transation
        fake_merkle_root = Transaction.generate_hash_for_transactions(transactions)
        return BlockHeader(
                prev_hash=block.hash,
                merkle_root=fake_merkle_root,
                timestamp=get_timestamp(),
                target=TARGET,
        )

    def _create_candidate_header(self, transactions, last_block):
        header = self._get_new_block_header(last_block, transactions)

        nonce, valid_hash = mine(header)
        if nonce is None or valid_hash is None:
            return (False, header, None)

        header.nonce = nonce
        return (True, header, valid_hash)

    def create_candidate_block(self, transactions):
        last_block = self.get_last_block()
        success, header, valid_hash = self._create_candidate_header(transactions, last_block)
        if not success:
            return None

        block = Block(
                    index=last_block.index + 1,
                    header=header,
                    transaction=transactions,
                    pow_hash=valid_hash,
        )
        block.check_block_header()
        block.check_block()


    def get_last_block(self):
        return self.__blockchain[-1]

    def is_valid_new_block(self, prev_block, new_block):
        # If the blockhain is empty, the first entry is defined to be valid
        if not self.__blockchain:
            return True

        if prev_block.index + 1 != new_block.index:
            return False

        if prev_block.hash != new_block.prev_hash:
            return False

        # if prev_block.hash != hash(prev_block):
        #     return False

        return True


# Dumb initialization
if Chain is None:
    Chain = _Chain()
    #Chain._init_genesis_block()
