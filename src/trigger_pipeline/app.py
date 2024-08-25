import json
import boto3
from botocore.exceptions import ClientError
import logging
from unittest.mock import MagicMock

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context, codepipeline=None):
    # If no CodePipeline client is provided, use a mock client
    if not codepipeline:
        logger.debug("No CodePipeline client provided. Using mock CodePipeline client.")
        codepipeline = MagicMock()

        # Mock the start_pipeline_execution response
        codepipeline.start_pipeline_execution.return_value = {
            'pipelineExecutionId': 'example-execution-id'
        }

    try:
        logger.debug(f"Received event: {event}")
        pipeline_name = event['pipeline_name']

        response = codepipeline.start_pipeline_execution(
            name=pipeline_name
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
