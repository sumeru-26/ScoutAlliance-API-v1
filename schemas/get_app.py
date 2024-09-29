# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

import json  # noqa: E402

from db import app_schema_db  # noqa: E402

def lambda_handler(event, context):
    
    team = event['requestContext']['authorizer']['lambda']['team']
    
    try:
        eventQuery = event['queryStringParameters']['event']
    except KeyError:
        return {
            'statusCode': 400,
            'headers': {
                'content-type':'application/json'
            },
            'body': '{ \"message\": \"Missing event parameter\" }'
        }
    
    try:
        typeQuery = event['queryStringParameters']['type']
    except KeyError:
        return {
            'statusCode': 400,
            'headers': {
                'content-type':'application/json'
            },
            'body': '{ \"message\": \"Missing type parameter\" }'
        }
    
    data = app_schema_db.find_one({'team': team, 'event': eventQuery, 'type': typeQuery}, {'_id': 0})

    return {
        'statusCode': 200,
        'headers': {
            'content-type':'application/json'
        },
        'body': json.dumps(data)
    }