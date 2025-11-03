import api.client
import config.consts
import random, json

def test_create_post():

    # POST /users/{id}/posts
    
    # creater a user and write to file
    data = {
        "name": "username",
        "email": str(random.randint(10000, 99999))+"@abc.com",
        "gender": "female",
        "status": "active"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2/users",
                                  headers=config.consts.TOKEN,
                                  json=data,
                                  expected_status=201)
    print("Created a user, id:", str(json.loads(res.text)['id']))

    # get current dir
    with open(config.consts.USER_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(res.text)
    

    data = {
        "user_id": json.loads(res.text)['id'],
        "title": "This is the post title",
        "body": "This is the post content, hi there!"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2/users"+"/"+str(json.loads(res.text)['id'])+"/"+"posts",
                                  headers=config.consts.TOKEN,
                                  json=data,
                                  expected_status=201)
    
    with open(config.consts.POST_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(res.text)
    
    print("test_create_post passed!")

def test_create_post_failure():

    # create posts with un-exist user (404)
    data = {
        "user_id": str(random.randint(1000000, 9999999)),
        "title": "This is the post title",
        "json": "This is the post content, hi there!"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2/users"+"/"+str(random.randint(1000000, 9999999))+"/"+"posts",
                                  headers=config.consts.TOKEN,
                                  json=data,
                                  expected_status=422)
    
    print("test_create_post passed!")

def test_list_posts_by_user():

    # GET /users/{id}/posts
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        data_json = json.load(f)
    
    res = api.client.send_request(method="get",
                                  path="/public/v2/users"+"/"+str(data_json['id'])+"/"+"posts",
                                  headers=config.consts.TOKEN,
                                  expected_status=200)
    
    for text in json.loads(res.text):
        print("Title: ", {text['title']})
    
    print("test_list_posts_by_user passed!")

def test_get_post_details():

    # GET /posts/{id}
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        data_json = json.load(f)
    
    res = api.client.send_request(method="get",
                                  path="/public/v2"+"/"+"posts"+"/"+str(data_json['id']),
                                  headers=config.consts.TOKEN,
                                  expected_status=200)
    
    print(f"Post details: {data_json}")

    print("test_get_post_details passed!")