import json


_event = {}


def get_host():
    host = _event.get('headers', {}).get('Host', '')
    path = _event['requestContext']['stage']
    return '%s/%s' % (host, path)


def _get_db_number_from_path():
    path_params = _event.get('pathParameters') or {}
    db_number = int(path_params.get('db_number', 1))
    try:
        db_number = int(path_params.get('db_number', 1))
    except Exception as e:
        print(e)
        db_number = 1
    return db_number


def _get_db_number_from_sns():
    if 'Records' not in _event:
        return None

    print('Looking up db_number from sns event')
    record = _event.get('Records', [])[0]
    payload = json.loads(record['Sns']['Message'])
    print(int(payload['db_number']))
    return int(payload['db_number'])


def get_db_number():
    db_num = _get_db_number_from_sns()
    if db_num:
        return db_num

    return _get_db_number_from_path()


def _init_genesis_block():
    # import here to prevent circular imports
    from .blockchain import Chain
    Chain._init_genesis_block()


def middleware(fn):
    """Apply some middleware to set globals on thread local context"""
    def _lambda_call(event, context):
        global _event
        _event = event
        _init_genesis_block()
        return fn(event, context)

    return _lambda_call
