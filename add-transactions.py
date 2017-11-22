import json
import requests


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


URL = 'https://6waijngu6i.execute-api.us-east-1.amazonaws.com/dev/3'
data_array = [create_fake_obj() for i in range(21)]

for obj in data_array[:5]:
    resp = requests.post(URL, json=obj)
    if resp.status_code == 200:
        print(resp.json())
    else:
        print(resp.text)
