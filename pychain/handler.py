import json

import sys
from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

from pychain.blockchain.miner import mine
from pychain.blockchain.block_header import BlockHeader


def sns_mine(event, context):
    record = event.get('Records', [])[0]
    header = json.loads(record['Sns']['Message'])
    print(header)
    header = BlockHeader(**header)
    print('Start mining')
    print(mine(header))


def web_mine(event, context):
    print(event)

    nonce, valid_hash = None, None

    try:
        payload = json.loads(event['body'])
        header = payload['header']
        transactions = payload['transactions']
        header = BlockHeader(**header)
        nonce, valid_hash = mine(header)
    except KeyError as e:
        msg = 'Missing key: %s' % (e, )
        response = {
            'success': False,
            'msg': msg,
            'header': None,
            'valid_hash': '',
            'transactions': None,
        }
    except Exception as e:
        response = {
            'success': False,
            'msg': str(e),
            'header': None,
            'valid_hash': '',
            'transactions': None,
        }

    if nonce is not None and valid_hash is not None:
        header.nonce = nonce
        response = {
                'success': True,
                'msg': 'Mining complete',
                'header': header.to_primitive(),
                'valid_hash': valid_hash,
                'transactions': transactions,
        }

    return {
            'statusCode': 200,
            'body': json.dumps(response),

    }
