import api.client
import config.settings
import random, json

def test_create_user():

    # POST /users
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

def test_create_user_failure():

    # duplicated email
    pass

def test_search_user():

    # GET /users/{id}
    pass

def test_search_user_failure():

    # un-existing uid
    pass

def test_update_user():

    # PUT /users/{id}
    pass

def test_update_user_failure():

    # invalid gender (famale)
    pass

def test_delete_user():

    # DELETE /users/{id}
    pass

def test_delete_user_failure():

    # delete deleted user (404)
    pass