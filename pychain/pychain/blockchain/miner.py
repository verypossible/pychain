import time
from .constants import (
        MAX_NONCE,
        MAX_MINING_TIME,
)
import time


class MiningTimeout(Exception):
    pass


def mine(header, timeout=MAX_MINING_TIME):
    start_time = time.time()
    counter = 0

    for nonce in range(MAX_NONCE):
        hash_result = header.generate_hash(nonce=nonce)
        if int(hash_result, 16) < header.target:
            return (nonce, hash_result)

        counter += 1
        if counter > 100000:
            if time.time() - start_time > timeout:
                raise MiningTimeout('Max time reached')
            counter = 0

    return (None, None)
