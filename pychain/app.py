import hashlib
import time
import pickle
import json

import redis

from collections import OrderedDict
from flask import Flask, jsonify, request

app = Flask(__name__)


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
