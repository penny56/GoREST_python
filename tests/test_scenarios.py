import api.client
import json
import pytest

@pytest.mark.skip("not known issue.")
def test_lifecycle(user_dict, post_dict):


    # 1. 创建用户
    create_user_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users",
                                  json=user_dict,
                                  expected_status=201)
    assert create_user_res.status_code == 201
    create_user_res_dict = json.loads(create_user_res.text)

    # 2. 创建用户的帖子
    post_dict = {
        "user_id": create_user_res_dict['id'],
        "title": "This is the post title",
        "body": "This is the post content, hi there!"
    }

    create_post_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{create_user_res_dict['id']}/posts",
                                  json=post_dict,
                                  expected_status=201)
    assert create_post_res.status_code == 201
    create_post_res_dict = json.loads(create_post_res.text)

    # 3. 给帖子加评论
    comment_dict = {
        "post_id": create_post_res_dict["id"],
        "name": "Matt",
        "email": "Matt@noreply.com",
        "body": "This is comment content."
    }

    comment_res = api.client.send_request(method="post",
                                  path=f"/public/v2/posts/{create_post_res_dict["id"]}/comments",
                                  json=comment_dict,
                                  expected_status=201)
    assert comment_res.status_code == 201
    comment_res_dict = json.loads(comment_res.text)



    # 4. 删除用户
    res = api.client.send_request(method="delete",
                                  path=f"/public/v2/users/{create_user_res_dict['id']}",
                                  expected_status=204)
    res.status_code == 204

    print(f"test_delete_user passed! id: {create_user_res_dict['id']}")

    # 5. 验证帖子和评论访问失败
    res = api.client.send_request(method="get",
                                  path=f"/public/v2/posts/{create_post_res_dict['id']}",
                                  expected_status=404)
    assert res.status_code == 404

    # this is the list comments, the response status code should be 200 and response text should be None.
    res = api.client.send_request(method="get",
                                  path=f"/public/v2/posts/{comment_res_dict['id']}/comments",
                                  expected_status=200)
    assert res.status_code == 200


