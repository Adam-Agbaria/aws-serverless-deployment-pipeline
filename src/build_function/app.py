import boto3
import logging
import os
from unittest.mock import MagicMock

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    try:
        logger.debug(f"Received event: {event}")
        project_name = event["project_name"]

        # Check if running locally
        if os.environ.get('AWS_SAM_LOCAL'):
            logger.debug("Running locally. Using mock for CodeBuild.")
            # Mock boto3 client for local testing
            codebuild = MagicMock()
            codebuild.start_build.return_value = {"buildId": "build-1234"}
        else:
            # Use the actual boto3 client for production
            codebuild = boto3.client('codebuild')

        response = codebuild.start_build(projectName=project_name)
        return {
            'statusCode': 200,
            'body': response
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': str(e)
        }
