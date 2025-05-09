def test_user_singup(client):
    response = client.post('/auth/singup', json={
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 400

def test_user_login(client):
    client.post('/auth/singup', json={
        "username": "newuser",
        "password": "password123"
    })
    response = client.post('/auth/login', json={
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
