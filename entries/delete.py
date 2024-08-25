# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

from db import entries_db  # noqa: E402

def lambda_handler(event, context):
    
    team = str(event['requestContext']['authorizer']['lambda']['team'])

    query = format_queries(event['queryStringParameters']) if 'queryStringParameters' in event.keys() else {}

    entries_db[team].delete_many(query)
    
    return {
        'statusCode': 200,
    }

def format_queries(raw_queries):
    formatted_queries = {}
    for field, val in raw_queries.items():
        if val.isdigit():
            val = int(val)
        formatted_queries[field] = val
    return formatted_queries