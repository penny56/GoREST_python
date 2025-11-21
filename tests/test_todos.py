import api.client
import json


def test_create_todo(todo_dict, temp_user):

    # POST /users/{id}/todos
    # status = 'pending' or 'completed'

    create_todo_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{temp_user}/todos",
                                  json=todo_dict,
                                  expected_status=201)
    assert create_todo_res.status_code == 201
    create_todo_res_dict = json.loads(create_todo_res.text)

    print("\ntest_create_todo passed, todo id is:", create_todo_res_dict['id'])

def test_create_todo_status(todo_dict, temp_user):

    # status = done, it's an error while create stage
    todo_dict['status'] = 'done'
    
    create_todo_done_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{temp_user}/todos",
                                  json=todo_dict,
                                  expected_status=422)
    assert create_todo_done_res.status_code == 422    

    print("\ntest_create_todo_status passed!")

def test_list_todos(todo_dict, temp_user):

    # GET /users/{id}/todos

    # 1. create a todo
    create_todo_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{temp_user}/todos",
                                  json=todo_dict,
                                  expected_status=201)
    assert create_todo_res.status_code == 201

    # 2. list the todo
    list_todo_res = api.client.send_request(method="get",
                                  path=f"/public/v2/users/{temp_user}/todos",
                                  expected_status=200)
    assert list_todo_res.status_code == 200
    todos = json.loads(list_todo_res.text)
    assert len(todos) == 1

    for todo in todos:
        print(f"todo id: {todo['id']}, json: {todo['title']}")

def test_update_todos(todo_dict, temp_user):
    
    # PATCH /todos/{id}
    # from 'pending' to 'completed'

    # 1. create a todo
    create_todo_res = api.client.send_request(method="post",
                                  path=f"/public/v2/users/{temp_user}/todos",
                                  json=todo_dict,
                                  expected_status=201)
    assert create_todo_res.status_code == 201
    create_todo_res_dict = json.loads(create_todo_res.text)

    # 2. update the status
    todo_dict['status'] = "completed"

    updated_todo_res = api.client.send_request(method="patch",
                                  path=f"/public/v2/todos/{create_todo_res_dict["id"]}",
                                  json=todo_dict,
                                  expected_status=200)
    assert updated_todo_res.status_code == 200
    updated_todo_res_dict = json.loads(updated_todo_res.text)
    assert updated_todo_res_dict['status'] == 'completed'

    print("\ntest_update_todos passed!")
