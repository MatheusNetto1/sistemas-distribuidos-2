from fastapi import status


def create_item(client, name="Caneta", description="Azul"):
    return client.post("/items/", json={"name": name, "description": description})


def test_create_item(client):
    response = create_item(client)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Caneta"
    assert data["description"] == "Azul"


def test_get_item_by_id(client):
    item_id = create_item(client).json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": item_id, "name": "Caneta", "description": "Azul"}


def test_list_items(client):
    create_item(client, "Caneta")
    create_item(client, "Lápis", None)

    response = client.get("/items/")

    assert response.status_code == status.HTTP_200_OK
    assert [item["name"] for item in response.json()] == ["Caneta", "Lápis"]


def test_update_item(client):
    item_id = create_item(client).json()["id"]

    response = client.patch(f"/items/{item_id}", json={"description": "Vermelha"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Caneta"
    assert response.json()["description"] == "Vermelha"
    assert client.get(f"/items/{item_id}").json()["description"] == "Vermelha"


def test_delete_item(client):
    item_id = create_item(client).json()["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"/items/{item_id}").status_code == status.HTTP_404_NOT_FOUND


def test_get_missing_item_returns_404(client):
    assert client.get("/items/999").status_code == status.HTTP_404_NOT_FOUND


def test_update_and_delete_missing_item_return_404(client):
    assert client.patch("/items/999", json={"name": "X"}).status_code == 404
    assert client.delete("/items/999").status_code == 404


def test_duplicate_name_returns_409(client):
    create_item(client)

    response = create_item(client)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_to_existing_name_returns_409(client):
    create_item(client, "Caneta")
    other_id = create_item(client, "Lápis").json()["id"]

    response = client.patch(f"/items/{other_id}", json={"name": "Caneta"})

    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_item_with_empty_name_is_rejected(client):
    response = client.post("/items/", json={"name": ""})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
