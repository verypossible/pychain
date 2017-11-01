import redis
import pickle

import os


REDIS_HOST = os.environ['PYCHAIN_REDIS_HOST']
REDIS_DB_NUMBER = int(os.environ.get('PYCHAIN_REDIS_DB_NUMBER', 0))


class RedisChain:
    LIST_NAME = 'block'

    def __init__(self):
        self.__db = None

    def __get_redis(self):
        if self.__db is None:
            self.__db = redis.StrictRedis(host=REDIS_HOST, port=6379, db=REDIS_DB_NUMBER)
        return self.__db

    def add_block_to_chain(self, block):
        r = self.__get_redis()
        if not isinstance(block, str):
            block = pickle.dumps(block)
        return r.rpush(LIST_NAME, block)

    def clear_chain(self):
        r = self.__get_redis()
        return r.delete(LIST_NAME)

    def get_chain_length(self):
        r = self.__get_redis()
        return r.llen(LIST_NAME) or 0

    def get_block_at(self, index=0):
        r = self.__get_redis()
        result = r.lindex(LIST_NAME, index)
        if not result:
            return None
        #block = result.decode('utf-8')
        return pickle.loads(result)


class RedisTransactionPool:

    LIST_NAME = 'tpool'

    def __init__(self):
        self.__db = None

    def __get_redis(self):
        if self.__db is None:
            self.__db = redis.StrictRedis(host=REDIS_HOST, port=6379, db=REDIS_DB_NUMBER)
        return self.__db

    def add_to_pool(self, t):
        r = self.__get_redis()
        if not isinstance(t, str):
            t = pickle.dumps(t)
        return r.rpush(LIST_NAME, t)

    def clear_pool(self):
        r = self.__get_redis()
        return r.delete(LIST_NAME)

    def get_pool_length(self):
        r = self.__get_redis()
        return r.llen(LIST_NAME) or 0

    def get_transactions(self):
        r = self.__get_redis()
        return [pickle.loads(t) for t in r.lrange(LIST_NAME, 0, -1)]

    def record_pending_transactions(self, transactions):
        transactions = [pickle.dumps(t) for t in transactions]
        return r.rpush('pending', *transactions)
