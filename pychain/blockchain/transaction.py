import json

from collections import OrderedDict

from ..hashing import generate_hash


class Transaction:

    def __init__(self, data):
        """Only allow json encodable things for now"""
        # the data we store needs to be sorted, otheriwse hashing will not work in a distributed manner
        if hasattr(data, 'keys'):
            data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

        # if not isinstance(data, (dict, list, tuple, str, float, int)):
        #     raise Exception('Can only use built-in types')

        self._data = json.dumps(data)

        # ensure data is non-empty
        if not self._data:
            assert self._data

    def generate_hash(self):
        return generate_hash(self._data)
        # if isinstance(self._data, str) or not hasattr(self._data, '__iter__'):
        #     return generate_hash(self._data)
        # else:
        #     data = (json.dumps(d) for d in self._data)
        #     return generate_hash(data)
