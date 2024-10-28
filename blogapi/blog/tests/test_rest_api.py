import pytest
from model_bakery import baker
from ninja.testing import TestClient

from blogapi.blog.models import Post
from blogapi.core.utils.datetime import timedelta_isoformat


@pytest.mark.django_db
def test_read_posts(post_api_client: TestClient):
    response = post_api_client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_read_post(post_api_client: TestClient):
    post = baker.make(Post)
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
        "automatically_answer_comments": post.automatically_answer_comments,
        "automatic_answer_delay": timedelta_isoformat(post.automatic_answer_delay),
    }
