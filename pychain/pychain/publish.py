import boto3
import json

from .blockchain.constants import MINING_ARN


def publish_mining_required(payload):
    print('Publishing payload')
    client = boto3.client('sns')
    print('Publishing with client: %s' % client)
    print('Publishing using ARN: %s' % MINING_ARN)
    #payload = json.dumps(payload).encode()
    # client.invoke(
    #     FunctionName='pychain-dev-Mine',
    #     InvocationType='Event',
    #     Payload=payload,
    # )
    client.publish(
            TopicArn=MINING_ARN,
            Message=json.dumps({'default': json.dumps(payload)}),
            MessageStructure='json',
    )
    print('done')
