import pytest
from django.test import override_settings


@pytest.fixture(autouse=True)
def test_settings(settings):
    with override_settings(
        SECRET_KEY="ahf982hjadhpyc-9ums9dufg-a09sdf7n8A7DSF987F98A7SD9F7",
    ):
        yield
