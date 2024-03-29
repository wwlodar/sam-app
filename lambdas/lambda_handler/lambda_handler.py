import json
import boto3

client = boto3.client('lambda', region_name='eu-central-1')
response = client.list_functions()


def invoke_lambda(name, payload):
    return boto3.client('lambda').invoke(
        FunctionName=name,
        InvocationType='Event',
        Payload=payload,
    )


def lambda_handler(event):
    print(event)
    body = json.loads(event['body'])
    print(body)

    command = body['data']['name']
    if command == 'response':
        invoke_lambda('ResponseFunction', body)
    if command == 'search':
        invoke_lambda('SearchFunction', body)
