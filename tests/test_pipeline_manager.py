from unittest.mock import patch, MagicMock
from src.pipeline_manager.app import lambda_handler

@patch('src.pipeline_manager.app.boto3.resource')
def test_create_pipeline(mock_boto_resource):
    print("Mocking boto3.resource")

    # Create a mock DynamoDB Table
    mock_table = MagicMock()
    mock_boto_resource.return_value.Table.return_value = mock_table
    mock_table.put_item.return_value = {}

    event = {
        "operation": "create",
        "pipeline_data": {
            "pipeline_id": "123",
            "name": "MyPipeline",
            "description": "Test pipeline",
            "config": {
                "stage": "dev",
                "region": "us-east-1"
            }
        }
    }

    # Call the lambda function with the mock dynamodb resource
    response = lambda_handler(event, {}, mock_boto_resource.return_value)

    # Check the mock calls
    print("Mock calls:", mock_boto_resource.mock_calls)
    assert response['statusCode'] == 200

    # Ensure the correct method was called
    mock_table.put_item.assert_called_once_with(Item=event['pipeline_data'])


@patch('src.pipeline_manager.app.boto3.resource')
def test_read_pipeline(mock_boto_resource):
    print("Mocking boto3.resource")

    # Create a mock DynamoDB Table
    mock_table = MagicMock()
    mock_boto_resource.return_value.Table.return_value = mock_table
    mock_table.get_item.return_value = {'Item': {"pipeline_id": "123", "name": "MyPipeline"}}

    event = {
        "operation": "read",
        "pipeline_id": "123"
    }

    # Call the lambda function with the mock dynamodb resource
    response = lambda_handler(event, {}, mock_boto_resource.return_value)

    # Check the mock calls
    print("Mock calls:", mock_boto_resource.mock_calls)
    assert response['statusCode'] == 200

    # Ensure the correct method was called
    mock_table.get_item.assert_called_once_with(Key={'pipeline_id': '123'})


@patch('src.pipeline_manager.app.boto3.resource')
def test_update_pipeline(mock_boto_resource):
    print("Mocking boto3.resource")

    # Create a mock DynamoDB Table
    mock_table = MagicMock()
    mock_boto_resource.return_value.Table.return_value = mock_table
    mock_table.update_item.return_value = {}

    event = {
        "operation": "update",
        "pipeline_id": "123",
        "pipeline_data": {
            "name": "MyUpdatedPipeline",
            "description": "Updated pipeline",
            "config": {
                "stage": "prod",
                "region": "us-west-2"
            }
        }
    }

    # Call the lambda function with the mock dynamodb resource
    response = lambda_handler(event, {}, mock_boto_resource.return_value)

    # Check the mock calls
    print("Mock calls:", mock_boto_resource.mock_calls)
    assert response['statusCode'] == 200

    # Ensure the correct method was called
    mock_table.update_item.assert_called_once_with(
        Key={'pipeline_id': '123'},
        UpdateExpression="set #name = :n, #desc = :d, #config = :c",
        ExpressionAttributeNames={
            '#name': 'name',
            '#desc': 'description',
            '#config': 'config'
        },
        ExpressionAttributeValues={
            ':n': event['pipeline_data']['name'],
            ':d': event['pipeline_data']['description'],
            ':c': event['pipeline_data']['config']
        }
    )


@patch('src.pipeline_manager.app.boto3.resource')
def test_delete_pipeline(mock_boto_resource):
    print("Mocking boto3.resource")

    # Create a mock DynamoDB Table
    mock_table = MagicMock()
    mock_boto_resource.return_value.Table.return_value = mock_table
    mock_table.delete_item.return_value = {}

    event = {
        "operation": "delete",
        "pipeline_id": "123"
    }

    # Call the lambda function with the mock dynamodb resource
    response = lambda_handler(event, {}, mock_boto_resource.return_value)

    # Check the mock calls
    print("Mock calls:", mock_boto_resource.mock_calls)
    assert response['statusCode'] == 200

    # Ensure the correct method was called
    mock_table.delete_item.assert_called_once_with(Key={'pipeline_id': '123'})
