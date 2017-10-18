import hashlib
import time
import pickle
import json

import redis

from collections import OrderedDict
from flask import Flask, jsonify, request

app = Flask(__name__)

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
