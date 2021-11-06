import json


def test_get_all_posts(client, test_post):
    res = client.get("/posts/")
    print(res.json())
    assert res.status_code == 200


def test_create_post(authorized_client):
    res = authorized_client.post(
        "/posts/", json={"title": "Test title", "content": "Test Content"}
    )
    print(res.json())
    assert res.status_code == 201


def test_get_post(client, test_post):
    res = client.get(f'/posts/{test_post["id"]}/')
    print(res.json())
    assert res.status_code == 200
