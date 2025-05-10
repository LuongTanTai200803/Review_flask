def test_create_post(client):
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
    post_data = {
        #"title": "Chill",
        "content": "Viết test integration"
    }
    create_response = client.post('/post/', json=post_data, headers=headers)
    assert create_response.status_code == 400
    assert create_response.json["msg"] == "Not Enough Data" 

def test_get_post(client):
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
    response = client.get('/post/', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)         # API trả list
    assert "post" in data
    if data["post"]:
        for post in data["post"]:
            assert "title" in post            # Mỗi post có title
            assert "content" in post      # Mỗi post có content

def test_update_post(client):
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
    post_data = {
        "title": "Chill",
        "content": "Viết test integration"
    }
    create_response = client.post('/post/', json=post_data, headers=headers)
    print(create_response.json)
    assert create_response.status_code == 201
    post_id = create_response.json["post_id"]

    update_post = {
        "title": "one"
    }
    update_response = client.put(f'/post/{post_id}', json=update_post, headers=headers)
    assert update_response.status_code == 200
    assert update_response.json["msg"] == "Post update success"

def test_delete_post(client):
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
    
    del_response = client.delete('/post/09fd3e5c-a6a0-4555-ab26-24dcd2c0fdc7', headers=headers)
    assert del_response.status_code == 404
    assert del_response.json["error"] == "Post Not Found"

def test_post_search_and_pagination(client):
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
    # Tạo post
    post_data = {
        "title": "Chill",
        "content": "Viết test integration"
    }
    create_response = client.post('/post/', json=post_data, headers=headers) # Tạo post thứ 1
    create_response = client.post('/post/', json=post_data, headers=headers) # Tạo post thứ 2
    assert create_response.status_code == 201
    # Thực hiện yêu cầu GET với search query và pagination
    response = client.get('/post/?q=Chill&page=1&per_page=1', headers=headers) # Lấy post

    # Kiểm tra mã trạng thái
    assert response.status_code == 200

    # Test tìm kiếm từ khóa
    data = response.json
    assert len(data['post']) == 1  # 1 bài viết trên trang đầu tiên
    assert data['total'] == 2
    assert data['page'] == 1    # page hiện tại
    assert data['pages'] == 2   # Số lượng page

    # Test phân trang
    create_response = client.post('/post/', json=post_data, headers=headers) # Tạo post thứ 3
    response = client.get('/post/', headers=headers, query_string={"q": "", "page": 1, "per_page": 2})
    assert response.status_code == 200
    data = response.json
    assert len(data['post']) == 2  # 2 bài viết trên trang đầu tiên
    assert data['total'] == 3  # Tổng số bài viết phải là 3
    assert data['page'] == 1
    assert data['pages'] == 2  # Số trang phải là 2 khi per_page = 2

    # Kiểm tra dữ liệu trả về
    data = response.json
    assert "page" in data
    assert "pages" in data
    assert "total" in data
    assert isinstance(data["post"], list)

    assert isinstance(data, dict)  # Cả response là dict
    assert isinstance(data["post"], list)  # "post" là list
    for post in data["post"]:
        assert isinstance(post, dict)  # Mỗi phần tử trong "post" là dict

    # Kiểm tra từng bài post
    for post in data["post"]:
        assert isinstance(post, dict)
        required_keys = {"id", "title", "content", "user_id"}
        assert required_keys.issubset(post)