import pytest
from ninja.testing import TestClient

from blogapi.blog.api import comments_router, posts_router


@pytest.fixture
def post_api_client():
    return TestClient(posts_router)


@pytest.fixture
def comment_api_client():
    return TestClient(comments_router)
