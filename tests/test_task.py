from tests.conftest import authenticated_client


def test_create_task(authenticated_client): 
    client, access_token = authenticated_client  # unpack
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    task_data = {
        "title": "New Task",
        "status": "Pending",
        "due_date": "2025-5-10",
        "description": "test lần 1"
    }
    create_response = client.post('/task/', json=task_data, headers=headers)
    assert create_response.status_code == 201
    assert create_response.json['msg'] == "Task created"

def test_get_task(authenticated_client):
    client, access_token = authenticated_client  # unpack
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    task_data = {
        "title": "New Task",
        "status": "Pending",
        "due_date": "2025-5-10",
        "description": "test lần 1"
    }
    create_response = client.post('/task/', json=task_data, headers=headers)
    assert create_response.status_code == 201
    get_response = client.get('/task/', headers=headers)
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert isinstance(data, dict)  # Đảm bảo dữ liệu là một dictionary
    assert "tasks" in data        # Đảm bảo có khóa 'tasks'
    assert isinstance(data["tasks"], list)  # Kiểm tra value của 'tasks' là một list

    if data["tasks"]:  # Kiểm tra nếu danh sách không rỗng
        assert "id" in data["tasks"][0]      # Mỗi task có id
        assert "title" in data["tasks"][0]   # Mỗi task có title

def test_update_task(authenticated_client):
    client, access_token = authenticated_client  # unpack

    # Tạo task trước
    task_data = {
        "title": "New Task",
        "status": "Pending",
        "due_date": "2025-5-10",
        "description": "test lần 1"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/task/", json=task_data, headers=headers)
    assert response.status_code == 201
    task_id = response.json["task_id"]

    update_task = {
        "title": "Update"
    }
    response = client.put(f'/task/{task_id}', json=update_task, headers=headers)
    assert response.status_code == 200
    assert response.json["msg"] == "Task update success"

def test_delete_task(authenticated_client):
    client, access_token = authenticated_client  # unpack
    # Tạo task trước
    task_data = {
        "title": "New Task",
        "status": "Pending",
        "due_date": "2025-5-10",
        "description": "test lần 1"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    create_esponse = client.post("/task/", json=task_data, headers=headers)
    assert create_esponse.status_code == 201
    task_id = create_esponse.json["task_id"]

    del_response = client.delete(f'/task/{task_id}', headers=headers)
    assert del_response.status_code == 200
    assert del_response.json["msg"] == "Task delete success"