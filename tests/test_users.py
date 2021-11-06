import pytest


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Hello FastApi from Ubuntu"


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "jim@gmail.com", "password": "password123"}
    )
    print(response.json())
    assert response.status_code == 201


def test_login(client, test_user):
    response = client.post(
        "/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("jim@gmail.com", "passsword", 403),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post(
        "/login",
        json={"email": email, "password": password},
    )
    print(response.json())
    assert response.status_code == status_code
