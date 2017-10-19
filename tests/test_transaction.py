import pytest

from pychain.blockchain.transaction import (
        Transaction,
)


_test_data = (
        #('abc', 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'),
        (('a', 'b', 'c'), 'd33b202c020cbde1c4a7bb26d0b02e66645407dcef42c63543cff899b8f979c8'),
        (['a', 'b', 'c'], 'd33b202c020cbde1c4a7bb26d0b02e66645407dcef42c63543cff899b8f979c8'),
        (['c', 'a', 'b'], '4e66376f31ef090741ee72f1d29d238ab41203aee79324072e3623aa3f6180dd'),
        #({'msg': 'hello', 'sender': 'test', 'year': 2017}, 'abc'),
        #(({'one': 1}, {'another': 'baadf'}), 'abc'),
        #(([1, 2], ('abc'), {'one': 1}), 'abc'),
)

@pytest.mark.parametrize('data, expected_hash', _test_data)
def test_hashing(data, expected_hash):
    #import pdb; pdb.set_trace()
    transaction = Transaction(data)
    assert transaction.generate_hash() == expected_hash


def test_hashing_of_different_dicts():
    pass
