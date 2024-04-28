import requests
import unittest
import uuid

base_url = "https://todo.pixegami.io/"

create_data = {
  "content": "https://music.youtube.com/watch?v=qr9rVNfCYgg&feature=shared",
  "user_id": "grmm",
  "task_id": "42",
  "is_done": False
}
update_data = {
    "content": "https://store.steampowered.com/app/413150/Stardew_Valley/",
    "user_id": "grmm",
    "task_id": "42",
    "is_done": False
}


def default_get():
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in GET request @ %s" % base_url)
        print(response.json())
        return response.status_code


def create_task(data):
    response = requests.put(base_url + "create-task", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in PUT request @ %s" % base_url)
        print(response.json())
        return response.status_code


def get_task(task_id):
    response = requests.get(base_url + "get-task/" + task_id)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in GET request @ %s" % base_url)
        print(response.json())
        return response.status_code


def update_task(data):
    response = requests.put(base_url + "update-task", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in PUT request @ %s" % base_url)
        print(response.json())
        return response.status_code


def test_create_get_task():
    create_task_response = create_task(create_data)
    # Get task_id from the response
    task_id = create_task_response["task"]["task_id"]
    get_task_response = get_task(task_id)
    assert get_task_response['is_done'] == create_data['is_done']
    assert get_task_response['content'] == create_data['content']
    assert get_task_response['user_id'] == create_data['user_id']
    print("Create task and get task test passed")


def test_update_get_task():
    create_task_response = create_task(create_data)
    # Get task_id from the response
    task_id = create_task_response["task"]["task_id"]
    # Change the already created dictionary to contain the task_id
    # received from the response
    update_data["task_id"] = task_id
    update_task_response = update_task(update_data)
    get_task_response = get_task(task_id)
    assert get_task_response['is_done'] == update_data['is_done']
    assert get_task_response['content'] == update_data['content']
    assert get_task_response['user_id'] == update_data['user_id']
    print("Update task and get task test passed")


# def test_list_three_tasks():
#     for i in range(3):
#         random_task_id = str(uuid.uuid4())
#     response = default_get()
#     assert len(response) == 3
#     print("List three tasks test passed")

test_create_get_task()
test_update_get_task()

# print(uuid.uuid4())
