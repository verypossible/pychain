import requests

from .constants import PEERS
from .globals import get_host, get_db_number


def broadcast(*items):
    me = get_db_number()

    host = get_host()
    urls = ('https://%s/broadcast/%s' % (host, i) for i in PEERS if i != me)

    for item in items:
        for url in urls:
            print('publishing to %s' % url)
            r = requests.post(url, json=item.to_primitive())
            print(r, r.text, item.to_primitive())


def broadcast_new_block(block):
    me = get_db_number()

    host = get_host()
    urls = ('https://%s/block/%s' % (host, i) for i in PEERS if i != me)

    for url in urls:
        print('broadcasting new block to %s' % url)
        r = requests.post(url, json=block.to_primitive())
        print(r, r.text, block.to_primitive())
