# import os
# import sys
# from pprint import pprint  # noqa: F401

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# comment out above when uploading, only necessary for local development

import json  # noqa: E402

from db import entries_db, alliances_db  # noqa: E402

def lambda_handler(event, context):
    
    team = str(event['requestContext']['authorizer']['lambda']['team'])

    query = format_queries(event['queryStringParameters']) if 'queryStringParameters' in event.keys() else {}

    if 'alliance' in query.keys() and query['alliance'] in ('true', 'True'):
        teams_set = set()
        for alliance in alliances_db.find({'teams': int(team)}, {'_id': 0}):
            for t in alliance['teams']:
                teams_set.add(str(t))
        teams = list(teams_set)
        query.pop('alliance')
    else:
        teams = [team]

    data = []
    for t in teams:
        data.extend([x for x in entries_db[t].find(query, {'_id': 0})])
    
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