import pytest


def capital_case(x):
    return x.capitalize()


def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'


def test_raises_exception_on_non_string_arguments():
    with pytest.raises(TypeError):
        capital_case(9)


# from lambdas import lambda_verify
# import json
# import os
# import pytest
#
#
# @pytest.fixture(scope='function')
# def mock_context(mocker):
#     mock_context = mocker.MagicMock()
#     mock_context.aws_request_id = '00000000-0000-1000-0000-000000000000'
#     return mock_context
#
#
# @pytest.fixture(scope='function')
# def event(request):
#     dir = '{0}/../../events'.format(os.path.dirname(os.path.abspath(__file__)))
#     name = request.param
#     path = '{0}/{1}'.format(dir, name)
#     with open(path) as f:
#         event = f.read()
#     return event
#
#
# class TestMethodNotAllowed:
#
#     @pytest.mark.parametrize('event', ['405-get.json'], indirect=True)
#     def test_405_get(self, event, mock_context):
#         '''Test a GET event.'''
#
#         response = lambda_verify.lambda_handler(json.loads(event), mock_context)
#         body = json.loads(response['body'])
#
#         assert response['statusCode'] == 405
#         assert 'exception' in body
#         assert 'error_message' in body['exception']
#         assert body['exception']['error_message'] == 'Method not allowed.'
#         assert body['exception']['error_type'] == 'MethodNotAllowedException'
#         assert body['exception']['http_method'] == 'GET'
#
#     # Tests for PUT and DELETE also exist.
