from ..hashing import generate_hash

from .transaction import Transaction


class BlockError(Exception):
    pass


class Block:

    BLOCK_SIZE = 5

    def __init__(self, *, index, prev_hash, timestamp):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.block_hash = None
        self.__transactions = []
        self.__is_closed = False
        self.hash = None

    def __len__(self):
        return len(self.__transactions)

    def generate_hash(self):
        transaction_hashes = [t.generate_hash() for t in self.__transactions]
        # Critical component is to add the previous hash as part of the data to create this blocks
        # hash.  Without this, the block's hash isn't secure in any way.
        return generate_hash([self.prev_hash] + transaction_hashes)

    def add_transaction(self, transaction):
        if self.__is_closed:
            raise BlockError('Cannot add to closed block')

        if not isinstance(transaction, Transaction):
            transaction = Transaction(transaction)

        self.__transactions.append(transaction)
        if len(self.__transactions) >= self.BLOCK_SIZE:
            self.close()

    def close(self):
        # Close off this block, no more writing
        self.hash = self.generate_hash()
        self.__is_closed = True

    def is_closed(self):
        return self.__is_closed

    def as_dict(self):
        data = self.data
        if hasattr(data, 'decode'):
            data = data.decode('utf-8')

        prev_hash = self.prev_hash
        if hasattr(prev_hash, 'decode'):
            prev_hash = prev_hash.decode('utf-8')

        _hash = self.hash
        if hasattr(_hash, 'decode'):
            _hash = _hash.decode('utf-8')

        return {
                'index': self.index,
                'prev_hash': prev_hash,
                'timestamp': self.timestamp,
                'data': data,
                'hash': _hash,
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


def add_block_from_http_payload(data):
    previous_block = get_latest_block()
    new_block = generate_next_block(data, previous_block)

    validate_block(new_block, previous_block)

    print(add_block_to_redis(new_block))
    return new_block



def get_latest_block(as_dict=False):
    item = r.lrange(LIST, -1, -1)[0]
    block = pickle.loads(item)
    if as_dict:
        block = block.as_dict()
    return block


def get_genesis_block():
    return r.get('GENESIS') == _GENSIS_BLOCK.hash


def generate_next_block(block_data, previous_block=None):
    previous_block = previous_block or get_latest_block()
    next_index = previous_block.index + 1
    next_timestamp = get_timestamp()
    return Block(next_index, previous_block.hash, next_timestamp, block_data)


def validate_block(new_block, previous_block):
    if previous_block.index + 1 != new_block.index:
        raise BlockException('invalid index')

    if previous_block.hash != new_block.prev_hash:
        raise BlockException('invalid previoushash');

    return True



