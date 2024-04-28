import requests
import unittest
import uuid
import random
import json

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


def get_task_supressed(task_id):
    response = requests.get(base_url + "get-task/" + task_id)
    return response.status_code


def update_task(data):
    response = requests.put(base_url + "update-task", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in PUT request @ %s" % base_url)
        print(response.json())
        return response.status_code


def list_tasks(user_id):
    response = requests.get(base_url + "list-tasks/" + user_id)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in GET request @ %s" % base_url)
        print(response.json())
        return response.status_code


def write_list_tasks_json():
    with open("list_tasks_response.json", "w") as f:
        json.dump(list_tasks("grmm"), f, indent=4)


def delete_task(task_id):
    response = requests.delete(base_url + "delete-task/" + task_id)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error in DELETE request @ %s" % base_url)
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
    print("[1] Create task and get task test passed")


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
    print("[2] Update task and get task test passed")


def test_list_three_tasks():
    # Generate a random user_id
    user_id = str(uuid.uuid4())
    # Keep track of ids of the created tasks
    task_ids = []
    for i in range(3):
        random_data = {
            "content": ''.join(random.choices("abcde", k=10)),
            "user_id": user_id,
            "task_id": "42",
            "is_done": False
        }
        create_task_response = create_task(random_data)
        task_ids.append(create_task_response["task"]["task_id"])

    list_tasks_response = list_tasks(user_id)
    # Check length of the list of tasks
    assert len(list_tasks_response["tasks"]) == 3
    # Check if the task_ids of the created tasks are in the response
    for task in list_tasks_response["tasks"]:
        assert task["task_id"] in task_ids
    print("[3] List three tasks test passed")


def test_delete_task():
    create_task_response = create_task(create_data)
    # Get task_id from the response
    task_id = create_task_response["task"]["task_id"]
    delete_task_response = delete_task(task_id)
    assert delete_task_response["deleted_task_id"] == task_id
    # Test if the task is actually deleted
    get_task_response = get_task_supressed(task_id)
    assert get_task_response == 404
    print("[4] Delete task test passed")


if __name__ == "__main__":
    test_create_get_task()
    test_update_get_task()
    test_list_three_tasks()
    test_delete_task()