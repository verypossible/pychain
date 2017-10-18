from .block import Block
from .block_entry import BlockEntry

from ..helpers import get_timestamp

GENESIS_BLOCK = Block(index=0, prev_hash='0', timestamp=get_timestamp())


class _Chain:

    def __init__(self):
        self.__blockchain = []
        self.__entries = []

    def __len__(self):
        return len(self.__blockchain)

    def _get_new_block(self, current_block):
        current_block.close()
        new_block = Block(
                index=current_block.index + 1,
                prev_hash=current_block.hash,
                timestamp=get_timestamp(),
        )
        assert self.is_valid_new_block(new_block, current_block)
        return new_block

    def add_entry(self, data):
        block_entry = BlockEntry(data)

        # if this is the genesis block, add it and create the first block
        if not self.__blockchain:
            GENESIS_BLOCK.add_entry(block_entry)
            self.__blockchain.append(GENESIS_BLOCK)
            next_block = self._get_new_block(GENESIS_BLOCK)
            self.__blockchain.append(next_block)
        else:
            current_block = self.get_current_block()
            if current_block.is_closed():
                current_block = self._get_new_block(current_block)
                self.__blockchain.append(current_block)
            current_block.add_entry(block_entry)

    def get_current_block(self):
        return self.__blockchain[-1]

    def is_valid_new_block(self, new_block, prev_block):
        # If the blockhain is empty, the first entry is defined to be valid
        if not self.__blockchain:
            return True

        if new_block.index != prev_block.index + 1:
            return False

        if new_block.prev_hash != prev_block.hash:
            return False

        # if hash(prev_block) != prev_block.hash:
        #     return False

        return True

# dumb singletone
Chain = _Chain()
