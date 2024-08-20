# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

import json  # noqa: E402

from db import entries_db  # noqa: E402

def lambda_handler(event, context):
    
    team = str(event['requestContext']['authorizer']['lambda']['team'])

    query = format_queries(event['queryStringParameters']) if 'queryStringParameters' in event.keys() else {}

    cursor = entries_db[team].find(query, {'_id': 0})
    data = []
    for x in cursor:
        data.append(x)
    
    return {
        'statusCode': 200,
        'headers': {
            'content-type':'application/json'
        },
        'body': json.dumps(data)
    }

def format_queries(raw_queries):
    formatted_queries = {}
    for field, val in raw_queries.items():
        if val.isdigit():
            val = int(val)
        formatted_queries[field] = val
    print(formatted_queries)
    return formatted_queries