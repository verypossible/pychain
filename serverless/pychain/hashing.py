import hashlib


def generate_hash(*data):
    m = hashlib.sha256()
    for item in data:
        m.update(str(item).encode('utf-8'))
    return m.hexdigest()
