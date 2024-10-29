import pytest
from ninja.testing import TestClient

from blogapi.blog.models import Comment, Post


@pytest.mark.django_db
def test_read_comments(
    comment_api_client: TestClient,
):
    response = comment_api_client.get("/")
    expected_ids = Comment.objects.all().values_list("id", flat=True)
    response_ids = [comment["id"] for comment in response.data]

    assert response.status_code == 200
    assert set(response_ids) == set(expected_ids)
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"


@pytest.mark.django_db
def test_read_comment(
    comment: Comment,
    comment_api_client: TestClient,
):
    response = comment_api_client.get(f"/{comment.pk}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    assert response.data == {
        "author": {"id": comment.author.id, "username": comment.author.username},
        "id": comment.pk,
        "post": comment.post.pk,
        "content": comment.content,
        "parent_comment": comment.parent_comment,
        "created": f"{comment.created.isoformat()[:-9]}Z",
        "last_modified": f"{comment.last_modified.isoformat()[:-9]}Z",
        "blocked": comment.blocked,
        "ai_generated": comment.ai_generated,
    }


@pytest.mark.django_db
def test_create_comment(
    comment_api_client: TestClient,
    comment_json: dict,
    user_jwt: dict,
):
    response = comment_api_client.post(
        "/",
        json=comment_json,
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"


@pytest.mark.django_db
def test_update_comment(
    comment: Comment,
    comment_api_client: TestClient,
    post: Post,
    user_jwt: dict,
):
    response = comment_api_client.put(
        f"/{comment.pk}",
        json={
            "content": "new content",
            "post_id": post.pk,
            "parent_comment_id": None,
        },
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    assert response.json()["content"] == "new content"
    assert response.json()["parent_comment"] == None


@pytest.mark.django_db
def test_partial_update_comment(
    comment: Comment,
    comment_api_client: TestClient,
    user_jwt: dict,
):
    response = comment_api_client.patch(
        f"/{comment.pk}",
        json={
            "content": "partially new content",
        },
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"

    assert response.json()["content"] == "partially new content"
    assert response.json()["parent_comment"] == comment.parent_comment


@pytest.mark.django_db
def test_delete_comment(
    comment: Comment,
    comment_api_client: TestClient,
    user_jwt: dict,
):
    response = comment_api_client.delete(
        f"/{comment.pk}",
        headers={"Authorization": f"Bearer {user_jwt['access']}"},
    )

    assert response.status_code == 204
