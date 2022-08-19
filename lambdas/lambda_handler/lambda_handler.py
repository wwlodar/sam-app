import json

def lambda_handler(event, context):
    body = json.loads(event['body'])

    signature = event['headers']['x-signature-ed25519']
    timestamp = event['headers']['x-signature-timestamp']
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