from unittest.mock import patch, MagicMock
from src.notifications.app import lambda_handler

@patch('src.notifications.app.boto3.client')
def test_send_notification(mock_boto_client):
    print("Mocking boto3.client")

    # Create a mock SNS client
    mock_sns = MagicMock()
    mock_sns.publish.return_value = {"MessageId": "msg-1234"}

    # Assign the mock client to boto3.client return value
    mock_boto_client.return_value = mock_sns

    event = {
        "topic_arn": "arn:aws:sns:us-east-1:123456789012:MyTopic",
        "message": "Deployment successful"
    }

    # Call the lambda function with the mocked client
    response = lambda_handler(event, None, sns=mock_sns)

    # Assertions
    assert response['statusCode'] == 200
    mock_sns.publish.assert_called_once_with(
        TopicArn="arn:aws:sns:us-east-1:123456789012:MyTopic",
        Message="Deployment successful"
    )
