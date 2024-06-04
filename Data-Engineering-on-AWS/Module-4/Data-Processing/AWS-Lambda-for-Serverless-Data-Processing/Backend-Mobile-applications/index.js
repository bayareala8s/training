const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
  const body = JSON.parse(event.body);

  const params = {
    TableName: process.env.DYNAMODB_TABLE,
    Item: {
      id: body.id,
      data: body.data
    }
  };

  try {
    await dynamodb.put(params).promise();
    const response = {
      statusCode: 200,
      body: JSON.stringify('Data written to DynamoDB')
    };
    return response;
  } catch (error) {
    const response = {
      statusCode: 500,
      body: JSON.stringify('Error writing to DynamoDB')
    };
    return response;
  }
};
