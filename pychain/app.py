import pickle
import json

from flask import Flask, jsonify, request

from pychain.blockchain import Chain
from pychain.blockchain.transaction_pool import add_transaction

from pprint import pprint as pp

app = Flask(__name__)


@app.route('/')
def index():
    #count = r.llen(LIST) or 0
    return jsonify({
        'number_of_items': len(Chain),
        'latest_block': Chain.get_last_block().as_dict()
    })


@app.route('/add', methods=['POST'])
def add_block():
    payload = request.get_json() or request.get_data().decode('utf-8')
    pp(payload)
    return jsonify(payload)
    #try:
    # Chain.add_transaction(payload)
    # block = Chain.get_last_block()
    # return jsonify(block.as_dict())
    # # except BlockException as e:
    #     return jsonify({'errors': str(e)})
    #




@app.route('/blockchain')
def list_blockchain():
    #items = [pickle.loads(data) for data in r.lrange(LIST, -5, -1)]
    items = [t.as_dict() for t in Chain]
    return jsonify(items)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
