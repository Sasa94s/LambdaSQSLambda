import json
from logger import get_logger

logger = get_logger()


def lambda_handler(event, context):
    if len(event.get('Records', [])) == 0:
        logger.info('No records')
        return {
            'statusCode': 400,
            'body': 'No records',
        }
    records = event['Records']
    logger.info('Polling - Messages Count: {}'.format(len(records)))

    return {
        'statusCode': 200,
        'body': json.dumps([record['body'] for record in records]),
    }
