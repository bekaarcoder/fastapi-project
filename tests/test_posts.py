import json


def test_get_all_posts(client, test_post):
    res = client.get("/posts/")
    print(res.json())
    assert res.status_code == 200


def test_create_post(authorized_client):
    res = authorized_client.post(
        "/posts/", json={"title": "Test title", "content": "Test Content"}
    )
    assert res.status_code == 201


def test_get_post(client, test_post):
    res = client.get(f'/posts/{test_post["id"]}/')
    print(res.json())
    assert res.status_code == 200


def test_delete_post(authorized_client, test_post):
    res = authorized_client.delete(f'/posts/{test_post["id"]}/')
    assert res.status_code == 204


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}/")
    print(client.headers)
    assert res.status_code == 401


def test_update_post(authorized_client, test_post):
    res = authorized_client.put(
        f'/posts/{test_post["id"]}/',
        json={
            "title": "Test title Updated",
            "content": "Test Content Updated",
        },
    )
    print(res.json())
    assert res.status_code == 200
    updated_post = res.json().get("data")
    assert updated_post.get("title") == "Test title Updated"
    assert updated_post.get("content") == "Test Content Updated"
