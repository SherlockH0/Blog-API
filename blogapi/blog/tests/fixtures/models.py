import pytest
from django.contrib.auth.models import AbstractBaseUser
from model_bakery import baker

from blogapi.blog.models import Comment, Post


@pytest.fixture
def post(user: AbstractBaseUser) -> Post:
    return baker.make(Post, author=user)


@pytest.fixture
def comment(user: AbstractBaseUser) -> Comment:
    return baker.make(Comment, author=user)


@pytest.fixture
def post_json() -> dict:
    return {
        "title": "test",
        "content": "test",
        "automatic_answer_delay": "PT30M",
        "automatically_answer_comments": True,
    }


@pytest.fixture
def comment_json(post: Post, comment: Comment) -> dict:
    return {
        "content": "test",
        "post_id": post.pk,
        "parent_comment_id": comment.pk,
    }
