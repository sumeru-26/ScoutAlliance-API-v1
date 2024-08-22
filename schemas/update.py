# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

import json

from pymongo import ReturnDocument

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

    schema['team'] = team
    
    if data_schema_db.find_one_and_replace({'team': team, 'event': schema['event']}, schema, return_document=ReturnDocument.BEFORE) is None:
        return {
            'statusCode': 400,
            'body': 'You don\'t have a schema for this event; trying using /add instead'
        }

    return {
        'statusCode': 200,
    }