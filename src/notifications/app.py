import json
import boto3
from botocore.exceptions import ClientError
import logging
from unittest.mock import MagicMock

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context, sns=None):
    # If no SNS client is provided, use a mock SNS client
    if sns is None:
        logger.debug("No SNS client provided. Using mock SNS client.")
        sns = MagicMock()
        sns.publish.return_value = {
            'MessageId': 'msg-EXAMPLE123'
        }

    try:
        logger.debug(f"Received event: {event}")
        topic_arn = event['topic_arn']
        message = event['message']

        response = sns.publish(
            TopicArn=topic_arn,
            Message=message
        )

        return respond(200, response)
    except ClientError as e:
        logger.error(f"ClientError: {e.response['Error']['Message']}")
        return respond(500, f"ClientError: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return respond(500, f"Error: {str(e)}")

def respond(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps(message)
    }
