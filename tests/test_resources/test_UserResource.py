def test_index_page(testing_client):
    r = testing_client.get("/")  # Assumses that it has a path of "/"
    assert r.status_code == 200  # Assumes that it will return a 200 response
