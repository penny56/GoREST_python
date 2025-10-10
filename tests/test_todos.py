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
                                  uri="/public/v2"+"/"+"users"+"/"+str(user_json["id"])+"/"+"todos",
                                  headers=config.consts.HEADERS,
                                  body=todo_json,
                                  expected_status=201)

    print("\ntest_create_todo passed, todo id is:", str(json.loads(res.text)['id']))

    # get current dir
    with open(config.consts.TODO_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(res.text)

def test_create_todo_status():

    # status = 'done' (invalid)
    pass

def test_list_todos():

    # GET /users/{id}/todos
    pass

def test_update_todos():
    
    # PATCH /todos/{id}
    # from 'pending' to 'completed'
    pass