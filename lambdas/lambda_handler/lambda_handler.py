import json
import boto3

client = boto3.client('lambda', region_name='eu-central-1')
response = client.list_functions()


def invoke_lambda(payload):
    return boto3.client('lambda').invoke(
        FunctionName='FunctionB',
        InvocationType='Event',
        Payload='some_data'.encode('UTF-8')
    )

def lambda_handler(event, context):
    body = json.loads(event['body'])

    signature = event['headers']['x-signature-ed25519']
    return command_handler(body)


def command_handler(body):
  command = body['data']['name']

  if command == 'bleb':
    return {
      'statusCode': 200,
      'body': json.dumps({
        'type': 4,
        'data': {
          'content': 'Hello, World.',
        }
      })
    }
  else:
    return {
      'statusCode': 400,
      'body': json.dumps('unhandled command')
    }
