from db import keys_db


def lambda_handler(event, context):
    key = event["headers"]["x-sa-auth-key"]
    re = keys_db.find_one({'key': key}, {'_id': 0})
    if not re:
        print('denied')
        return generateDeny('_')
    else:
        print('allowed')
        return generateAllow(re['team'])

def generateAllow(team):
    return {
        'isAuthorized': True,
        'context': {
            'team': team
        }
    }


def generateDeny(team):
    return {
        'isAuthorized': False
    }