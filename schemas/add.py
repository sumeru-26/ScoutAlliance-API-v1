# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

import json

from db import data_schema_db  # noqa: E402

def lambda_handler(event, context):

    team = event['requestContext']['authorizer']['lambda']['team']  
    
    try:
        schema = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'No schema provided in body'
        }
    
    if 'event' not in schema.keys():
        return {
            'statusCode': 400,
            'body': 'Missing event field in schema'
        }

    if data_schema_db.find_one({'team': team, 'event': schema['event']}) is not None:
        return {
            'statusCode': 400,
            'body': 'You already have a schema for this event; try using /update instead'
        }
    
    schema['team'] = team
    
    data_schema_db.insert_one(schema)

    return {
        'statusCode': 200,
    }