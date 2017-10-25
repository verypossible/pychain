from .constants import MAX_NONCE


def mine(header):
    for nonce in range(MAX_NONCE):
        hash_result = header.generate_hash(nonce=nonce)
        if int(hash_result, 16) < header.target:
            return (nonce, hash_result)

    return (None, None)
