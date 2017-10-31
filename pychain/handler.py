import json

import sys
from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))


from pychain.blockchain.miner import mine
from pychain.blockchain.block_header import BlockHeader
from pychain.blockchain.transaction import Transaction
from pychain.blockchain.constants import TARGET
from pychain.helpers import get_timestamp


def _get_new_block_header(last_block, transactions):
    # This is not really a merkle root.  Instead, simply hash all of the hashes for each
    # transaction
    fake_merkle_root = Transaction.generate_hash_for_transactions(transactions)
    return BlockHeader(
            prev_hash=last_block['pow_hash'],
            merkle_root=fake_merkle_root,
            timestamp=get_timestamp(),
            target=TARGET,
    )


def sns_mine(event, context):
    record = event.get('Records', [])[0]
    payload = json.loads(record['Sns']['Message'])
    print(payload)

    transactions = [Transaction(t) for t in payload['transactions']]
    print(transactions)
    last_block = payload['last_block']

    header = _get_new_block_header(last_block, transactions)

    print('Start mining')
    print(mine(header))


def web_mine(event, context):
    print(event)

    nonce, valid_hash = None, None

    try:
        payload = json.loads(event['body'])

        transactions = [Transaction(t) for t in payload['transactions']]
        last_block = payload['last_block']

        header = _get_new_block_header(last_block, transactions)
        print(type(header))

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
        raise

    if nonce is not None and valid_hash is not None:
        header.nonce = nonce
        response = {
                'success': True,
                'msg': 'Mining complete',
                'header': header.to_primitive(),
                'valid_hash': valid_hash,
                'transactions': [t.to_primitive() for t in transactions],
        }

    return {
            'statusCode': 200,
            'body': json.dumps(response),

    }
