from .block import Block
from .transaction import Transaction

from ..helpers import get_timestamp


# dumb singleton
Chain = None


def get_genesis_block():
    return Block(index=0, prev_hash='0', timestamp=get_timestamp())


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
            genesis_block.add_transaction('Genesis')
            genesis_block.close()
            self.__blockchain.append(genesis_block)

    def _get_new_block(self, current_block):
        current_block.close()
        new_block = Block(
                index=current_block.index + 1,
                prev_hash=current_block.hash,
                timestamp=get_timestamp(),
        )
        assert self.is_valid_new_block(current_block, new_block)
        return new_block

    def add_transaction(self, data):
        transaction = Transaction(data)

        current_block = self.get_current_block()
        if current_block.is_closed():
            current_block = self._get_new_block(current_block)
            self.__blockchain.append(current_block)

        current_block.add_transaction(transaction)

    def get_current_block(self):
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
