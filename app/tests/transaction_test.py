API_URL = "/api/v1"


def budget_data_helper():
    return {"id": 0, "limit": 100.0, "name": "test_budget"}


def txn_data_helper(
    user_id=None, description="test description", amount=150.0, type="expense"
):
    return {
        "description": description,
        "amount": amount,
        "budget_id": 0,
        "user_id": user_id,
        "type": type,
    }


def create_user(client):
    response = client.post(
        f"{API_URL}/users/",
        json={"username": "testuser", "password": "password123", "balance": 1000.0},
    )

    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200  # O 201 si así está definido

    return response.json()


# ---------- Create ----------


def test_create_transaction_valid(client):
    user = create_user(client)
    txn_data = txn_data_helper(user_id=user["id"])
    response = client.post(f"{API_URL}/transactions/", json=txn_data)

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == txn_data["description"]
    assert data["amount"] == txn_data["amount"]
    assert data["user_id"] == user["id"]


def test_create_transaction_missing_field(client):
    user = create_user(client)
    txn_data = txn_data_helper(user_id=user.id)
    del txn_data["description"]
    response = client.post(f"{API_URL}/transactions/", json=txn_data)

    assert response.status_code == 422


def test_create_transaction_invalid_amount(client):
    user = create_user(client)
    txn_data = txn_data_helper(user_id=user["id"])
    txn_data["amount"] = -9
    response = client.post(f"{API_URL}/transactions/", json=txn_data)

    assert response.status_code == 422


def test_create_transaction_invalid_type(client):
    user = create_user(client)
    txn_data = txn_data_helper(user_id=user["id"])
    txn_data["type"] = "investment"
    response = client.post(f"{API_URL}/transactions/", json=txn_data)

    assert response.status_code == 422


# ---------- Read ----------


def test_get_transaction_by_id_success(client):
    user = create_user(client)
    txn_data = txn_data_helper(user_id=user["id"])
    response = client.post(f"{API_URL}/transactions/", json=txn_data)
    txn_id = response.json()["id"]

    response = client.get(f"{API_URL}/transactions/{txn_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == txn_id


def test_get_transaction_not_found(client):
    response = client.get(f"{API_URL}/transactions/999")
    assert response.status_code == 404


def test_list_transactions(client):
    user = create_user(client)
    for i in range(3):
        txn_data = txn_data_helper(description=f"txn {i}", user_id=user["id"])
        client.post(f"{API_URL}/transactions/", json=txn_data)

    response = client.get(f"{API_URL}/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_list_transactions_empty(client):
    response = client.get(f"{API_URL}/transactions/")
    assert response.status_code == 200
    assert response.json() == []


# ---------- Update ----------


def test_update_transaction_success(client):
    user = create_user(client)
    txn_data = txn_data_helper(user_id=user["id"])
    txn = client.post(f"{API_URL}/transactions/", json=txn_data).json()

    update_data = {"description": "Updated", "amount": 999.99}
    response = client.put(f"{API_URL}/transactions/{txn['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated"
    assert data["amount"] == 999.99


def test_update_transaction_invalid_data(client):
    user = create_user(client)
    txn = client.post(
        f"{API_URL}/transactions/", json=txn_data_helper(user_id=user["id"])
    ).json()

    response = client.put(f"{API_URL}/transactions/{txn['id']}", json={"amount": "bad"})
    assert response.status_code == 422


def test_update_transaction_not_found(client):
    response = client.put(f"{API_URL}/transactions/999", json={"description": "nope"})
    assert response.status_code == 404


# ---------- Delete ----------


def test_delete_transaction_success(client):
    user = create_user(client)
    txn = client.post(
        f"{API_URL}/transactions/", json=txn_data_helper(user_id=user["id"])
    ).json()

    response = client.delete(f"{API_URL}/transactions/{txn['id']}")
    assert response.status_code in [200, 204]

    response = client.get(f"{API_URL}/transactions/{txn['id']}")
    assert response.status_code == 404


def test_delete_transaction_not_found(client):
    response = client.delete(f"{API_URL}/transactions/999")
    assert response.status_code == 404
