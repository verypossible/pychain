import json

import sys
from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

import requests

from pychain.handlers import (
        handle_mining,
        handle_index,
        handle_add_new_block,
        handle_add_transaction,
)
from pychain.globals import middleware


@middleware
def index(event, context):
    params = event.get('queryStringParameters') or {}
    reset = True if params.get('reset') else False
    return {
            'statusCode': 200,
            'body': json.dumps(handle_index(reset)),
    }


@middleware
def add_transaction(event, context):
    """Add a transaction to the transaction pool.

    This comes in over https as a POST.

    Supports adding transactions for up to 3 different hosts, which arrive as part of the URL in
    the form of $HOST/${id}/.  If no id is found then we default to 1.

    """
    is_broadcasting = True if '/broadcast' in event['path'] else False
    transaction = json.loads(event['body'])
    msg = handle_add_transaction(transaction, is_broadcasting=is_broadcasting)
    return {
            'statusCode': 200,
            'body': json.dumps(msg),
    }


def sns_mine(event, context):
    print(event)
    # Decode the payload and kick over to the library for processing.
    record = event.get('Records', [])[0]
    payload = json.loads(record['Sns']['Message'])

    transactions = payload['transactions']
    last_block = payload['last_block']
    callback_url = payload.get('callback_url')

    header, pow_hash, transactions = handle_mining(last_block, transactions)
    response = {
            'success': True if header.nonce else False,
            'msg': 'Mining complete',
            'header': header.to_primitive(),
            'pow_hash': pow_hash,
            'transactions': [t._raw_data for t in transactions],
    }
    if callback_url:
        resp = requests.post(callback_url, json=response)
        print(resp)
        print(resp.text)

    return json.dumps(resp.json())


def verify_new_block(event, context):
    payload = json.loads(event['body'])
    print(payload)
    response = handle_add_new_block(**payload)
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
