import boto3
import json
import sys
import time



def notify(header):
    client = boto3.client('sns')
    arn = 'arn:aws:sns:us-east-1:679892560156:PyChainMiners'

    client.publish(
            TopicArn=arn,
            Message=json.dumps({'default': json.dumps(header)}),
            MessageStructure='json',
    )


if __name__ == '__main__':
    header = {
            "merkle_root": "2f2d7ab3523283b62fe9e1ed89a64247a19a2abb8d80dd22e96a8784d0707d5e",
            "nonce": 151809,
            "prev_hash": "0",
            "target": 1766847064778384329583297500742918515827483896875618958121606201292619776,
            "timestamp": 1508907362,
            "version": 1
    }
    notify(header)
