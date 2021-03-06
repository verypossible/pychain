import json

from collections import OrderedDict

from ..hashing import generate_hash


class Transaction:

    def __init__(self, data):
        """Only allow json encodable things for now"""
        # the data we store needs to be sorted, otheriwse hashing will not work in a distributed
        # manner
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass

        if hasattr(data, 'keys'):
            data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

        self._raw_data = data
        self._data = json.dumps(data)

        # ensure data is non-empty
        if not self._data:
            assert self._data

    def generate_hash(self):
        return generate_hash(self._data)

    def to_primitive(self):
        return self._data
        #return self._raw_data
        # return {
        #     'data': self._data,
        #     'hash': self.generate_hash(),
        # }

    @staticmethod
    def generate_hash_for_transactions(transactions):
        return generate_hash(*[t.generate_hash() for t in transactions])
