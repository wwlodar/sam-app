import boto3
import botocore
import pytest
# Set "running_locally" flag if you are running the integration test locally
running_locally = True

if running_locally:

    # Create Lambda SDK client to connect to appropriate Lambda endpoint
    lambda_client = boto3.client('lambda',
        region_name="eu-central-1",
        endpoint_url="http://127.0.0.1:3001",
        use_ssl=False,
        verify=False,
        config=botocore.client.Config(
            signature_version=botocore.UNSIGNED,
            read_timeout=1,
            retries={'max_attempts': 0},
        )
    )
else:
    lambda_client = boto3.client('lambda')


# Invoke your Lambda function as you normally usually do. The function will run
# locally if it is configured to do so
response = lambda_client.invoke(FunctionName="HelloWorldFunction")

# Verify the response
assert response == "Hello World"


from proxy import app
import json
import os
import pytest


@pytest.fixture(scope='function')
def mock_context(mocker):
    mock_context = mocker.MagicMock()
    mock_context.aws_request_id = '00000000-0000-1000-0000-000000000000'
    return mock_context


@pytest.fixture(scope='function')
def event(request):
    dir = '{0}/../../events'.format(os.path.dirname(os.path.abspath(__file__)))
    name = request.param
    path = '{0}/{1}'.format(dir, name)
    with open(path) as f:
        event = f.read()
    return event


class TestMethodNotAllowed:

    @pytest.mark.parametrize(
        'event', ['405-get.json'], indirect=True)
    def test_405_get(self, event, mock_context):
        '''Test a GET event.'''

        response = app.lambda_handler(json.loads(event), mock_context)
        body = json.loads(response['body'])

        assert response['statusCode'] == 405
        assert 'exception' in body
        assert 'error_message' in body['exception']
        assert body['exception']['error_message'] == 'Method not allowed.'
        assert body['exception']['error_type'] == 'MethodNotAllowedException'
        assert body['exception']['http_method'] == 'GET'

    # Tests for PUT and DELETE also exist.
