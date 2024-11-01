import pytest
from ninja.testing import TestClient

from blogapi.blog.models import Post
from blogapi.core.utils.datetime import timedelta_isoformat


@pytest.mark.django_db
def test_read_posts(
    post_api_client: TestClient,
):
    response = post_api_client.get("/")
    expected_ids = Post.objects.all().values_list("id", flat=True)
    response_ids = [post["id"] for post in response.data["items"]]

    assert response.status_code == 200
    assert set(response_ids) == set(expected_ids)
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"


@pytest.mark.django_db
def test_read_post(
    post: Post,
    post_api_client: TestClient,
):
    response = post_api_client.get(f"/{post.pk}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    assert response.data == {
        "author": {"id": post.author.id, "username": post.author.username},
        "id": post.pk,
        "title": post.title,
        "content": post.content,
        "created": f"{post.created.isoformat()[:-9]}Z",
        "last_modified": f"{post.last_modified.isoformat()[:-9]}Z",
        "last_moderated": (
            f"{post.last_moderated.isoformat()[:-9]}Z" if post.last_moderated else None
        ),
        "automatically_answer_comments": post.automatically_answer_comments,
        "status": post.status,
        "automatic_answer_delay": timedelta_isoformat(post.automatic_answer_delay),
        "block_reason": None,
    }


@pytest.mark.django_db
def test_create_post(
    post_api_client: TestClient,
    post_json: dict,
    user_jwt: dict,
):
    response = post_api_client.post(
        "/",
        json=post_json,
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"


@pytest.mark.django_db
def test_create_post_unauthorized(
    post_api_client: TestClient,
    post_json: dict,
):
    response = post_api_client.post(
        "/",
        json=post_json,
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_update_post(
    post: Post,
    post_api_client: TestClient,
    user_jwt: dict,
):
    response = post_api_client.put(
        f"/{post.pk}",
        json={
            "title": "new title",
            "content": "new content",
        },
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    assert response.json()["title"] == "new title"


@pytest.mark.django_db
def test_partial_update_post(
    post: Post,
    post_api_client: TestClient,
    user_jwt: dict,
):
    response = post_api_client.patch(
        f"/{post.pk}",
        json={
            "title": "partially new title",
        },
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    assert response.json()["title"] == "partially new title"
    assert response.json()["content"] == post.content


@pytest.mark.django_db
def test_delete_post(
    post: Post,
    post_api_client: TestClient,
    user_jwt: dict,
):
    response = post_api_client.delete(
        f"/{post.pk}",
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 204
