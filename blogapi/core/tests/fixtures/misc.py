import pytest
from django.test import override_settings


@pytest.fixture(autouse=True)
def test_settings(settings):
    with override_settings(
        SECRET_KEY="django-insecure-l1h1nb!(oz4*)@&3*pn*z=t^b!i)xud@&6gf%+oa2nsd)mj32v",
    ):
        yield
