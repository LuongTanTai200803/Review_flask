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

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    update_task = {
        "id": "011f0fd0-aac1-4a72-b52c-97ce5bfe5e65",
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

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "id": "09fd3e5c-a6a0-4555-ab26-24dcd2c0fdc7"
    }
    del_response = client.delete('/task/', json = data, headers=headers)
    assert del_response.status_code == 400
    assert del_response.json["msg"] == "Task Not Found"