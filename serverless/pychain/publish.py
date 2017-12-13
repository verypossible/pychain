import boto3
import json

from .constants import MINING_ARN


def publish_mining_required(payload):
    client = boto3.client('sns')
    client.publish(
            TopicArn=MINING_ARN,
            Message=json.dumps({'default': json.dumps(payload)}),
            MessageStructure='json',
    )
