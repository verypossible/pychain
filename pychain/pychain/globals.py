import threading

from .blockchain.constants import DEFAULT_DB_NUMBER


_request_local = threading.local()


def get_host():
    return _request_local.host


def get_db_number():
    if not hasattr(_request_local, 'db_number'):
        _request_local.db_number = DEFAULT_DB_NUMBER
    return _request_local.db_number


def _set_host_from_event(event):
    if not hasattr(_request_local, 'host'):
        _request_local.host = event['headers']['Host'] + event['requestContext']['path']


def _set_db_number_from_event(event):
    if hasattr(_request_local, 'db_number'):
        return

    path_params = event.get('pathParameters') or {}
    try:
        db_number = int(path_params.get('db_number', 1))
    except Exception as e:
        print(e)
        db_number = 1
    _request_local.db_number = db_number


def middleware(fn):
    """Apply some middleware to set globals on thread local context"""
    def _lambda_call(event, context):
        _set_host_from_event(event)
        _set_db_number_from_event(event)
        return fn(event, context)

    return _lambda_call
