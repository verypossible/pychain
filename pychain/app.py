import pickle
import json

from flask import Flask, jsonify, request

from pychain.blockchain import Chain
from pychain.blockchain.block import BlockError
from pychain.blockchain.transaction_pool import add_transaction

from pprint import pprint as pp

app = Flask(__name__)


@app.route('/')
def index():
    #count = r.llen(LIST) or 0
    return jsonify({
        'num_blocks': len(Chain),
        'latest_block': Chain.get_last_block().as_dict()
    })


@app.route('/add', methods=['POST'])
def add_block():
    payload = request.get_json() or request.get_data().decode('utf-8')
    # pp(payload)
    # return jsonify(payload)
    try:
        add_transaction(payload)
    except BlockError as e:
        return jsonify({'errors': str(e)})

    return jsonify({
            'msg': 'Transaction adding to transaction pool.',
            'success': True,
    })



@app.route('/blockchain')
def list_blockchain():
    #items = [pickle.loads(data) for data in r.lrange(LIST, -5, -1)]
    items = [t.as_dict() for t in Chain]
    return jsonify(items)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
