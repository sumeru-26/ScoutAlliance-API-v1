# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

import json

from db import entries_db, data_schema_db  # noqa: E402

METADATA_SCHEMA = {
    'event': 'str',
    'match': 'int',
    'bot': 'int'
}

def lambda_handler(event, context):

    team = event['requestContext']['authorizer']['lambda']['team']

    try:
        entries = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'headers': {
                'content-type':'application/json'
            },
            'body': '{ \"message\": \"No entries provided in body\" }'
        }
    
    if isinstance(entries, dict):
        entries = [entries]

    try:
        entryEvent = entries[0]['metadata']['event']
    except KeyError:
        return {
                'statusCode': 400,
                'headers': {
                    'content-type':'application/json'
                },
                'body': '{ \"message\": \"Badly formatted entry; missing event\" }'
            }
    
    data_schema = data_schema_db.find_one({'team': team, 'event': entryEvent}, {'_id': 0, 'team': 0, 'event': 0})

    for entry in entries:
        if not set(['metadata', 'data']) == entry.keys():
            return {
                'statusCode': 400,
                'headers': {
                    'content-type':'application/json'
                },
                'body': '{ \"message\": \"Badly formatted entry; missing metadata and data fields or extra top-level fields\" }'

            }
        if not (verify_entry(entry['metadata'], METADATA_SCHEMA) and verify_entry(entry['data'], data_schema)):
            return {
                'statusCode': 400,
                'headers': {
                    'content-type':'application/json'
                },
                'body': '{ \"message\": \"Badly formatted entry; does not follow schemas\" }'
            }
        entry['metadata']['team'] = team
    
    entries_db[str(team)].insert_many(entries)

    return {
        'statusCode': 200,
    }

def verify_entry(entry, schema):
    for field, type in schema.items():
        if field not in entry.keys():
            return False
        if isinstance(type, dict):
            checked = verify_entry(entry[field], schema[field])
        else:
            checked = verify_type(entry[field], type)
        if not checked:
            return False
    return True

def verify_type(val, type):
    if type == 'int':
        return isinstance(val, int)
    elif type == 'str':
        return isinstance(val, str)