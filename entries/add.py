# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

from time import time
import json

from db import entries_db, data_schema_db  # noqa: E402

METADATA_SCHEMA = {
    'event': 'str',
    'type': 'str',
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
                'body': '{ \"message\": \"Badly formatted entry; missing \'event\' field in metadata\" }'
            }
    
    try:
        entryType = entries[0]['metadata']['type']
    except KeyError:
        return {
                'statusCode': 400,
                'headers': {
                    'content-type':'application/json'
                },
                'body': '{ \"message\": \"Badly formatted entry; missing \'type\' field in metadata\" }'
            }
    
    data_schema = data_schema_db.find_one({'team': team, 'event': entryEvent, 'type': entryType}, {'_id': 0, 'team': 0, 'event': 0, 'type': 0})

    if data_schema is None:
        return {
            'statusCode': 400,
            'headers': {
                'content-type':'application/json'
            },
            'body': '{ \"message\": \"Schema not found; is your event and type correct?\" }'
        }

    for entry in entries:
        if not set(['metadata', 'data']) == entry.keys():
            return {
                'statusCode': 400,
                'headers': {
                    'content-type':'application/json'
                },
                'body': '{ \"message\": \"Badly formatted entry; missing metadata and data fields or has extra top-level fields\" }'

            }
        # if not (verify_entry(entry['metadata'], METADATA_SCHEMA) and verify_entry(entry['data'], data_schema)):
        #     return {
        #         'statusCode': 400,
        #         'headers': {
        #             'content-type':'application/json'
        #         },
        #         'body': '{ \"message\": \"Badly formatted entry; does not follow schema\" }'
        #     }
        if not verify_entry(entry['metadata'], METADATA_SCHEMA):
            return {
                'statusCode': 400,
                'headers': {
                    'content-type':'application/json'
                },
                'body': '{ \"message\": \"Badly formatted entry; does not follow metadata schema\" }'
            }
        if not verify_entry(entry['data'], data_schema):
            return {
                'statusCode': 400,
                'headers': {
                    'content-type':'application/json'
                },
                'body': f'{{ \"message\": \"Badly formatted entry; does not follow data schema for \'{entryEvent}\' event and \'{entryType}\' type\" }}'
            }
        entry['metadata']['team'] = team
        entry['metadata']['timestamp'] = int(time()*1000)
    
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
    elif type == 'bool':
        return isinstance(val, bool)