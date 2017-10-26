import json
import urllib.request

URL = 'http://localhost:5000/add'

# with open('inputs.json') as fh:
#     data_array = json.load(fh)

from faker import Faker
fake = Faker()

def create_fake_obj():
    return {
        'name': fake.name(),
        'address': fake.address(),
        'credit_card': fake.credit_card_number(card_type=None),
        'isbn': fake.isbn13(separator="-"),
        'ssn': fake.ssn(),
    }


data_array = [create_fake_obj() for i in range(21)]

for obj in data_array:
    r = urllib.request.Request(
            URL,
            data=json.dumps(obj).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
    )
    resp = urllib.request.urlopen(r)
    print(json.loads(resp.read()))

