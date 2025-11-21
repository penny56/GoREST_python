import api.client
import random, json

def test_create_user(user_dict):

    # POST /users
    res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=201)
    assert res.status_code == 201
    
    res_dict = json.loads(res.text)
    
    print("\ntest_create_user passed, user id is: ", res_dict['id'])

def test_create_user_failure(user_dict):

    # failure reason: duplicated email

    # create a user
    res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=201)
    assert res.status_code == 201

    # create another user, re-use the email (without update the user_dict)
    res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=422)
    assert res.status_code == 422

    print("test_create_user_failure passed!")

def test_search_user(user_dict):

    # GET /users/{id}

    # create a user
    create_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=201)
    assert create_res.status_code == 201

    create_res_dict = json.loads(create_res.text)

    search_res = api.client.send_request(method="get",
                                  path=f"/public/v2/users/{create_res_dict['id']}",
                                  expected_status=200)
    assert search_res.status_code == 200

    search_res_dict = json.loads(search_res.text)

    assert create_res_dict['name'] == search_res_dict['name'] and create_res_dict['email'] == search_res_dict['email'] and create_res_dict['gender'] == search_res_dict['gender'] and create_res_dict['status'] == search_res_dict['status'], (
        f"{search_res.text}"
    )

    print("test_search_user passed!")

def test_search_user_failure():

    # failure reason: search random un-existing uid
    res = api.client.send_request(method="get",
                                  path=f"/public/v2/users/{random.randint(10000, 99999)}",
                                  expected_status=404)
    
    print("test_search_user_failure passed!")

def test_update_user(user_dict):

    # PUT /users/{id}

    # create a user
    create_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=201)
    assert create_res.status_code == 201

    create_res_dict = json.loads(create_res.text)

    # check the gender
    old_gender = create_res_dict['gender']

    # update
    if old_gender == 'male':
        new_gender = 'female'
    else:
        new_gender = 'male'

    gender_data = { "gender": new_gender }

    update_res = api.client.send_request(method="put",
                                  path=f"/public/v2/users/{create_res_dict['id']}",
                                  json=gender_data,
                                  expected_status=200) 
    assert update_res.status_code == 200   

    # 3. confirm the change
    assert json.loads(update_res.text)['gender'] == new_gender, (
        f"{update_res.text}"
    )

    print('test_update_user passed!')

def test_update_user_failure(user_dict):

    # invalid gender

    # create a user
    create_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=201)
    assert create_res.status_code == 201

    create_res_dict = json.loads(create_res.text)

    invalid_data = { "gender": 'invalid' }

    update_res = api.client.send_request(method="put",
                                  path=f"/public/v2/users/{create_res_dict['id']}",
                                  json=invalid_data,
                                  expected_status=422)
    assert update_res.status_code == 422

    print('test_update_user_failure passed!')

def test_delete_user(user_dict):

    # DELETE /users/{id}

    # 1. create a user
    create_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=201)
    assert create_res.status_code == 201

    create_res_dict = json.loads(create_res.text)

    delete_res = api.client.send_request(method="delete",
                                  path=f"/public/v2/users/{create_res_dict['id']}",
                                  expected_status=204)
    assert delete_res.status_code == 204

    print(f"test_delete_user passed! id: {create_res_dict['id']}")

def test_delete_user_failure():

    # failure reason: delete a non-exist user (404)

    delete_res = api.client.send_request(method="delete",
                                  path=f"/public/v2/{random.randint(10000, 99999)}",
                                  expected_status=404)
    assert delete_res.status_code == 404

    print(f"test_delete_user_failure passed!")
