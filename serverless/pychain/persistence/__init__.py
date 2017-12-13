from .redis import (
        RedisChain,
        RedisTransactionPool,
        RedisPendingTransactions,
)


def clear_all_dbs():
    for db in (RedisChain, RedisTransactionPool, RedisPendingTransactions):
        db().clear()
