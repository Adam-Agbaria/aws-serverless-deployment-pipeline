from unittest.mock import patch, MagicMock
from src.build_function.app import lambda_handler

def test_lambda_handler():
    print("Mocking boto3.client")

    # Create a mock CodeBuild client
    mock_codebuild = MagicMock()
    mock_codebuild.start_build.return_value = {"buildId": "build-1234"}

    with patch('src.build_function.app.boto3.client', return_value=mock_codebuild) as mock_boto_client:
        event = {
            "project_name": "MyBuildProject"
        }

        # Call the lambda function
        response = lambda_handler(event, {})

        # Check the mock calls
        print("Mock calls:", mock_boto_client.mock_calls)

        assert response['statusCode'] == 200
        mock_boto_client.return_value.start_build.assert_called_once_with(projectName="MyBuildProject")
