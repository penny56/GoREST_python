import api.client
import config.settings
import random, json

def test_lifecycle():
    # 创建用户 → 创建用户的帖子 → 给帖子加评论 → 删除用户 → 验证帖子和评论访问失败。
    pass

def test_parallel():

    # 在短时间内创建多个用户并验证分页（GET /users?page=2）。
    pass

def test_verify_data():

    # 检查每个接口返回的字段结构（JSON schema validation）。
    pass