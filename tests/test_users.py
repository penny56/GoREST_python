import api.client
import config.consts
import random, json

# for the skip test cases
import pytest

def test_create_user():

    # POST /users
    user_dict = {
        "name": "username",
        "email": str(random.randint(10000, 99999))+"@abc.com",
        "gender": "female",
        "status": "active"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2/users",
                                  headers=config.consts.TOKEN,
                                  json=user_dict,
                                  expected_status=201)
    res_dict = json.loads(res.text)
    
    print("\ntest_create_user passed, user id is: ", res_dict['id'])

    # write to user.json
    with open(config.consts.USER_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(res_dict, f, ensure_ascii=False, indent=4)

def test_create_user_failure():

    # duplicated email
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        email = json.loads(f.read())['email']
    
    user_dup_email_dict = {
        "name": "username",
        "email": email,
        "gender": "female",
        "status": "active"
    }
    
    res = api.client.send_request(method="post",
                                  path="/public/v2/users",
                                  headers=config.consts.TOKEN,
                                  json=user_dup_email_dict,
                                  expected_status=422)
    
    print("test_create_user_failure passed!")

def test_search_user():

    # GET /users/{id}
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_dict = json.load(f)
    
    res = api.client.send_request(method="get",
                                  path="/public/v2/users"+"/"+str(user_dict['id']),
                                  headers=config.consts.TOKEN,
                                  expected_status=200)

    data_res = json.loads(res.text)

    assert user_dict['name'] == data_res['name'] and user_dict['email'] == data_res['email'] and user_dict['gender'] == data_res['gender'] and user_dict['status'] == data_res['status'], (
        f"{res.text}"
    )

    print("test_search_user passed!")


def test_search_user_failure():

    # un-existing uid
    res = api.client.send_request(method="get",
                                  path="/public/v2/users"+"/"+str(random.randint(10000, 99999)),
                                  headers=config.consts.TOKEN,
                                  expected_status=404)
    
    print("test_search_user_failure passed!")

def test_update_user():

    # PUT /users/{id}
    # 1. check the gender
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_dict = json.load(f) 

    old_gender = user_dict['gender']

    # 2. update
    if old_gender == 'male':
        new_gender = 'female'
    else:
        new_gender = 'male'

    gender_data = { "gender": new_gender }

    res = api.client.send_request(method="put",
                                  path="/public/v2/users"+"/"+str(user_dict['id']),
                                  headers=config.consts.TOKEN,
                                  json=gender_data,
                                  expected_status=200)    

    # 3. confirm the change
    assert json.loads(res.text)['gender'] == new_gender, (
        f"{res.text}"
    )

    print('test_update_user passed!')

def test_update_user_failure():

    # invalid gender
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_dict = json.load(f) 

    invalid_data = { "gender": 'invalid' }

    res = api.client.send_request(method="put",
                                  path="/public/v2/users"+"/"+str(user_dict['id']),
                                  headers=config.consts.TOKEN,
                                  json=invalid_data,
                                  expected_status=422)    

    print('test_update_user_failure passed!')

@pytest.mark.skip(reason="user should be used later, skip the deletion.")
def test_delete_user():

    # DELETE /users/{id}
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_dict = json.load(f) 

    res = api.client.send_request(method="delete",
                                  path="/public/v2/users"+"/"+str(user_dict['id']),
                                  headers=config.consts.TOKEN,
                                  expected_status=204)

    print(f"test_delete_user passed! id: {user_dict['id']}")

@pytest.mark.skip(reason="user should be used later, skip the deletion.")
def test_delete_user_failure():

    # delete deleted user (404)
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_dict = json.load(f) 

    res = api.client.send_request(method="delete",
                                  path="/public/v2"+"/"+str(user_dict['id']),
                                  headers=config.consts.TOKEN,
                                  expected_status=404)

    print(f"test_delete_user_failure passed!")
