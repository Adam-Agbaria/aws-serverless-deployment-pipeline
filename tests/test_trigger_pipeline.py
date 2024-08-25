from unittest.mock import patch, MagicMock
from src.trigger_pipeline.app import lambda_handler

@patch('src.trigger_pipeline.app.boto3.client')
def test_trigger_pipeline(mock_boto_client):
    print("Mocking boto3.client")

    # Create a mock CodePipeline client
    mock_codepipeline = MagicMock()
    mock_codepipeline.start_pipeline_execution.return_value = {"pipelineExecutionId": "pipeline-1234"}

    # Assign the mock client to boto3.client return value
    mock_boto_client.return_value = mock_codepipeline

    event = {
        "pipeline_name": "MyPipeline"
    }

    # Call the lambda function with the mocked client
    response = lambda_handler(event, None, codepipeline=mock_codepipeline)

    # Assertions
    assert response['statusCode'] == 200
    mock_codepipeline.start_pipeline_execution.assert_called_once_with(
        name="MyPipeline"
    )
