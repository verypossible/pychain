from ..hashing import generate_hash

from .transaction import Transaction


class BlockError(Exception):
    pass


class Block:

    def __init__(self, *, index, header, transactions, pow_hash):
        self.index = index
        self.header = header
        self.__transactions = transactions
        self.__pow_hash = pow_hash

    def __len__(self):
        return len(self.__transactions)

    @property
    def hash(self):
        return self.__pow_hash

    def check_block_header(self):
        hash_result = self.header.generate_hash(nonce=self.header.nonce)

        if hash_result != self.__pow_hash:
            raise BlockError('Invalid POW hash')

        if int(hash_result, 16) >= self.header.target:
            raise BlockError('POW target greater than expected target')

    def check_block(self):
        if len(self.__transactions) < 1:
            raise BlockError('Empty transactions list')

        transactions_hash = Transaction.generate_hash_for_transactions(self.__transactions)
        if transactions_hash != self.header.merkle_root:
            raise BlockError('Invalid merkle_root hash')

    def to_primitive(self):
        return {
                'index': self.index,
                'transactions': [(t.generate_hash(), t._raw_data) for t in self.__transactions],
                #'transactions': [t._raw_data for t in self.__transactions],
                'pow_hash': self.__pow_hash,
                'header': {
                    'prev_hash': self.header.prev_hash,
                    'merkle_root': self.header.merkle_root,
                    'timestamp': self.header.timestamp,
                    'target': self.header.target,
                    'version': self.header.version,
                    'nonce': self.header.nonce,
                }
        }
