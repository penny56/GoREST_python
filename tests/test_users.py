import api.client
import config.settings
import random, json, os

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
    print("\ntest_create_user passed, user id is:", str(json.loads(res.text)['id']))

    # get current dir
    with open(config.settings.FILE_PATH, "w", encoding="utf-8") as f:
        f.write(res.text)

def test_create_user_failure():

    # duplicated email
    with open(config.settings.FILE_PATH, "r", encoding="utf-8") as f:
        email = json.loads(f.read())['email']
    
    data = {
        "name": "username",
        "email": email,
        "gender": "female",
        "status": "active"
    }
    
    res = api.client.send_request(method="post",
                                  uri="/public/v2/users",
                                  headers=config.settings.HEADERS,
                                  body=data,
                                  expected_status=422)
    
    print("test_create_user_failure passed!")

def test_search_user():

    # GET /users/{id}
    with open(config.settings.FILE_PATH, "r", encoding="utf-8") as f:
        data_json = json.load(f) 
    
    res = api.client.send_request(method="get",
                                  uri="/public/v2/users"+"/"+str(data_json['id']),
                                  headers=config.settings.HEADERS,
                                  expected_status=200)

    data_res = json.loads(res.text)

    assert data_json['name'] == data_res['name'] and data_json['email'] == data_res['email'] and data_json['gender'] == data_res['gender'] and data_json['status'] == data_res['status'], (
        f"{res.text}"
    )

    print("test_search_user passed!")


def test_search_user_failure():

    # un-existing uid
    res = api.client.send_request(method="get",
                                  uri="/public/v2/users"+"/"+str(random.randint(10000, 99999)),
                                  headers=config.settings.HEADERS,
                                  expected_status=404)
    
    print("test_search_user_failure passed!")

def test_update_user():

    # PUT /users/{id}
    # 1. check the gender
    with open(config.settings.FILE_PATH, "r", encoding="utf-8") as f:
        data_json = json.load(f) 

    old_gender = data_json['gender']

    # 2. update
    if old_gender == 'male':
        new_gender = 'female'
    else:
        new_gender = 'male'

    data = { "gender": new_gender }

    res = api.client.send_request(method="put",
                                  uri="/public/v2/users"+"/"+str(data_json['id']),
                                  headers=config.settings.HEADERS,
                                  body=data,
                                  expected_status=200)    

    # 3. confirm the change
    assert json.loads(res.text)['gender'] == new_gender, (
        f"{res.text}"
    )

    print('test_update_user passed!')

def test_update_user_failure():

    # invalid gender
    with open(config.settings.FILE_PATH, "r", encoding="utf-8") as f:
        data_json = json.load(f) 

    data = { "gender": 'invalid' }

    res = api.client.send_request(method="put",
                                  uri="/public/v2/users"+"/"+str(data_json['id']),
                                  headers=config.settings.HEADERS,
                                  body=data,
                                  expected_status=422)    

    print('test_update_user_failure passed!')

def test_delete_user():

    # DELETE /users/{id}
    pass

def test_delete_user_failure():

    # delete deleted user (404)
    pass