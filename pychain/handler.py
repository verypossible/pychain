import json

import sys
from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

from pychain.handlers import (
        handle_mining,
        handle_index,
)


def index(event, context):
    params = event.get('queryStringParameters') or {}
    reset = True if params.get('reset') else False
    return {
            'statusCode': 200,
            'body': json.dumps(handle_index(reset)),
    }


def add_transaction(event, context):
    print(event)
    msg = {'msg': 'hello'}
    transaction = json.loads(event['body'])
    handle_add_transaction(transaction)
    return {
            'statusCode': 200,
            'body': json.dumps(msg),
    }


def sns_mine(event, context):
    # Decode the payload and kick over to the library for processing.
    record = event.get('Records', [])[0]
    payload = json.loads(record['Sns']['Message'])

    transactions = payload['transactions']
    last_block = payload['last_block']

    header, pow_hash, transactions = handle_mining(last_block, transactions)
    response = {
            'success': True,
            'msg': 'Mining complete',
            'header': header.to_primitive(),
            'pow_hash': pow_hash,
            'transactions': [t.to_primitive() for t in transactions],
    }
    return {
            'statusCode': 200,
            'body': json.dumps(response),
    }


def web_mine(event, context):
    error = None
    try:
        payload = json.loads(event['body'])
        transactions = payload['transactions']
        last_block = payload['last_block']
    except KeyError as e:
        error = 'Missing key: %s' % (e, )
    except Exception as e:
        error = str(e)

    if error is not None:
        response = {
            'success': False,
            'msg': error,
            'header': None,
            'valid_hash': '',
            'transactions': None,
        }
        return {
                'statusCode': 200,
                'body': json.dumps(response),
        }

    header, pow_hash, transactions = handle_mining(last_block, transactions)
    response = {
            'success': True,
            'msg': 'Mining complete',
            'header': header.to_primitive(),
            'pow_hash': pow_hash,
            'transactions': [t.to_primitive() for t in transactions],
    }
    return {
            'statusCode': 200,
            'body': json.dumps(response),
    }
