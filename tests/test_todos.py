import api.client
import config.consts
import json
from datetime import datetime


def test_create_todo():

    # POST /users/{id}/todos
    # status = 'pending' or 'completed'
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_json = json.loads(f.read())

    todo_json = {
        "title": "todo title",
        "due_on": datetime.now().isoformat(),
        "status": "pending"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2"+"/"+"users"+"/"+str(user_json["id"])+"/"+"todos",
                                  headers=config.consts.TOKEN,
                                  json=todo_json,
                                  expected_status=201)

    print("\ntest_create_todo passed, todo id is:", str(json.loads(res.text)['id']))

    # get current dir
    with open(config.consts.TODO_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(res.text)

def test_create_todo_status():

    # status = 'done' (invalid)
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_json = json.loads(f.read())

    todo_json_done = {
        "title": "todo title",
        "due_on": datetime.now().isoformat(),
        "status": "done"
    }

    res = api.client.send_request(method="post",
                                  path="/public/v2"+"/"+"users"+"/"+str(user_json["id"])+"/"+"todos",
                                  headers=config.consts.TOKEN,
                                  json=todo_json_done,
                                  expected_status=422)

    print("\ntest_create_todo_status passed!")

def test_list_todos():

    # GET /users/{id}/todos
    with open(config.consts.USER_FILE_PATH, "r", encoding="utf-8") as f:
        user_json = json.loads(f.read())

    res = api.client.send_request(method="get",
                                  path="/public/v2"+"/"+"users"+"/"+str(user_json["id"])+"/"+"todos",
                                  headers=config.consts.TOKEN,
                                  expected_status=200)

    todos = json.loads(res.text)

    for todo in todos:
        print(f"todo id: {todo['id']}, json: {todo['title']}")

def test_update_todos():
    
    # PATCH /todos/{id}
    # from 'pending' to 'completed'
    with open(config.consts.TODO_FILE_PATH, "r", encoding="utf-8") as f:
        todo_json = json.loads(f.read())

    todo_data = {
        "status": "completed"
    }

    res = api.client.send_request(method="patch",
                                  path="/public/v2"+"/"+"todos"+"/"+str(todo_json["id"]),
                                  headers=config.consts.TOKEN,
                                  json=todo_data,
                                  expected_status=200)

    print("\ntest_update_todos passed!")
