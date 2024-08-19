import json

from db import entries_db

def lambda_handler(event, context):
    
    team = str(event['requestContext']['authorizer']['lambda']['team'])
    
    cursor = entries_db[team].find({}, {'_id': 0})
    data = []
    for x in cursor:
        data.append(x)
    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
