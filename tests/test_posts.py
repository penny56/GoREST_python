import api.client
import config.consts
import random, json

def test_create_post():

    # POST /users/{id}/posts

    # user the existing user id
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_dict = json.load(f)  

    post_dict = {
        "user_id": str(user_dict['id']),
        "title": "This is the post title",
        "body": "This is the post content, hi there!"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2/users"+"/"+str(user_dict['id'])+"/"+"posts",
                                  headers=config.consts.TOKEN,
                                  json=post_dict,
                                  expected_status=201)
    res_dict = json.loads(res.text)
    
    with open(config.consts.POST_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(res_dict, f, ensure_ascii=False, indent=4)
    
    print("test_create_post passed!")

def test_create_post_failure():

    # create posts with un-exist user (404)
    random_uid_post_data = {
        "user_id": str(random.randint(1000000, 9999999)),
        "title": "This is the post title",
        "json": "This is the post content, hi there!"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2/users"+"/"+str(random.randint(1000000, 9999999))+"/"+"posts",
                                  headers=config.consts.TOKEN,
                                  json=random_uid_post_data,
                                  expected_status=422)
    
    print("test_create_post passed!")

def test_list_posts_by_user():

    # GET /users/{id}/posts
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_dict = json.load(f)
    
    res = api.client.send_request(method="get",
                                  path="/public/v2/users"+"/"+str(user_dict['id'])+"/"+"posts",
                                  headers=config.consts.TOKEN,
                                  expected_status=200)
    
    for text in json.loads(res.text):
        print("Title: ", {text['title']})
    
    print("test_list_posts_by_user passed!")

def test_get_post_details():

    # GET /posts/{id}
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        post_dict = json.load(f)
    
    res = api.client.send_request(method="get",
                                  path="/public/v2"+"/"+"posts"+"/"+str(post_dict['id']),
                                  headers=config.consts.TOKEN,
                                  expected_status=200)
    
    print(f"Post details: {post_dict}")

    print("test_get_post_details passed!")