import api.client
import config.settings
import random, json

def test_create_user():
    data = {
        "name": "username",
        "email": str(random.randint(10000, 99999))+"@abc.com",
        "gender": "female",
        "status": "active"
    }

    res = api.client.send_request(method="post",
                                  uri="/public/v2/users",
                                  headers=config.settings.HEADERS,
                                  body=data,
                                  expected_status=201)
    print("test_create_user passed, user id is:", str(json.loads(res.text)['id']))