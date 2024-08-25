import json
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context, dynamodb=None):
    # If no DynamoDB resource is provided, use the default boto3 resource
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table("PipelineConfig")

    try:
        logger.debug(f"Received event: {event}")

        # Determine the operation: create, read, update, delete
        operation = event.get('operation', '')
        
        if operation == 'create':
            return create_pipeline(table, event['pipeline_data'])
        elif operation == 'read':
            return read_pipeline(table, event['pipeline_id'])
        elif operation == 'update':
            return update_pipeline(table, event['pipeline_id'], event['pipeline_data'])
        elif operation == 'delete':
            return delete_pipeline(table, event['pipeline_id'])
        else:
            return respond(400, "Invalid operation")
    except ClientError as e:
        return respond(500, f"ClientError: {e.response['Error']['Message']}")
    except Exception as e:
        return respond(500, f"Error: {str(e)}")

def create_pipeline(table, pipeline_data):
    table.put_item(Item=pipeline_data)
    return respond(200, "Pipeline created successfully")

def read_pipeline(table, pipeline_id):
    response = table.get_item(Key={'pipeline_id': pipeline_id})
    if 'Item' in response:
        return respond(200, response['Item'])
    else:
        return respond(404, "Pipeline not found")

def update_pipeline(table, pipeline_id, pipeline_data):
    table.update_item(
        Key={'pipeline_id': pipeline_id},
        UpdateExpression="set #name = :n, #desc = :d, #config = :c",
        ExpressionAttributeNames={
            '#name': 'name',
            '#desc': 'description',
            '#config': 'config'
        },
        ExpressionAttributeValues={
            ':n': pipeline_data['name'],
            ':d': pipeline_data['description'],
            ':c': pipeline_data['config']
        }
    )
    return respond(200, "Pipeline updated successfully")

def delete_pipeline(table, pipeline_id):
    table.delete_item(Key={'pipeline_id': pipeline_id})
    return respond(200, "Pipeline deleted successfully")

def respond(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps(message)
    }
