import time


def get_timestamp():
    """Return epoch time in milliseconds"""
    return int(time.time() * 1000)
