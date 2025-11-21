import pytest
import random
import json
import api.client
from datetime import datetime

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
                                  json=user_dict,
                                  expected_status=201)
    assert user_res.status_code == 201
    
    temp_user_id = json.loads(user_res.text)['id']

    yield temp_user_id

    # delete the user
    delete_res = api.client.send_request(method="delete",
                                  path=f"/public/v2/users/{temp_user_id}",
                                  # path="/public/v2/users"+"/"+str(temp_user_id),
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

##### using in test_comments.py
@pytest.fixture
def temp_post(post_dict):

    # create a post
    post_res = api.client.send_request(method="post",
                                  path="/public/v2/users"+"/"+str(post_dict['user_id'])+"/"+"posts",
                                  json=post_dict,
                                  expected_status=201)
    assert post_res.status_code == 201

    temp_post_id = json.loads(post_res.text)['id']

    yield temp_post_id

    # delete the post
    delete_res = api.client.send_request(method="delete",
                                  path=f"/public/v2/posts/{temp_post_id}",
                                  expected_status=204)
    assert delete_res.status_code == 204

@pytest.fixture
def comment_dict(temp_post):
    return {
        "post_id": temp_post,
        "name": "Matt",
        "email": "Matt@noreply.com",
        "body": "This is comment content."
    }

#####

##### using in test_todos.py

@pytest.fixture
def todo_dict():
    return {
        "title": "todo title",
        "due_on": datetime.now().isoformat(),
        "status": "pending"   
    }

#####