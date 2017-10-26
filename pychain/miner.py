from flask import Flask, jsonify, request

from pychain.blockchain.miner import mine
from pychain.blockchain.block import BlockError
from pychain.blockchain.block_header import BlockHeader

from pprint import pprint as pp

app = Flask(__name__)


@app.route('/mine', methods=['POST'])
def mine_new_block():
    payload = request.get_json() or request.get_data().decode('utf-8')

    try:
        header = BlockHeader(**payload)
        nonce, valid_hash = mine(header)
    except Exception as e:
        return jsonify({
            'success': False,
            'msg': str(e),
        })

    if nonce is None or valid_hash is None:
        success = False
    else:
        success = True
        header.nonce = nonce
    #return (True, header, valid_hash)

    return jsonify({
            'msg': 'Mining complete',
            'success': True,
            'header': header.to_primitive(),
            'valid_hash': valid_hash,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
