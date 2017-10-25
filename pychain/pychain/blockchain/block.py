from ..hashing import generate_hash

from .transaction import Transaction


class BlockError(Exception):
    pass


class Block:

    BLOCK_SIZE = 5

    def __init__(self, *, index, header, transactions, pow_hash):
        self.index = index
        self.header = header
        self.__transactions = transactions
        self.__pow_hash = pow_hash

    def __len__(self):
        return len(self.__transactions)

    def check_block_header(self):
        hash_result = self.header.generate_hash(nonce=self.header.nonce)

        if hash_result != self.__pow_hash:
            raise BlockError('Invalid header hash')

        if int(hash_result, 16) >= self.header.target:
            raise BlockError('POW target greater than expected target')

    def check_block(self):
        if len(self.__transactions) < 1:
            raise BlockError('Empty transactions list')

        transactions_hash = Transaction.generate_hash_for_transactions(self.__transactions)
        if transactions_hash != self.header.merkle_root:
            raise BlockError('Invalid merkle_root hash')

    def as_dict(self):
        return {
                'index': self.index,
                'prev_hash': self.prev_hash,
                'timestamp': self.timestamp,
                'transactions': [t._data for t in self.__transactions],
                'hash': self.hash,
                'is_closed': self.is_closed(),
        }


#
# def add_block_to_redis(block):
#     b = pickle.dumps(block)
#     return r.rpush(LIST, b)
#
#
# def add_genesis_block():
#     result = r.set('GENESIS', _GENSIS_BLOCK.hash)
#     was_added = add_block_to_redis(_GENSIS_BLOCK)
#     return result
#
#


# def get_latest_block(as_dict=False):
#     item = r.lrange(LIST, -1, -1)[0]
#     block = pickle.loads(item)
#     if as_dict:
#         block = block.as_dict()
#     return block
#
#
# def get_genesis_block():
#     return r.get('GENESIS') == _GENSIS_BLOCK.hash
#
#
# def generate_next_block(block_data, previous_block=None):
#     previous_block = previous_block or get_latest_block()
#     next_index = previous_block.index + 1
#     next_timestamp = get_timestamp()
#     return Block(next_index, previous_block.hash, next_timestamp, block_data)
