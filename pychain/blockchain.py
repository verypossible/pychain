LIST = 'block'

r = redis.StrictRedis(
        host='redis',
        port=6379,
        db=0)


def get_timestamp():
    return int(time.time() * 1000)


class Block:

    def __init__(self, index, prev_hash, timestamp, data, _hash=None):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = timestamp

        # the data we store needs to be sorted, otheriwse hashing will not work in a distributed manner
        if hasattr(data, 'keys'):
            data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        self.data = data

        self.hash = _hash if _hash else self._calculate_hash()

    def as_dict(self):
        data = self.data
        if hasattr(data, 'decode'):
            data = data.decode('utf-8')

        prev_hash = self.prev_hash
        if hasattr(prev_hash, 'decode'):
            prev_hash = prev_hash.decode('utf-8')

        _hash = self.hash
        if hasattr(_hash, 'decode'):
            _hash = _hash.decode('utf-8')

        return {
                'index': self.index,
                'prev_hash': prev_hash,
                'timestamp': self.timestamp,
                'data': data,
                'hash': _hash,
        }

    def _calculate_hash(self):
        m = hashlib.sha256()
        for item in (self.index, self.prev_hash, self.timestamp, self.data):
            m.update(str(item).encode('utf-8'))
        return m.hexdigest()


class BlockException(Exception):
    pass


_GENSIS_BLOCK = Block(
            0,
            b'0',
            get_timestamp(),
            b'my genesis block!!',
            b'816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7',
)


def add_block_to_redis(block):
    b = pickle.dumps(block)
    return r.rpush(LIST, b)


def add_genesis_block():
    result = r.set('GENESIS', _GENSIS_BLOCK.hash)
    was_added = add_block_to_redis(_GENSIS_BLOCK)
    return result


