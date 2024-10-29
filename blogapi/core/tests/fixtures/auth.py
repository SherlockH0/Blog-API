import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from model_bakery import baker
from ninja_jwt.tokens import RefreshToken


@pytest.fixture
def user():
    return baker.make(get_user_model())


@pytest.fixture
def user_jwt(user: AbstractBaseUser):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh.token),
        "access": str(refresh.access_token),  # pyright: ignore
    }
