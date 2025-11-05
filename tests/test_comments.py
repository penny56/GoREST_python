import api.client
import config.consts
import json

def test_create_comment():

    # POST /posts/{id}/comments
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        post_dict = json.load(f)

    comment_dict = {
        "post_id": post_dict['id'],
        "name": "Matt",
        "email": "Matt@noreply.com",
        "body": "This is comment content."
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2"+"/"+"posts"+"/"+str(comment_dict["post_id"])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  json=comment_dict,
                                  expected_status=201)
    res_dict = json.loads(res.text)

    print("\ntest_create_comment passed, comment id is:", res_dict['id'])

    # get current dir
    with open(config.consts.COMMENT_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(res_dict, f, ensure_ascii=False, indent=4)

def test_create_comment_failure():

    # miss email or json field
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        post_dict = json.load(f)

    no_email_comment_dict = {
        "post_id": post_dict['id'],
        "name": "Matt",
        "body": "This is comment content."
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2"+"/"+"posts"+"/"+str(post_dict["id"])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  json=no_email_comment_dict,
                                  expected_status=422)

    print("test_create_comment_failure passed")

def test_list_comments():

    # GET /posts/{id}/comments
    with open(config.consts.POST_FILE_PATH, "r", encoding="utf-8") as f:
        post_dict = json.load(f)

    res = api.client.send_request(method="get",
                                  path="/public/v2"+"/"+"posts"+"/"+str(post_dict['id'])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  expected_status=200)
    comments = json.loads(res.text)

    for comment in comments:
        print(f"comment id: {comment['id']}, post id: {comment['post_id']}, body: {comment['body']}")

    print("test_list_comments passed")
    