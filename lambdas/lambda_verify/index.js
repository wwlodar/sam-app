const nacl = require('tweetnacl');

exports.handler = async (event) => {
  // Checking signature (requirement 1.)
  // Your public key can be found on your application in the Developer Portal
  const PUBLIC_KEY = process.env.PUBLIC_KEY;
  const signature = event.headers['x-signature-ed25519']
  const timestamp = event.headers['x-signature-timestamp'];
  const strBody = event.body; // should be string, for successful sign

  const isVerified = nacl.sign.detached.verify(
    Buffer.from(timestamp + strBody),
    Buffer.from(signature, 'hex'),
    Buffer.from(PUBLIC_KEY, 'hex')
  );

  if (!isVerified) {
    return {
      statusCode: 401,
      body: JSON.stringify('invalid request signature'),
    };
  }


  // Replying to ping (requirement 2.)
  const body = JSON.parse(strBody)
  if (body.type == 1) {
    return {
      statusCode: 200,
      body: JSON.stringify({ "type": 1 }),
    }
  }


  const stackName = process.env.STACK_NAME.split('-').slice(0, 3).join('-')
  const funcs = await lambda.listFunctions().promise();
  const commandHandlerLambda = funcs.Functions.find(
    l => (l.FunctionName.includes('HandlerFunction') && l.FunctionName.includes(stackName))
  )

  if (commandHandlerLambda) {
    var params = {
      FunctionName: commandHandlerLambda.FunctionName,
      InvocationType: 'Event',
      LogType: 'Tail',
      Payload: strBody
    };

    params.Payload = JSON.stringify(params.Payload);
    const lambdaResult = await lambda.invoke(params).promise();

    return {
      statusCode: 200,
      body: JSON.stringify({ "type": 5 })
    }
  } else {
    return {
      statusCode: 404  // If no handler implemented for Discord's request
    }
  }
};
