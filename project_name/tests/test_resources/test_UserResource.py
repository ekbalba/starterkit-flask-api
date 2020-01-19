def test_index_page(testing_client):
    r = testing_client.get("/")  # Assumses that it has a path of "/"
    assert r.status_code == 200  # Assumes that it will return a 200 response


def test_index_page(testing_client):
    response = testing_client.post(
        "/v1/login", json={"email": "admin1@google.net", "password": "Admin123!"}
    )
    assert response.status_code == 200
    assert b"Login successful." in response.data
