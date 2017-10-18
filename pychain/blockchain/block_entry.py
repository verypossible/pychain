from ..hashing import generate_hash


class BlockEntry:

    def __init__(self, data):
        # the data we store needs to be sorted, otheriwse hashing will not work in a distributed manner
        if hasattr(data, 'keys'):
            data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

        self._data = data

        # ensure data is non-empty but allow for zero
        if not self._data and self._data != 0:
            assert self._data

    def generate_hash(self):
        return generate_hash(self._data)
