import pytest
import random
import json
import api.client
import config.consts

# using in test_users.py

@pytest.fixture
def user_dict():

    return {
        "name": "username",
        "email": str(random.randint(10000, 99999))+"@abc.com",
        "gender": "female",
        "status": "active"
    }

#####

# using in test_posts.py

'''
3 layers of fixture calling:
test_create_post -> post_dict
post_dict -> temp_user
temp_user -> user_dict
'''

@pytest.fixture
def temp_user(user_dict):

    # create an user
    user_res = api.client.send_request(method="post",
                                  path="/public/v2/users",
                                  headers=config.consts.TOKEN,
                                  json=user_dict,
                                  expected_status=201)
    assert user_res.status_code == 201
    
    temp_user_id = json.loads(user_res.text)['id']

    yield temp_user_id

    # delete the user
    delete_res = api.client.send_request(method="delete",
                                  path=f"/public/v2/users/{temp_user_id}",
                                  # path="/public/v2/users"+"/"+str(temp_user_id),
                                  headers=config.consts.TOKEN,
                                  expected_status=204)
    assert delete_res.status_code == 204

@pytest.fixture
def post_dict(temp_user):
    return {
        "user_id": temp_user,       # 这里，temp_user fixture 返回的就是 temp_user_id
        "title": "This is the post title",
        "body": "This is the post content, hi there!"
    }

#####
