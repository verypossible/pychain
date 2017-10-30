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
        header = payload['header']
        transactions = payload['transactions']
        header = BlockHeader(**header)
        nonce, valid_hash = mine(header)
    except KeyError as e:
        msg = 'Missing key: %s' % (e, )
        return jsonify({
            'success': False,
            'msg': msg,
            'header': None,
            'valid_hash': '',
            'transactions': None,
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'msg': str(e),
            'header': None,
            'valid_hash': '',
            'transactions': None,
        })

    if nonce is None or valid_hash is None:
        success = False
    else:
        success = True
        header.nonce = nonce

    return jsonify({
            'success': True,
            'msg': 'Mining complete',
            'header': header.to_primitive(),
            'valid_hash': valid_hash,
            'transactions': transactions,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
