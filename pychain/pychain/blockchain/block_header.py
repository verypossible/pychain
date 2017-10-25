from .constants import TARGET

from ..hashing import generate_hash


class BlockHeader:

    def __init__(self, *, prev_hash, merkle_root, timestamp, target=TARGET, nonce=0, version=1):
        self.__prev_hash = prev_hash
        self.__merkle_root = merkle_root
        self.__timestamp = timestamp
        # this is difficulty
        self.__target = target
        self.__version = version
        self.nonce = nonce

    @property
    def target(self):
        return self.__target

    @property
    def merkle_root(self):
        return self.__merkle_root

    def generate_hash(self, *, nonce):
        return generate_hash(
                self.__version,
                self.__prev_hash,
                self.__merkle_root,
                self.__timestamp,
                self.__target,
                nonce,
        )
