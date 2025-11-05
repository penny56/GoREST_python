import api.client
import config.consts
import random, json

def test_lifecycle():

    scenario_list = []

    # 1. 创建用户
    user_dict = {
        "name": "username",
        "email": str(random.randint(10000, 99999))+"@abc.com",
        "gender": "female",
        "status": "active"
    }

    user_res = api.client.send_request(method="post",
                                  path="/public/v2/users",
                                  headers=config.consts.TOKEN,
                                  json=user_dict,
                                  expected_status=201)

    user_res_dict = {"user": json.loads(user_res.text)}
    scenario_list.append(user_res_dict)

    # 2. 创建用户的帖子
    post_dict = {
        "user_id": str(user_res_dict['user']['id']),
        "title": "This is the post title",
        "body": "This is the post content, hi there!"
    }

    post_res = api.client.send_request(method="post",
                                  path="/public/v2/users"+"/"+str(user_res_dict['user']['id'])+"/"+"posts",
                                  headers=config.consts.TOKEN,
                                  json=post_dict,
                                  expected_status=201)
    post_res_dict = {"post": json.loads(post_res.text)}

    # append the post info
    if isinstance(scenario_list, list):
        scenario_list.append(post_res_dict)
    else:
        raise TypeError(f"Expected a list, but got {type(scenario_list).__name__}")

    # 3. 给帖子加评论
    comment_dict = {
        "post_id": post_res_dict["post"]["id"],
        "name": "Matt",
        "email": "Matt@noreply.com",
        "body": "This is comment content."
    }

    comment_res = api.client.send_request(method="post",
                                  path="/public/v2"+"/"+"posts"+"/"+str(comment_dict["post_id"])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  json=comment_dict,
                                  expected_status=201)
    comment_res_dict = {"comment": json.loads(comment_res.text)}

    # append the comment info
    if isinstance(scenario_list, list):
        scenario_list.append(comment_res_dict)
    else:
        raise TypeError(f"Expected a list, but got {type(scenario_list).__name__}")

    # 4. 删除用户
    res = api.client.send_request(method="delete",
                                  path="/public/v2/users"+"/"+str(user_res_dict['user']['id']),
                                  headers=config.consts.TOKEN,
                                  expected_status=204)

    print(f"test_delete_user passed! id: {user_res_dict['user']['id']}")

    # 5. 验证帖子和评论访问失败
    res = api.client.send_request(method="get",
                                  path="/public/v2"+"/"+"posts"+"/"+str(post_res_dict['post']['id']),
                                  headers=config.consts.TOKEN,
                                  expected_status=404)

    # this is the list comments, the response status code should be 200 and response text should be None.
    res = api.client.send_request(method="get",
                                  path="/public/v2"+"/"+"posts"+"/"+str(post_res_dict['post']['id'])+"/"+"comments",
                                  headers=config.consts.TOKEN,
                                  expected_status=200)

    # write to user.json
    with open(config.consts.SCENARIOS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(scenario_list, f, ensure_ascii=False, indent=4)

def test_parallel():

    # 在短时间内创建多个用户并验证分页（GET /users?page=2）。
    pass

def test_verify_data():

    # 检查每个接口返回的字段结构（JSON schema validation）。
    pass