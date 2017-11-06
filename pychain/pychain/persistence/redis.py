import redis
import pickle

import os

from ..globals import get_db_number


REDIS_HOST = os.environ['PYCHAIN_REDIS_HOST']


def redis_handle(func):
    def _inner(self, *args, **kwargs):
        if self._db is None:
            db_num = get_db_number()
            self._db = redis.StrictRedis(host=REDIS_HOST, port=6379, db=db_num)
        return func(self, *args, **kwargs)

    return _inner


class _RedisList:
    LIST_NAME = '__test'

    def __init__(self):
        self._db = None

    @redis_handle
    def __iter__(self):
        return (pickle.loads(t) for t in self.db.lrange(self.LIST_NAME, 0, -1))

    def __len__(self):
        return self.get_list_length()

    @property
    def db(self):
        return self._db

    @redis_handle
    def append(self, block):
        if not isinstance(block, str):
            block = pickle.dumps(block)
        return self.db.rpush(self.LIST_NAME, block)

    @redis_handle
    def clear(self):
        return self.db.delete(self.LIST_NAME)

    @redis_handle
    def get_list_length(self):
        return self.db.llen(self.LIST_NAME) or 0

    @redis_handle
    def get_item_at(self, index=0):
        result = self.db.lindex(self.LIST_NAME, index)
        if not result:
            return None
        #block = result.decode('utf-8')
        return pickle.loads(result)


class RedisChain(_RedisList):
    LIST_NAME = 'block'


class RedisTransactionPool(_RedisList):
    LIST_NAME = 'tpool'

    @redis_handle
    def get_transactions(self):
        return [pickle.loads(t) for t in self.db.lrange(self.LIST_NAME, 0, -1)]

    @redis_handle
    def record_pending_transactions(self, transactions):
        p = RedisPendingTransactions()
        p.add_transactions(transactions)
        self.clear()
        #transactions = [pickle.dumps(t) for t in transactions]
        #return self.db.rpush('pending', *transactions)


class RedisPendingTransactions(_RedisList):
    LIST_NAME = 'pending'

    @redis_handle
    def add_transactions(self, transactions):
        transactions = [pickle.dumps(t) for t in transactions]
        return self.db.rpush(self.LIST_NAME, *transactions)
