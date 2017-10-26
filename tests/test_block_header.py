import json

from pychain.blockchain.block_header import BlockHeader

_expected_keys = sorted([
        'prev_hash',
        'merkle_root',
        'timestamp',
        'target',
        'nonce',
        'version',
])

def test_to_json():
    h = BlockHeader(
            prev_hash='000abc',
            merkle_root='xyz',
    )
    j = h.to_json()
    deserialized = json.loads(j)
    assert sorted(deserialized.keys()) == _expected_keys

def test_from_json():
    h = BlockHeader(
            prev_hash='000abc',
            merkle_root='xyz',
            timestamp=123456789,
            target=987654321,
            nonce=8888,
            version=88,
    )
    new_header = BlockHeader.from_json(h.to_json())
    assert new_header.prev_hash == '000abc'
    assert new_header.merkle_root == 'xyz'
    assert new_header.timestamp == 123456789
    assert new_header.target == 987654321
    assert new_header.nonce == 8888
    assert new_header.version == 88

