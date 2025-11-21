import api.client
import random, json

def test_create_post(post_dict):

    # POST /users/{id}/posts

    post_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{post_dict['user_id']}/posts",
                                  json=post_dict,
                                  expected_status=201)
    assert post_res.status_code == 201
    
    print("test_create_post passed!")

def test_create_post_failure(post_dict):

    # create posts with un-exist user (404)

    # the path include a random user_id and the json is a real post_dict
    failed_post_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{random.randint(1000000, 9999999)}/posts",
                                  json=post_dict,
                                  expected_status=422)
    failed_post_res.status_code == 422
    
    print("test_create_post_failure passed!")

def test_list_posts_by_user(post_dict):

    # GET /users/{id}/posts

    # 1. create a post
    post_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{post_dict['user_id']}/posts",
                                  json=post_dict,
                                  expected_status=201)
    assert post_res.status_code == 201

    # 2. list the posts from the user
    post_res = api.client.send_request(method="get",
                                  path=f"/public/v2/users/{post_dict['user_id']}/posts",
                                  expected_status=200)
    assert post_res.status_code == 200
    
    assert len(json.loads(post_res.text)) == 1
    
    for text in json.loads(post_res.text):
        print("Title: ", {text['title']})
    
    print("test_list_posts_by_user passed!")

def test_get_post_details(post_dict):

    # GET /posts/{id}

    # 1. create a post
    post_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{post_dict['user_id']}/posts",
                                  json=post_dict,
                                  expected_status=201)
    assert post_res.status_code == 201

    post_res_dict = json.loads(post_res.text)
    
    post_details_res = api.client.send_request(method="get",
                                  path=f"/public/v2/posts/{post_res_dict['id']}",
                                  expected_status=200)
    assert post_details_res.status_code == 200
    
    post_details_res_dict = json.loads(post_details_res.text)
    
    print(f"Post details: {post_details_res_dict}")

    print("test_get_post_details passed!")

def test_delete_post(post_dict):

    # DELETE /posts/{id}

    # 1. create a post
    post_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{post_dict['user_id']}/posts",
                                  json=post_dict,
                                  expected_status=201)
    assert post_res.status_code == 201

    create_post_res = json.loads(post_res.text)

    # 2. delete the post
    delete_res = api.client.send_request(method="delete",
                                  path=f"/public/v2/posts/{create_post_res['id']}",
                                  expected_status=204)
    assert delete_res.status_code == 204

