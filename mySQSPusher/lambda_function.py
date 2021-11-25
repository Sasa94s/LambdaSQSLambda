import os
import json
import boto3
from uuid import uuid4
from time import time
from logger import get_logger

logger = get_logger()
QUEUE_NAME = os.environ.get('QUEUE_NAME')


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    sqs_queue_url = sqs_client.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
    msg_text = 'Hello from mySQSPusher Lambda! - ts[{}]'.format(time())
    try:
        did = 'did-{}'.format(str(uuid4()))
        gid = 'gid-{}'.format(str(uuid4()))
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=json.dumps({'Message': msg_text}),
                                      MessageDeduplicationId=did, MessageGroupId=gid)
        logger.info('Pushed Message: "{}"'.format(msg))
    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500
        }

    return {
        'statusCode': 200,
        'body': json.dumps(msg_text)
    }
