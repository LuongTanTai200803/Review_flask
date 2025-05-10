def test_create_task(client):
    response = client.post('/auth/login', json={
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 200
    #Lấy token từ response
    access_token = response.json['access_token']

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

def test_get_task(client):
    response = client.post('/auth/login', json={
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 200
    #Lấy token từ response
    access_token = response.json['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.get('/task/', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)         # API trả list
    if data:
        assert "id" in data[0]             # Mỗi task có id
        assert "title" in data[0]          # Mỗi task có title

def test_update_task(client):
    response = client.post('/auth/login', json={
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 200
    #Lấy token từ response
    access_token = response.json['access_token']

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

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    update_task = {
        "id": task_id,
        "due_date": None
    }
    response = client.put('/task/', json=update_task, headers=headers)
    assert response.status_code == 200
    assert response.json["msg"] == "Task update success"

def test_delete_task(client):
    response = client.post('/auth/login', json={
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 200
    #Lấy token từ response
    access_token = response.json['access_token']
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

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "id": task_id
    }
    del_response = client.delete('/task/', json = data, headers=headers)
    assert del_response.status_code == 200
    assert del_response.json["msg"] == "Task delete success"