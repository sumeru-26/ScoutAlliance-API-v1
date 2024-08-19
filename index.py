def lambda_handler(event, context):
    
    print(event)
    
    print(event['requestContext']['authorizer']['lambda']['team'])

    res = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "*/*"
        },
        "body": "Hello!"
    }

    return res