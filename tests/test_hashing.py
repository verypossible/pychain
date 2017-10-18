import pytest

from pychain.hashing import generate_hash


def test_basic_hashing():
    expected = '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090'
    assert generate_hash('abc123') == expected


_hashing_data = (
        (('abc123', 13123), 'b1393fe36ecd179949daa005cc2f18631c69be1076e086d4d726fe150395e2f2'),
        (range(10, 20), '7ffe8444eb12480cb32785fc32844f642e6bc36291d1c4ca38cf21e369cbc3a9'),
        ((1, 0x001, 123456, 'hello'), 'b948a2326f89927dc866c19af654ba28aa68c6be69cc412acdd61f9d379b9600'),
)

@pytest.mark.parametrize('data, expected', _hashing_data)
def test_basic_hashing(data, expected):
    assert generate_hash(data) == expected


def test_hash_same_results():
    assert generate_hash('bz') == generate_hash('bz')
