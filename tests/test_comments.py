import api.client
import config.consts
import json

def test_create_comment():

    # POST /posts/{id}/comments
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        post_json = json.loads(f.read())

    post_data = {
        "post_id": post_json['id'],
        "name": "Matt",
        "email": "Matt@noreply.com",
        "body": "This is comment content."
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2"+"/"+"posts"+"/"+str(post_data["post_id"])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  json=post_data,
                                  expected_status=201)

    print("\ntest_create_comment passed, comment id is:", str(json.loads(res.text)['id']))

    # get current dir
    with open(config.consts.COMMENT_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(res.text)

def test_create_comment_failure():

    # miss email or json field
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        data_json = json.loads(f.read())

    data = {
        "post_id": data_json['id'],
        "name": "Matt",
        "body": "This is comment content."
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2"+"/"+"posts"+"/"+str(data["post_id"])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  json=data,
                                  expected_status=422)

    print("test_create_comment_failure passed")

def test_list_comments():

    # GET /posts/{id}/comments
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        post_json = json.loads(f.read())

    res = api.client.send_request(method="get",
                                  path="/public/v2"+"/"+"posts"+"/"+str(post_json['id'])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  expected_status=200)
    comments = json.loads(res.text)

    for comment in comments:
        print(f"comment id: {comment['id']}, post id: {comment['post_id']}, body: {comment['body']}")

    print("test_list_comments passed")
    