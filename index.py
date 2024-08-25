def lambda_handler(event, context):
    
    print(event)
    
    team = str(event['requestContext']['authorizer']['lambda']['team'])

    res = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        
        "body": f"{{ \"message\": \"Hello team {team}! This is the ScoutAlliance API\" }}"
    }

    return res