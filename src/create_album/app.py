import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(message, context):

    if ('body' not in message or
            message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'order')
    print(table_name)


    albums_table = boto3.resource(
            'dynamodb'
        )

    table = albums_table.Table(table_name)
    album = json.loads(message['body'])

    params = {
        "AlbumProporty":{
            'AlbumId': album['AlbumId'],
            'AlbumName': album['AlbumName']
        },
        "AlbumData":{

            'DateReleased': album['DateReleased'],
            'ArtistId': album['ArtistId'],
            'GenreId': album['GenreId']
        }
        
    }
    

    response = table.put_item(
        TableName=table_name,
        Item=params
    )
    print(response)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'msg': 'order created'})
    }
