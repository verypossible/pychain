import boto3
import json
import sys
import time



def notify(payload):
    client = boto3.client('sns')
    arn = 'arn:aws:sns:us-east-1:679892560156:PyChainMiners'

    client.publish(
            TopicArn=arn,
            Message=json.dumps({'default': json.dumps(payload)}),
            MessageStructure='json',
    )


if __name__ == '__main__':
    payload = {
        "last_block": {
            "pow_hash": "00000c34d3cf08dd8bccb401fd5a4fc0c37734750abc142bbdcb2f7639a5c230"
        },
        "transactions": [
            "foo",
            "bar",
            "baz",
            {
                "name": "bz", "age": 44, "awesome": True
            }
        ]
    }
    notify(payload)
