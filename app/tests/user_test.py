API_URL = "/api/v1"


def user_data(username="test", password="test", balance=0.0):
    return {"username": username, "password": password, "balance": balance}


# ---------- Create ----------


def test_create_user_success(client):
    response = client.post(f"{API_URL}/users/", json=user_data("alice", "pass123", 500))
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["balance"] == 500


# def test_create_user_missing_username(client):
#     data = user_data()
#     del data["username"]
#     response = client.post(f"{API_URL}/users/", json=data)
#     assert response.status_code == 422
#
#
# def test_create_user_duplicate_username(client):
#     client.post(f"{API_URL}/users/", json=user_data("bob", "123", 100))
#     response = client.post(f"{API_URL}/users/", json=user_data("bob", "xyz", 200))
#     assert response.status_code in [400, 409]
#
#
# # ---------- Read ----------
#
#
# def test_get_user_by_id(client):
#     response = client.post(f"{API_URL}/users/", json=user_data("carl", "xyz", 100))
#     assert response.status_code == 200
#     user = response.json()
#     response = client.get(f"{API_URL}/users/{user['id']}")
#     assert response.status_code == 200
#     assert response.json()["username"] == "carl"
#
#
# def test_get_user_not_found(client):
#     response = client.get(f"{API_URL}/users/999")
#     assert response.status_code == 404
#
#
# def test_list_users(client):
#     client.post(f"{API_URL}/users/", json=user_data("u1", "p", 0))
#     client.post(f"{API_URL}/users/", json=user_data("u2", "p", 0))
#
#     response = client.get(f"{API_URL}/users/")
#     assert response.status_code == 200
#     assert len(response.json()) >= 2
#
#
# # ---------- Update ----------
#
#
# def test_update_user_success(client):
#     response = client.post(f"{API_URL}/users/", json=user_data("editme", "abc", 100))
#     assert response.status_code == 200
#     user = response.json()
#     update_data = {"username": "updated", "password": "new", "balance": 999}
#     response = client.put(f"{API_URL}/users/{user['id']}", json=update_data)
#     assert response.status_code == 200
#     assert response.json()["username"] == "updated"
#
#
# def test_update_user_not_found(client):
#     update_data = {"username": "nope", "password": "no", "balance": 0}
#     response = client.put(f"{API_URL}/users/999", json=update_data)
#     assert response.status_code == 404
#
#
# # ---------- Delete ----------
#
#
# def test_delete_user_success(client):
#     response = client.post(f"{API_URL}/users/", json=user_data("deleteme", "pass", 0))
#     assert response.status_code == 200
#     user = response.json()
#     response = client.delete(f"{API_URL}/users/{user['id']}")
#     assert response.status_code in [200, 204]
#
#
# def test_delete_user_not_found(client):
#     response = client.delete(f"{API_URL}/users/999")
#     assert response.status_code == 404
