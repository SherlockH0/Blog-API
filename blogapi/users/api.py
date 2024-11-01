from typing import Self

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router, Schema
from pydantic import field_validator, model_validator
from pydantic_core import PydanticCustomError


class UserIn(Schema):
    username: str
    password: str

    @model_validator(mode="after")
    def secure_password(self) -> Self:
        user = User(username=self.username)
        try:
            validate_password(password=self.password, user=user)
        except exceptions.ValidationError as e:
            raise PydanticCustomError(
                "weak_password",
                "Password is too weak. {error}",
                {"error": e.messages},
            )

        return self

    @field_validator("username")
    @classmethod
    def username_is_unique(cls, v):
        if User.objects.filter(username=v):
            raise ValueError("User with this username already exists")

        return v


class UserOut(Schema):
    id: int
    username: str


router = Router()


@router.post("")
def create_user(request, payload: UserIn):
    user = User.objects.create_user(**payload.dict())

    return {"id": user.pk}


@router.get("{user_id}/", response=UserOut)
def get_user(request, user_id: int):
    comment = get_object_or_404(get_user_model(), id=user_id)
    return comment
