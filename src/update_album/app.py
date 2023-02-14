import boto3
import os
import json


def lambda_handler(message, context):

    if ('body' not in message or
            message['httpMethod'] != 'PUT'):
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
    album = json.loads(message['body'])

    params = {
        'AlbumId': album['AlbumId'],
        'DateReleased': album['DateReleased']
    }

    response = table.update_item(
        Key=params,
        UpdateExpression="set AlbumName = :n, ArtistId = :a, GenreId = :g",
        ExpressionAttributeValues={
            ':n': album['AlbumName'],
            ':a': album['ArtistId'],
            ':g': album['GenreId']
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({'msg': 'Album updated'})
    }
