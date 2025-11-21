import api.client
import json

def test_create_comment(comment_dict):

    # POST /posts/{id}/comments

    comment_res = api.client.send_request(method="post",
                                  path=f"/public/v2/posts/{comment_dict["post_id"]}/comments",
                                  json=comment_dict,
                                  expected_status=201)
    assert comment_res.status_code == 201

    comment_res_dict = json.loads(comment_res.text)

    print("\ntest_create_comment passed, comment id is:", comment_res_dict['id'])

def test_create_comment_failure(comment_dict):

    # miss email or json field
    del comment_dict['email']

    comment_res = api.client.send_request(method="post",
                                  path=f"/public/v2/posts/{comment_dict["post_id"]}/comments",
                                  json=comment_dict,
                                  expected_status=422)
    assert comment_res.status_code == 422

    print("test_create_comment_failure passed")

def test_list_comments(comment_dict):

    # GET /posts/{id}/comments

    # 1. create a comment
    comment_res = api.client.send_request(method="post",
                                  path=f"/public/v2/posts/{comment_dict["post_id"]}/comments",
                                  json=comment_dict,
                                  expected_status=201)
    assert comment_res.status_code == 201

    comment_res_dict = json.loads(comment_res.text)

    # 2. list the comment 
    comments_res = api.client.send_request(method="get",
                                  path=f"/public/v2/posts/{comment_res_dict['post_id']}/comments",
                                  expected_status=200)
    assert comments_res.status_code == 200
    comments = json.loads(comments_res.text)
    assert len(comments) == 1

    for comment in comments:
        print(f"comment id: {comment['id']}, post id: {comment['post_id']}, body: {comment['body']}")

    print("test_list_comments passed")
    