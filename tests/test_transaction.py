import pytest

from pychain.blockchain.transaction import (
        Transaction,
)


_test_data = (
        (
            'abc',
            '6cc43f858fbb763301637b5af970e2a46b46f461f27e5a0f41e009c59b827b25'
        ),
        (
            ('a', 'b', 'c'),
            'd33b202c020cbde1c4a7bb26d0b02e66645407dcef42c63543cff899b8f979c8'
        ),
        (
            ['a', 'b', 'c'],
            'd33b202c020cbde1c4a7bb26d0b02e66645407dcef42c63543cff899b8f979c8'
        ),
        (   ['c', 'a', 'b'],
            '4e66376f31ef090741ee72f1d29d238ab41203aee79324072e3623aa3f6180dd'
        ),
        (
            {'msg': 'hello', 'sender': 'test', 'year': 2017},
            '6fbd26f5b1b746b20488ba744aba012185d99d32264084c8b48fd530dfb9243d'
        ),
        (
            {'year': 2017, 'sender': 'test', 'msg': 'hello'},
            '6fbd26f5b1b746b20488ba744aba012185d99d32264084c8b48fd530dfb9243d'
        ),
        (
            ({'one': 1}, {'zzz': 'abc', 'aaa': 123}),
            'd1012c41fb2b10d36f3549cceee506cd5c120c38d5d8dcc202b8adf8137d2ce4'
        ),
        # Note, there is no sub-sorting of dicts so this one will fail
        # (
        #     ({'one': 1}, {'aaa': 123, 'zzz': 'abc'}),
        #     'd1012c41fb2b10d36f3549cceee506cd5c120c38d5d8dcc202b8adf8137d2ce4'
        # ),
        (
            ([1, 2], ('abc', ), {'one': 1}),
            'ab8ff824aa7d46400a90973eb75026d1961b11c025799f7a7482223f5866963e'
        ),
)

@pytest.mark.parametrize('data, expected_hash', _test_data)
def test_hashing(data, expected_hash):
    transaction = Transaction(data)
    assert transaction.generate_hash() == expected_hash
