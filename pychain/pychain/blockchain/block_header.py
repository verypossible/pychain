import json

from .constants import TARGET

from ..hashing import generate_hash
from ..helpers import get_timestamp


class BlockHeader:

    def __init__(self, *, prev_hash, merkle_root, timestamp=None, target=TARGET, nonce=0, version=1):
        self.__prev_hash = prev_hash
        self.__merkle_root = merkle_root
        self.__timestamp = timestamp or get_timestamp()
        # this is difficulty
        self.__target = target
        self.__version = version
        self.nonce = nonce

    @staticmethod
    def from_json(payload):
        payload = json.loads(payload)
        return BlockHeader(**payload)

    @property
    def prev_hash(self):
        return self.__prev_hash

    @property
    def merkle_root(self):
        return self.__merkle_root

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def target(self):
        return self.__target

    @property
    def version(self):
        return self.__version

    def to_primitive(self):
        return {
            'prev_hash': self.prev_hash,
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp,
            'target': self.target,
            'version': self.version,
            'nonce': self.nonce,
        }

    def to_json(self):
        return json.dumps(to_primitive)

    def generate_hash(self, *, nonce):
        return generate_hash(
                self.__version,
                self.__prev_hash,
                self.__merkle_root,
                self.__timestamp,
                self.__target,
                nonce,
        )
