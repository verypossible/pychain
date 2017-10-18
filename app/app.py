import hashlib
import time
import pickle
import json

import redis

from collections import OrderedDict
from flask import Flask, jsonify, request

app = Flask(__name__)



LIST = 'block'


r = redis.StrictRedis(
        host='redis',
        port=6379,
        db=0)


def get_timestamp():
    return int(time.time() * 1000)


class Block:

    def __init__(self, index, prev_hash, timestamp, data, _hash=None):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = timestamp

        # the data we store needs to be sorted, otheriwse hashing will not work in a distributed manner
        if hasattr(data, 'keys'):
            data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        self.data = data

        self.hash = _hash if _hash else self._calculate_hash()

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

    def _calculate_hash(self):
        m = hashlib.sha256()
        for item in (self.index, self.prev_hash, self.timestamp, self.data):
            m.update(str(item).encode('utf-8'))
        return m.hexdigest()


class BlockException(Exception):
    pass


_GENSIS_BLOCK = Block(
            0,
            b'0',
            get_timestamp(),
            b'my genesis block!!',
            b'816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7',
)


def add_block_to_redis(block):
    b = pickle.dumps(block)
    return r.rpush(LIST, b)


def add_genesis_block():
    result = r.set('GENESIS', _GENSIS_BLOCK.hash)
    was_added = add_block_to_redis(_GENSIS_BLOCK)
    return result


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


@app.route('/')
def index():
    if not get_genesis_block():
        add_genesis_block()

    count = r.llen(LIST) or 0

    return jsonify({
        'number_of_items': count,
        'latest_block': get_latest_block(as_dict=True)
    })


@app.route('/init')
def init_genesis():
    """Create the geneis block"""
    if not get_genesis_block():
        result = add_genesis_block()
        return jsonify({
            'result': 'Genesis block added',
        })
    else:
        return jsonify({
            'result': 'Genesis block already present',
        })


@app.route('/blockchain')
def list_blockchain():
    items = [pickle.loads(data) for data in r.lrange(LIST, -5, -1)]
    items = [i.as_dict() for i in items]
    return jsonify(items)


@app.route('/add', methods=['POST'])
def add_block():
    payload = request.get_json()
    try:
        new_block = add_block_from_http_payload(payload)
        return jsonify(new_block.as_dict())
    except BlockException as e:
        return jsonify({'errors': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
