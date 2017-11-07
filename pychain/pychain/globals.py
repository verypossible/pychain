_event = {}


def get_host():
    host = _event.get('headers', {}).get('Host', '')
    path = _event['requestContext']['stage']
    return '%s/%s' % (host, path)


def get_db_number():
    path_params = _event.get('pathParameters') or {}
    try:
        db_number = int(path_params.get('db_number', 1))
    except Exception as e:
        print(e)
        db_number = 1
    return db_number


def middleware(fn):
    """Apply some middleware to set globals on thread local context"""
    def _lambda_call(event, context):
        global _event
        _event = event
        print('setting up middleware')
        return fn(event, context)

    return _lambda_call
