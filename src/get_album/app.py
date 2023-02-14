import boto3
import os
import json
from boto3.dynamodb.conditions import Key


def lambda_handler(message, context):

    if ('pathParameters' not in message or
            message['httpMethod'] != 'GET'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'Albums')
 
    albums_table = boto3.resource(
            'dynamodb'
        )

    table = albums_table.Table(table_name)
    date = message['pathParameters']['DateReleased']

    response = table.query(
        KeyConditionExpression=Key('DateReleased').eq(date)
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
